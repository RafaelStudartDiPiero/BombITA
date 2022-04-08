import pygame
from constants import *
import os
from bomb import *

# Loading Image for Player
vector = pygame.math.Vector2
dir_project = os.path.dirname(__file__)
dir_images = os.path.join(dir_project, 'images')
sprite_player = pygame.image.load(os.path.join(dir_images, 'bomberman.png'))


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        # Defining initial values for Attributes
        self.destroyed = False
        self.grid_pos = pos
        self.pix_pos = vector(
            self.grid_pos.x*self.game.cell_width + self.game.cell_width / 2,
            self.grid_pos.y*self.game.cell_height + self.game.cell_height / 2)
        self.direction = vector(0, 0)
        self.change_direction = False
        self.orientation = 0
        self.base_rect = None
        self.banned_direction = vector(1, 1)
        self.blocked = False

        # Instantiating the bomb for the Player
        self.bomb = Bomb(self.game)
        self.sprites_bomb = pygame.sprite.Group()
        self.sprites_bomb.add(self.bomb)

        # Defining Player Sprite
        self.player_images = []
        for row in range(4):
            for col in range(3):
                self.img = sprite_player.subsurface((col * 32, row * 32), (32, 32))
                self.img = pygame.transform.scale(self.img, (32*2, 32*2))
                self.player_images.append(self.img)

        self.index_img = 0
        self.image = self.player_images[self.index_img]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Updates the state of player"""
        # Moves in a unbanned direction
        if self.direction != self.banned_direction:
            self.pix_pos += self.direction*2

        # Changes sprite image based in change in direction
        if self.change_direction:
            self.index_img = self.orientation * 3

        # Changes sprite image based in time
        self.index_img += 0.2
        if self.index_img >= 3*(self.orientation + 1):
            self.index_img = self.orientation * 3

        # Updates sprite
        self.image = self.player_images[int(self.index_img)]
        self.rect.center = self.pix_pos

        # Updates the player bomb
        self.bomb.update()

    def draw(self):
        """Draws necessary elements for the player"""
        # Draw the player's bomb
        if self.bomb.dropped:
            self.sprites_bomb.draw(self.game.window)

    def move(self, direction, orientation):
        """Decides it's movement in a certain direction"""
        if direction != self.direction:
            self.change_direction = True
        else:
            self.change_direction = False

        self.direction = direction
        self.orientation = orientation

    def drop_bomb(self):
        """Drops the bomb, if another isn't dropped"""
        if not self.bomb.dropped:
            self.bomb.dropped = True
            self.bomb.pos.x = self.pix_pos.x
            self.bomb.pos.y = self.pix_pos.y

    def ban_direction(self):
        """Bans a direction of the movement"""
        if not self.blocked:
            self.banned_direction = self.direction

    def destroy(self):
        """Destroys the player, removing it from the screen."""
        self.pix_pos = vector(880, 450)
        self.destroyed = True
        self.rect.center = self.pix_pos
