import pygame

pygameSurf = pygame.surface.Surface

class PickleableSurface(pygameSurf):
    def __init__(self, *arg,**kwarg):
        size = arg[0]

        # size given is not an iterable,  but the object of pygameSurf itself
        if (isinstance(size, pygameSurf)):
            pygameSurf.__init__(self, size=size.get_size(), flags=size.get_flags())
            self.surface = self
            self.name='test'
            self.blit(size, (0, 0))

        else:
            pygameSurf.__init__(self, *arg, **kwarg)
            self.surface = self
            self.name = 'test'

    def __getstate__(self):
        state = self.__dict__.copy()
        surface = state["surface"]

        _1 = pygame.image.tostring(surface.copy(), "RGBA")
        _2 = surface.get_size()
        _3 = surface.get_flags()
        state["surface_string"] = (_1, _2, _3)
        return state

    def __setstate__(self, state):
        surface_string, size, flags = state["surface_string"]

        pygameSurf.__init__(self, size=size, flags=flags)

        s=pygame.image.fromstring(surface_string, size, "RGBA")
        state["surface"] =s;
        self.blit(s,(0,0));self.surface=self;
        self.__dict__.update(state)

class PhysicsEntity:
    def __init__(self, e_type, pos, size) -> None:
        self.first = True
        self.type = e_type
        self.pos = list(pos)  # so that each entity has its own list for pos values and not share any with other entities
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.action = ''
        self.anim_offset = (-3,-3)
        self.flip = False

    def set_action(self, action, game):
        if action != self.action:
            self.action = action
            self.animation = game.assets[self.type + '/' + self.action].copy()


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self,game, tilemap, movement=(0,0)):
        if self.first:
            self.set_action('idle', game)
            self.first = False

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])



        self.pos[0] += self.frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True

                if self.frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True

                self.pos[0] = entity_rect.x

        self.pos[1] += self.frame_movement[1]

        entity_rect = self.rect()

        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.velocity[1] = 0
                    self.collisions['down'] = True

                if self.frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.velocity[1] = 0
                    self.collisions['up'] = True

                self.pos[1] = entity_rect.y
       
        if self.frame_movement[0] > 0:
            self.flip = False

        elif self.frame_movement[0] < 0:
            self.flip = True

        if not self.collisions['down']:
            self.velocity[1] = min(5, self.velocity[1] + .1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity):
    def __init__(self, pos, size) -> None:
        super().__init__('player', pos, size)
        self.airtime = 0
        

    def update(self, game, tilemap, movement=(0, 0)):
        super().update(game, tilemap, movement)
    
        self.airtime += 1

        if self.collisions['down']:
            self.airtime = 0

        if self.airtime > 4:
            self.set_action('jump',game)

        elif movement[0] != 0:
            self.set_action('run',game)

        else:
            self.set_action('idle',game)

