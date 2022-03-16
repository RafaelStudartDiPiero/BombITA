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
        self.base_rect = None
        self.banned_direction = vector(1,1)
        self.blocked = False

    def update(self):
        if self.direction != self.banned_direction:
            self.pix_pos += self.direction*2
        print(self.banned_direction)
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




    def draw(self):
        self.base_rect = pygame.draw.rect(self.game.window, 'red', (int(self.pix_pos.x) - 9, int(self.pix_pos.y) + 10,
                           (self.game.cell_width - 5) // 2, (self.game.cell_height - 5) // 2))
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

    def ban_direction(self):
        if not self.blocked:
            print("aaaaaaa")
            self.banned_direction = self.direction
            print(self.banned_direction)


