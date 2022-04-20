import pygame
from constants import *
import os
import random
from powerup import PowerUp

vector = pygame.math.Vector2

# Loading Image for blocks.
dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_boot = pygame.image.load(os.path.join(dir_images, 'boots.png'))


class SpeedPowerUp(PowerUp):
    def __init__(self, game, grid_pos):
        super().__init__(game, grid_pos)

        # Defining speed powerup sprite
        self.boot_images = []
        self.img = sprite_boot.subsurface((3 * 96, 1 * 96), (96, 96))
        self.img = pygame.transform.scale(self.img, (self.game.cell_width,
                                                     self.game.cell_height))
        self.boot_images.append(self.img)
        self.index_img = 0
        self.image = self.boot_images[self.index_img]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.pix_pos

        self.destroyed = False

    def update(self):
        pass


