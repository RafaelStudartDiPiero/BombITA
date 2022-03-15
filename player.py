import pygame
from constants import *
import os
vector = pygame.math.Vector2

dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project,'images')
sprite_player = pygame.image.load(os.path.join(dir_images, 'bomberman.png'))


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.grid_pos = pos
        self.pix_pos = vector(self.grid_pos.x*self.game.cell_width + self.game.cell_width /2,
                              self.grid_pos.y*self.game.cell_height + self.game.cell_height /2)
        self.direction = vector(0, 0)
        self.dropped = False
        self.bomb_time = 0
        self.bomb_pos = vector(0,  0)
        self.player_images = []
        for row in range(4):
            for col in range(3):
                self.img = sprite_player.subsurface((col * 32, row * 32), (32, 32))
                self.img = pygame.transform.scale(self.img, (32*2, 32*2))
                self.player_images.append(self.img)

        self.index_img = 0
        self.image = self.player_images[self.index_img]
        self.rect = self.image.get_rect()
        self.change_direction = False
        self.orientation = 0

    def update(self):
        if self.direction != vector(0,0):
            self.pix_pos += self.direction*2

        if self.bomb_time < 4*FPS:
            self.bomb_time += 1
        else:
            self.dropped = False
            self.bomb_time = 0

        if self.change_direction:
            self.index_img = self.orientation * 3

        self.index_img += 0.2
        if self.index_img >= 3*(self.orientation + 1):
            self.index_img = self.orientation * 3

        self.image = self.player_images[int(self.index_img)]
        self.rect.center = self.pix_pos
        print(self.index_img)

    def draw(self):
        if self.dropped == True:
            pygame.draw.circle(self.game.window, 'black', (int(self.bomb_pos.x), int(self.bomb_pos.y)),
                              (self.game.cell_height - 5) // 2)

    def move(self, direction, orientation):
        if direction != self.direction:
            self.change_direction = True
        else:
            self.change_direction = False

        self.direction = direction
        self.orientation = orientation

    def drop_bomb(self):
        if not self.dropped:
            self.dropped = True
            self.bomb_pos.x = self.pix_pos.x
            self.bomb_pos.y = self.pix_pos.y



