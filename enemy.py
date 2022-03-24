import pygame
from constants import *
import os
import random
vector = pygame.math.Vector2

dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_enemy = pygame.image.load(os.path.join(dir_images, 'enemies.png'))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        """"""
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.grid_pos = pos
        self.pix_pos = vector(
            self.grid_pos.x * self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y * self.game.cell_height + self.game.cell_height / 2)
        self.direction = vector(0, 0)
        self.enemy_images = []
        for col in range(12):
            if col == 3:
                self.img = sprite_enemy.subsurface((col * 25 + 4, 0), (23, 32))
                self.img = pygame.transform.scale(self.img, (23*2, 32*2))
                self.enemy_images.append(self.img)
            elif col == 5:
                self.img = sprite_enemy.subsurface((col * 25 + 1, 0), (23, 32))
                self.img = pygame.transform.scale(self.img, (23 * 2, 32 * 2))
                self.enemy_images.append(self.img)
            elif col == 9:
                self.img = sprite_enemy.subsurface((col * 25 + 4, 0), (23, 32))
                self.img = pygame.transform.scale(self.img, (23 * 2, 32 * 2))
                self.enemy_images.append(self.img)
            else:
                self.img = sprite_enemy.subsurface((col * 25 + 1, 0), (25, 32))
                self.img = pygame.transform.scale(self.img, (25 * 2, 32 * 2))
                self.enemy_images.append(self.img)

        self.index_img = 0
        self.image = self.enemy_images[self.index_img]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.must_sort = True
        self.time_sort = 0
        self.collision_bool = False
        self.orientation = 0
        self.destroyed = False

    def update(self):
        """"""
        if not self.destroyed:
            if self.time_sort < 6*FPS:
                self.time_sort += 1
            else:
                self.time_sort = 0
                self.must_sort = True
            self.collision()

            self.sort_direction()

            self.pix_pos += self.direction * 1

            self.index_img += 0.2
            if self.index_img >= 3 * (self.orientation + 1):
                self.index_img = self.orientation * 3

            self.image = self.enemy_images[int(self.index_img)]
            self.rect.center = self.pix_pos

    def draw(self):
        """"""
        pass

    def sort_direction(self):
        """"""
        possible_directions = [vector(1, 0), vector(-1, 0), vector(0, 1), vector(0, -1)]
        if self.must_sort:
            self.grid_pos = vector(
                int(self.pix_pos.x/self.game.cell_width),
                int(self.pix_pos.y/self.game.cell_height))

            for wall in self.game.walls:
                if wall == vector(self.grid_pos.x+1, self.grid_pos.y):
                    possible_directions.remove(vector(1, 0))
                elif wall == vector(self.grid_pos.x-1, self.grid_pos.y):
                    possible_directions.remove(vector(-1, 0))
                elif wall == vector(self.grid_pos.x, self.grid_pos.y+1):
                    possible_directions.remove(vector(0, 1))
                elif wall == vector(self.grid_pos.x, self.grid_pos.y-1):
                    possible_directions.remove(vector(0, -1))

            self.direction = random.choice(possible_directions)
            self.define_orientation()
            self.index_img = self.orientation*3
            self.time_sort = 0
            self.must_sort = False

    def collision(self):
        """"""
        for wall in self.game.walls:
            dist_x = abs((wall.x + 1/2)*self.game.cell_width - self.pix_pos.x)
            dist_y = abs((wall.y + 1/2)*self.game.cell_height - (self.pix_pos.y + 20))

            if dist_x < self.game.cell_width*3/5 and dist_y < self.game.cell_height*3/5:
                self.must_sort = True

    def define_orientation(self):
        """"""
        if self.direction == (0, -1):
            self.orientation = 0
        elif self.direction == (1, 0):
            self.orientation = 1
        elif self.direction == (0, 1):
            self.orientation = 2
        elif self.direction == (-1, 0):
            self.orientation = 3

    def destroy(self):
        self.pix_pos = vector(880, 450)
        self.destroyed = True
        self.rect.center = self.pix_pos
