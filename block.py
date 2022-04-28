import pygame
from constants import *
import os
import random
from speed import SpeedPowerUp

vector = pygame.math.Vector2

# Loading Image for blocks.
dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_block = pygame.image.load(os.path.join(dir_images, 'blocks.png'))


class Block(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        # Defining random initial position for them
        self.grid_pos = vector(random.randint(0, X_CELLS), random.randint(0, Y_CELLS))
        self.pix_pos = vector(
            self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)

        # Defining block sprite
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

        # Checking if the random initial position is free to position the block
        self.free = False
        while not self.free:
            self.grid_pos = vector(random.randint(0, X_CELLS - 1),
                                   random.randint(0, Y_CELLS - 1))
            self.free = True
            # Checking if the position is already occupied
            for wall in self.game.walls:
                if wall.x == self.grid_pos.x and wall.y == self.grid_pos.y:
                    self.free = False
            # Checking if the position is one of the reserved ones.
            if self.grid_pos == vector(2, 1) or self.grid_pos == vector(3, 1) or self.grid_pos == vector(2, 2) or \
                    self.grid_pos == vector(14, 11) or self.grid_pos == vector(13, 11) or\
                    self.grid_pos == vector(14, 10) or self.grid_pos == vector(6, 6) or self.grid_pos == vector(6, 5):
                self.free = False

        # Adding this position to the list of impassable
        self.game.walls.append(self.grid_pos)
        self.rect.center = vector(
            self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)
        # Defining the initial state of block
        self.destroyed = False

        #adding a power up
        self.power_up = SpeedPowerUp(self.game, self.grid_pos)
        self.sprites_power_up = pygame.sprite.Group()
        self.sprites_power_up.add(self.power_up)
        if random.random() > 0.5:
            self.power_up.exist = 1

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
        """Destroys block and removes from impassable positions list"""
        self.game.walls.remove(vector(
            int(self.grid_pos.x),
            int(self.grid_pos.y)))
        self.destroyed = True
        self.power_up.appearance = True


    def draw(self):
        """draw the power up"""
        if self.destroyed and self.power_up.exist:
            self.sprites_power_up.draw(self.game.window)
