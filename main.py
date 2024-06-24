import pygame, sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import loadImage, loadImages, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
import random
from scripts.particle import Particle
import math
from network2 import Network


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
    
        self.display = pygame.Surface((320,240))

        pygame.display.set_caption('')

        self.clock = pygame.time.Clock()

        self.movement = [False,False]

        self.assets = {
            'decor': loadImages('tiles/decor'),
            'grass': loadImages('tiles/grass'),
            'large_decor': loadImages('tiles/large_decor'),
            'spawners': loadImages('tiles/spawners'),
            'stone': loadImages('tiles/stone'),
            'player':loadImage('entities/player.png'),
            'background':loadImage('background.png'),
            'clouds': loadImages('clouds'),
            'player/idle': Animation(loadImages('entities/player/idle'), image_dur = 4),
            'player/run': Animation(loadImages('entities/player/run'), image_dur=6),
            'player/jump': Animation(loadImages('entities/player/jump')),
            'player/slide': Animation(loadImages('entities/player/slide')),
            'player/wall_slide': Animation(loadImages('entities/player/wall_slide')),
            'particles': Animation(loadImages('particles/particle')),
            'particle/leaf': Animation(loadImages('particles/leaf'), image_dur=20, loop=False),
        }

        self.network = Network()

        self.pos = [100,200]

        pdata = self.network.get_p()
        # print(pdata)
        self.player = Player(pdata['pos'], (8,15))
        self.p2 = Player((50,50), (8,15))
         

        self.tilemap = TileMap(self)

        self.p2.update(self, self.tilemap,(0, 0))

        self.offset = [0,0]

        self.clouds = Clouds(self.assets['clouds'])

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(tree['pos'][0] + 4, tree['pos'][1] + 4, 23, 13))

        self.particles = []



    def run(self):
        while True:
            self.player.update(self,self.tilemap,(self.movement[1] - self.movement[0],0))
            player_data = self.network.send({'movement':self.player.frame_movement, 'pos': self.player.pos})
            self.p2.frame_movement = player_data['movement']
            self.p2.pos = player_data['pos']

            pygame.display.update()
            self.display.blit(pygame.transform.scale(self.assets['background'],self.display.get_size()), (0,0))
            
            self.offset[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.offset[0])/20
            self.offset[1] += (self.player.rect().centery - self.display.get_height()/2 - self.offset[1])/20

            render_offset = (int(self.offset[0]),int(self.offset[1]))

            
            self.clouds.update()
            self.clouds.render(self.display, render_offset)

            self.tilemap.physics_rect_around(self.player.pos)
            
            self.tilemap.render(self.display, offset =render_offset)
            
            for rect in self.leaf_spawners:
                if random.random() * 30000 < rect.width * rect.height:
                    pos = [rect.x + random.random()* rect.width, rect.y + random.random()*rect.height]
                    self.particles.append(Particle(self, 'leaf', pos, [.1,.3], random.randint(0,20)))


            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display,offset= render_offset)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame*.035) * .3
                if kill:    
                    self.particles.remove(particle)
            
            self.p2.update(self, self.tilemap,player_data['movement'])
            self.player.render(self.display, offset = render_offset)
            self.p2.render(self.display,render_offset)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        
                        self.movement[0] = True

                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3

                    if event.key == pygame.K_s:
                        if self.player.flip:
                            self.player.velocity[0] = -5
                        else:
                            self.player.velocity[0] = 5
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        
                        self.movement[0] = False

                    if event.key == pygame.K_s:
                        self.player.velocity[0] = 0
                    
                
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
