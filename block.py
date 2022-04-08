import pygame
from constants import *
import os
import random

vector = pygame.math.Vector2

dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_block = pygame.image.load(os.path.join(dir_images, 'blocks.png'))


class Block(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.grid_pos = vector(random.randint(0, X_CELLS), random.randint(0, Y_CELLS))
        self.pix_pos = vector(
            self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)
        self.block_images = []

        self.img = sprite_block.subsurface((0 * 56, 4 * 56), (56, 56))
        self.img = pygame.transform.scale(self.img, (self.game.cell_width,
                                                     self.game.cell_height))
        self.block_images.append(self.img)
        self.index_img = 0
        self.image = self.block_images[self.index_img]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.pix_pos
        self.free = False
        while not self.free:
            self.grid_pos = vector(random.randint(0, X_CELLS - 1),
                                   random.randint(0, Y_CELLS - 1))
            self.free = True
            for wall in self.game.walls:
                if wall.x == self.grid_pos.x and wall.y == self.grid_pos.y:
                    self.free = False

        self.game.walls.append(self.grid_pos)
        self.rect.center = vector(
            self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)
        self.destroyed = False

    def update(self):
        pass
        # while not self.free:
        #     self.grid_pos = vector(random.randint(0, X_CELLS - 1),
        #                            random.randint(0, Y_CELLS - 1))
        #     self.free = True
        #     for wall in self.game.walls:
        #         if wall.x == self.grid_pos.x and wall.y == self.grid_pos.y:
        #             self.free = False
        #
        # self.game.walls.append(self.grid_pos)
        # self.rect.center = vector(
        #     self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
        #     self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)

    def destroy(self):
        self.game.walls.remove(vector(
            int(self.grid_pos.x),
            int(self.grid_pos.y)))
        self.destroyed = True

