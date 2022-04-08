import pygame
from constants import *
import os

# Loading Image for bomb
dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_bomb = pygame.image.load(os.path.join(dir_images, 'bombs.png'))


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        # Defining initial values for attributes
        self.time = 0
        self.time_explosion = 0
        self.pos = vector(0, 0)
        self.dropped = False
        self.time_bomb = 1.2 * FPS
        self.exploded = False
        self.added_walls = False

        # Defining bomb sprite
        self.bomb_images = []
        for row in range(3):
            self.img = sprite_bomb.subsurface((row*18, 0), (18, 21))
            self.img = pygame.transform.scale(self.img, (18*2, 21*2))
            self.bomb_images.append(self.img)
        for row in range(3, 6):
            self.img = sprite_bomb.subsurface((460, 32), (52, 52))
            self.img = pygame.transform.scale(self.img, (52*2, 52*2))
            self.bomb_images.append(self.img)

        self.index_img = 0
        self.image = self.bomb_images[self.index_img]
        self.rect = self.image.get_rect()
        #  self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        """Updates the bomb state"""
        # Check if the bomb is dropped
        if self.dropped:
            # Behavior before Explosion
            if self.time < self.time_bomb:
                self.time += 1
                self.image = self.bomb_images[int(self.index_img)]
                self.index_img += 3 / self.time_bomb
                self.rect.center = self.pos
                # Allowing movement for a period for stopping bugged movement
                if self.time > self.time_bomb/2:
                    if not self.added_walls and self.dropped:
                        self.game.walls.append(vector(
                            int(self.pos.x/self.game.cell_width),
                            int(self.pos.y/self.game.cell_height)))
                        self.added_walls = True
            # Behavior During Explosion
            elif self.time_explosion < self.time_bomb/3:
                print()
                self.time_explosion += 1
                self.index_img = 5
                self.image = self.bomb_images[int(self.index_img)]
                self.rect.center = self.pos + vector(-30, -20)
                self.exploded = True

            # Behavior After Explosion
            else:
                self.time = 0
                self.time_explosion = 0
                if self.dropped and self.added_walls:
                    self.game.walls.remove(vector(
                            int(self.pos.x/self.game.cell_width),
                            int(self.pos.y/self.game.cell_height)))
                    self.added_walls = False
                self.exploded = False
                self.dropped = False
                self.index_img = 0
