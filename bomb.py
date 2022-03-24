import pygame
from constants import *
import os

dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_bomb = pygame.image.load(os.path.join(dir_images, 'bombs.png'))


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.time = 0
        self.time_explosion = 0
        self.pos = vector(0, 0)
        self.bomb_images = []
        for row in range(3):
            self.img = sprite_bomb.subsurface((row*16, 0), (16, 16))
            self.img = pygame.transform.scale(self.img, (32, 32))
            self.bomb_images.append(self.img)
        for row in range(3, 6):
            self.img = sprite_bomb.subsurface((row*16 + 5, 17), (16, 16))
            self.img = pygame.transform.scale(self.img, (32*2, 32*2))
            self.bomb_images.append(self.img)

        self.index_img = 0
        self.image = self.bomb_images[self.index_img]
        self.rect = self.image.get_rect()
        self.dropped = False
        self.time_bomb = 4*FPS
        
    def update(self):
        if self.time < self.time_bomb:
            self.time += 1
            self.image = self.bomb_images[int(self.index_img)]
            self.index_img += 3 / self.time_bomb

        elif self.time_explosion < self.time_bomb/3:
            self.time_explosion += 1
            self.index_img = 5
            self.image = self.bomb_images[int(self.index_img)]

        else:
            self.time = 0
            self.time_explosion = 0
            self.dropped = False
            self.index_img = 0

        self.rect.center = self.pos

