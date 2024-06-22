class Particle:
    def __init__(self, game, p_type, pos, velocity = [0,0], frame=0) -> None:
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation_frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill
    
    def render(self, screen, offset = (0,0)):
        img = self.animation.img()

        screen.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

