import pygame, os

import pygame.image

BASE_IMAGE_PATH = 'data/images/'

def loadImage(path):
    img = pygame.image.load(os.path.join(BASE_IMAGE_PATH ,path)).convert()
    img.set_colorkey((0,0,0))
    return img
    
def loadImages(path):
    images = [loadImage(os.path.join(path,image_name)) for image_name in sorted(os.listdir(BASE_IMAGE_PATH + path))]

    return images

class Animation:
    def __init__(self, images, image_dur=5, loop = True) -> None:
        self.images = images
        self.image_duration = image_dur
        self.loop = loop
        self.done = False
        self.frame = 0


    def copy(self):
        return Animation(self.images,image_dur= self.image_duration,loop= self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1)%(self.image_duration * len(self.images))

        else:
            self.frame = min(self.frame + 1,  self.image_duration*len(self.images) - 1)
            if self.frame >= self.image_duration*len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame/self.image_duration)]