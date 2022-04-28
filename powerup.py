import pygame
from constants import *
import os
import random

vector = pygame.math.Vector2

# Loading Image for blocks.
dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_block = pygame.image.load(os.path.join(dir_images, 'blocks.png'))


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, grid_pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        # Defining random initial position for them
        self.grid_pos = grid_pos
        self.pix_pos = vector(
            self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)

        # Defining the initial state of powerup
        self.destroyed = False
        self.appearance = False
        self.exist = False

    def update(self):
        pass


    def destroy(self):
        """Destroys power up image"""
        self.pix_pos = vector(880, 450)
        self.destroyed = True
        self.rect.center = self.pix_pos
