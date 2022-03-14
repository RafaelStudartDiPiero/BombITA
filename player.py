import pygame
from constants import *
vector = pygame.math.Vector2

class Player:
    def __init__(self, game, pos):
        self.game = game
        self.grid_pos = pos
        self.pix_pos = vector(self.grid_pos.x*self.game.cell_width + self.game.cell_width /2,
                              self.grid_pos.y*self.game.cell_height + self.game.cell_height /2)
        self.direction = vector(0,0)
        self.dropped = False
        self.bomb_time = 0
        self.bomb_pos = vector(0,0)

    def update(self):
        if self.direction != vector(0,0):
            self.pix_pos += self.direction*2
        if self.bomb_time < 4*FPS:
            self.bomb_time += 1
        else:
            self.dropped = False
            self.bomb_time = 0

    def draw(self):
        pygame.draw.circle(self.game.window, 'red', (int(self.pix_pos.x),int(self.pix_pos.y)), (self.game.cell_height - 5)//2)

        if self.dropped == True:
            pygame.draw.circle(self.game.window, 'black', (int(self.bomb_pos.x), int(self.bomb_pos.y)),
                              (self.game.cell_height - 5) // 2)

    def move(self, direction):
        self.direction = direction

    def drop_bomb(self):
        if not self.dropped:
            self.dropped = True
            self.bomb_pos.x = self.pix_pos.x
            self.bomb_pos.y = self.pix_pos.y
