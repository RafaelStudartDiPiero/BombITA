import pygame
import sys
import os
from constants import *
from player import *
from block import *
from enemy import *
import math


class Game:
    def __init__(self):
        """Method responsible for initializing and defining import attributes that will be used during the game"""
        # PyGame Initialization
        pygame.init()
        pygame.mixer.init()
        # Window Configuration
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        # Defining Clock
        self.clock = pygame.time.Clock()
        # Game States
        self.is_running = True
        self.state = 'menu'
        self.multiplayer = False
        # Starting Menu Options
        self.menu_options = 0
        # Defining BackGrounds
        self.playing_background = None
        self.menu_background = None
        self.gameover_background = None
        # Audio Directory
        self.dir_audios = None
        # List of Walls that Player Can't Trespass
        self.walls = []
        # Loading Images and Creating Walls
        self.load_files()
        # Defining Cell Constants
        self.cell_width = WIDTH//X_CELLS
        self.cell_height = HEIGHT//Y_CELLS
        # Instantiating Players
        self.player1 = Player(self, PLAYER1_START_POS)
        self.player2 = Player(self, PLAYER2_START_POS)
        # Instantiating Basic Enemy
        self.enemy = Enemy(self, ENEMY_START_POS)
        # Instantiating list of Breakable Blocks
        self.blocks = [None]*BLOCKS_NUMBER
        for i in range(len(self.blocks)):
            self.blocks[i] = Block(self)
        # Creating a SpriteGroup that will be used to update all sprites that will be used simultaneously
        self.all_sprites = pygame.sprite.Group()
        for i in range(len(self.blocks)):
            self.all_sprites.add(self.blocks[i])
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.enemy)
        # Creating a SpriteGroup that will be used to contain all elements that causes GameOver when collide with player
        self.collision_sprites = pygame.sprite.Group()
        self.collision_sprites.add(self.enemy)
        # Creating a SpriteGroup that will be used to define the interaction between bomb1 and players
        self.collision_sprites_bomb1_player = pygame.sprite.Group()
        self.collision_sprites_bomb1_player.add(self.player1.bomb)
        # Creating a SpriteGroup that will be used to define the interaction between bomb2 and players
        self.collision_sprites_bomb2_player = pygame.sprite.Group()
        self.collision_sprites_bomb2_player.add(self.player2.bomb)
        # Creating a SpriteGroup that will be used to define the interaction between the bomb and the enemy
        self.collision_sprites_bomb = pygame.sprite.Group()
        self.collision_sprites_bomb.add(self.enemy)
        # Creating a SpriteGroup that will be used to define the interaciont between the bomb and the blocks
        self.collision_sprites_bomb_block = pygame.sprite.Group()
        for i in range(len(self.blocks)):
            self.collision_sprites_bomb_block.add(self.blocks[i])
        # Creating a Bool Variable to Check if a Player1 needs to be Blocked
        self.is_player1_blocked = False
        # Creating List that contains elements that collide with the player1 at any given moment
        self.collisions1 = None
        # Creating List that contains elements in the collision between bombs(Of player1) and enemy
        self.collisions_bomb1 = None
        # Creating List that contains elements in the collision between bombs(Of player1) and blocks
        self.collisions_bomb_block1 = None
        # Creating List that contains elements in the collision bombs(Of player1) and the player
        self.collisions_bomb_player1 = None
        # Creating a Bool Variable to Check if a Player2 needs to be Blocked
        self.is_player2_blocked = False
        # Creating List that contains elements that collide with the player2 at any given moment
        self.collisions2 = None
        # Creating List that contains elements in the collision between bombs(Of player2) and enemy
        self.collisions_bomb2 = None
        # Creating List that contains elements in the collision between bombs(Of player2) and blocks
        self.collisions_bomb_block2 = None
        self.collisions_bomb_player2 = None

    def run(self):
        """Defines the Game State and calls its corresponding methods."""
        while self.is_running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_update()
                self.menu_draw()
            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            if self.state == 'gameover':
                self.gameover_events()
                self.gameover_update()
                self.gameover_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# ---------------------------- GENERAL FUNCTIONS -----------------------------------------

    def load_files(self):
        """Loads important images, audios and creates the list with background walls"""
        # Getting the Image Directory
        dir_images = os.path.join(os.getcwd(), 'images')
        # Getting the Audio Directory
        self.dir_audios = os.path.join(os.getcwd(), 'audios')
        # Loading the Menu Background
        self.menu_background = os.path.join(dir_images, MENU_BACKGROUND)
        self.menu_background = pygame.image.load(self.menu_background).convert()
        self.menu_background = pygame.transform.scale(self.menu_background,
                                                      (WIDTH, HEIGHT))
        # Loading the Playing Background
        self.playing_background = os.path.join(dir_images, SINGLE_BACKGROUND)
        self.playing_background = pygame.image.load(self.playing_background).convert()
        self.playing_background = pygame.transform.scale(self.playing_background,
                                                         (WIDTH, HEIGHT))
        # Loading the Game Over Background
        self.gameover_background = os.path.join(dir_images, GAME_OVER_BACKGROUND)
        self.gameover_background = pygame.image.load(self.gameover_background).convert()
        self.gameover_background = pygame.transform.scale(self.gameover_background,
                                                      (WIDTH, HEIGHT))
        # Creating list with the grid positions that have walls
        with open(os.path.join(os.getcwd(), 'walls.txt'), 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vector(x, y))

    def write_text(self, window, size, color, font_name, msg, position):
        """Generic method that writes messages in the window"""
        font = pygame.font.SysFont(font_name, size)
        text = font.render(msg, False, color)
        text_size = text.get_size()
        position[0] = position[0] - text_size[0]//2
        position[1] = position[1] - text_size[1]//2
        window.blit(text, position)

    def draw_grid(self):
        """Method to draw the grid in the map"""
        for x in range(X_CELLS):
            pygame.draw.line(self.window, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for y in range(Y_CELLS):
            pygame.draw.line(self.window, GREY, (0, y * self.cell_height),
                             (WIDTH, y * self.cell_height))

# ----------------------------- INTRO FUNCTIONS ------------------------------------------

    def menu_events(self):
        """Defines events that can happen in the menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_options -= 1
                    if self.menu_options < 0:
                        self.menu_options = 2
                if event.key == pygame.K_DOWN:
                    self.menu_options += 1
                    if self.menu_options > 2:
                        self.menu_options = 0
                if event.key == pygame.K_SPACE:
                    if self.menu_options == 0:
                        self.state = 'playing'
                    elif self.menu_options == 1:
                        self.state = 'playing'
                        self.multiplayer = True
                    elif self.menu_options == 2:
                        self.state = 'challenge'

    def menu_update(self):
        """Method that updates the state of the menu"""
        pass

    def menu_draw(self):
        """Draws elements that make the menu"""
        single_color = BLACK
        multi_color = BLACK
        challenge_color = BLACK
        # Changes color of selected option
        if self.menu_options == 0:
            single_color = WHITE
        elif self.menu_options == 1:
            multi_color = WHITE
        elif self.menu_options == 2:
            challenge_color = WHITE
        # Puts the background image
        self.window.blit(self.menu_background, (0, 0))
        # Writes the Options
        self.write_text(self.window, MENU_TEXT_SIZE, single_color,
                        MENU_TEXT_FONT, 'Single Player', [150, 230])
        self.write_text(self.window, MENU_TEXT_SIZE, multi_color,
                        MENU_TEXT_FONT, 'Multi Player', [150, 280])
        self.write_text(self.window, MENU_TEXT_SIZE, challenge_color,
                        MENU_TEXT_FONT, 'Challenge', [150, 330])
        pygame.display.update()

# ------------------------- Playing FUNCTIONS ---------------------------------------

    def playing_events(self):
        """Defines events that can happen during the playing"""

        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                self.is_running = False
            # Defines Player 1 Drop Bomb Key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player1.drop_bomb()
            # Defines Player 2 Drop Bomb Key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.player2.drop_bomb()
        # Defines Player 1 Movement
        if pygame.key.get_pressed()[pygame.K_w]:
            self.player1.move(vector(0, -1), 0)
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.player1.move(vector(0, 1), 2)
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.player1.move(vector(-1, 0), 3)
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.player1.move(vector(1, 0), 1)
        else:
            self.player1.move(vector(0, 0), 0)
        # Defines Player 2 Movement
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.player2.move(vector(0, -1), 0)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.player2.move(vector(0, 1), 2)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.player2.move(vector(-1, 0), 3)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.player2.move(vector(1, 0), 1)
        else:
            self.player2.move(vector(0, 0), 0)

        # Checks if Multiplayer was Chosen:
        if not self.multiplayer:
            if not self.player2.destroyed:
                self.player2.destroy()

        # Checks if Player1 has a banned direction and must be blocked
        self.is_player1_blocked = False
        for wall in self.walls:
            dist_x = abs((wall.x + 1/2) * self.cell_width - self.player1.pix_pos.x)
            dist_y = abs((wall.y + 1/2) * self.cell_height - (self.player1.pix_pos.y + 20))

            if dist_x < self.cell_width*3/5 and dist_y < self.cell_height*3/5:
                self.player1.ban_direction()
                self.player1.blocked = True
                self.is_player1_blocked = True

        if not self.is_player1_blocked:
            self.player1.blocked = False
            self.player1.banned_direction = vector(1, 1)

        # Checks if Player2 has a banned direction and must be blocked, if it is not destroyed
        if not self.player2.destroyed:
            self.is_player2_blocked = False
            for wall in self.walls:
                dist_x = abs((wall.x + 1 / 2) * self.cell_width - self.player2.pix_pos.x)
                dist_y = abs((wall.y + 1 / 2) * self.cell_height - (self.player2.pix_pos.y + 20))

                if dist_x < self.cell_width * 3 / 5 and dist_y < self.cell_height * 3 / 5:
                    self.player2.ban_direction()
                    self.player2.blocked = True
                    self.is_player2_blocked = True

            if not self.is_player2_blocked:
                self.player2.blocked = False
                self.player2.banned_direction = vector(1, 1)

    def playing_update(self):
        """Updates and Checks Conditions of Playing Game State"""
        # Checks if one of the player has died by a collision.
        if (not self.player1.destroyed and self.collisions1) or (not self.player2.destroyed and self.collisions2):
            if self.collisions1:
                self.all_sprites.remove(self.player1)
                self.player1.destroy()
                # If player 1 is destroyed and player 2 is already destroyed, the game ends.
                if self.player2.destroyed:
                    self.state = 'gameover'
            else:
                self.all_sprites.remove(self.player2)
                self.player2.destroy()
                # If player 2 is destroyed and player 1 is already destroyed, the game ends.
                if self.player1.destroyed:
                    self.state = 'gameover'
        else:
            # Updates Enemy,Blocks and Players
            self.enemy.update()
            for i in range(len(self.blocks)):
                self.blocks[i].update()
            self.player1.update()
            self.player2.update()
        # Checks if the enemy has collided with the bomb of player 1 or 2
        if self.collisions_bomb1 or self.collisions_bomb2:
            self.all_sprites.remove(self.enemy)
            self.enemy.destroy()
        # Checks if the player1 has collided with the bomb of player 1 or 2
        if self.collisions_bomb_player1:
            self.all_sprites.remove(self.player1)
            self.player1.destroy()
            # If player 1 is destroyed and player 2 is already destroyed, the game ends.
            if self.player2.destroyed:
                self.state = 'gameover'
        # Checks if the player2 has collided with the bomb of player 1 or 2
        if self.collisions_bomb_player2:
            self.all_sprites.remove(self.player2)
            self.player2.destroy()
            # If player 2 is destroyed and player 1 is already destroyed, the game ends.
            if self.player1.destroyed:
                self.state = 'gameover'

        # Checks collisions with Player1.
        self.collisions1 = pygame.sprite.spritecollide(self.player1, self.collision_sprites, False
                                                       , pygame.sprite.collide_mask)
        # Checks multiple collisions with Player1 Bomb when bomb is exploded.
        if self.player1.bomb.exploded:
            # Checks collisions between Enemy and Bomb1.
            self.collisions_bomb1 = pygame.sprite.spritecollide(self.player1.bomb, self.collision_sprites_bomb
                                                                , False, pygame.sprite.collide_mask)
            # Checks collisions between Player1 and Bomb1.
            self.collisions_bomb_player1 = pygame.sprite.spritecollide(self.player1, self.collision_sprites_bomb1_player
                                                                       , False, pygame.sprite.collide_mask)
            # Checks collisions between Player2 and Bomb1.
            self.collisions_bomb_player2 = pygame.sprite.spritecollide(self.player2, self.collision_sprites_bomb1_player
                                                                       , False, pygame.sprite.collide_mask)
            # Checks collisions between Blocks and Bomb1.
            self.collisions_bomb_block1 = pygame.sprite.spritecollide(self.player1.bomb,
                                                                      self.collision_sprites_bomb_block
                                                                      , False, pygame.sprite.collide_mask)

        # Checks collisions with Player2.
        self.collisions2 = pygame.sprite.spritecollide(self.player2, self.collision_sprites, False
                                                       , pygame.sprite.collide_mask)
        # Checks multiple collisions with Player2 Bomb.
        if self.player2.bomb.exploded:
            # Checks collisions between Enemy and Bomb2.
            self.collisions_bomb2 = pygame.sprite.spritecollide(self.player2.bomb, self.collision_sprites_bomb
                                                                , False, pygame.sprite.collide_mask)
            # Checks collisions between Player1 and Bomb2.
            self.collisions_bomb_player1 = pygame.sprite.spritecollide(self.player1, self.collision_sprites_bomb2_player
                                                                       , False, pygame.sprite.collide_mask)
            # Checks collisions between Player2 and Bomb2.
            self.collisions_bomb_player2 = pygame.sprite.spritecollide(self.player2, self.collision_sprites_bomb2_player
                                                                       , False, pygame.sprite.collide_mask)
            # Checks collisions between Blocks and Bomb2.
            self.collisions_bomb_block2 = pygame.sprite.spritecollide(self.player2.bomb,
                                                                      self.collision_sprites_bomb_block,
                                                                      False, pygame.sprite.collide_mask)
        # print(self.collisions1)
        # print(self.collisions2)
        # print(self.collisions_bomb1)
        print(self.collisions_bomb_block1)
        print(self.clock.get_fps())

    def playing_draw(self):
        """Drawing elements and sprites"""
        # Draws background
        self.window.blit(self.playing_background, (0, 0))
        self.draw_grid()
        # Draws Player Elements(Bomb)
        self.player1.draw()
        self.player2.draw()
        # Draws All Sprites used
        self.all_sprites.draw(self.window)
        pygame.display.update()

# ---------------------------- GAME OVER FUNCTIONS ---------------------------------------

    def gameover_events(self):
        """Defines events that happens during Gameover"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                self.is_running = False

        pass

    def gameover_update(self):
        """Updates elements in GameOver State"""
        pass

    def gameover_draw(self):
        """Draws Elements in the Window"""
        # Draws Background
        self.window.blit(self.gameover_background, (0, 0))
        # Write GameOver text
        self.write_text(self.window, MENU_TEXT_SIZE, WHITE,
                        MENU_TEXT_FONT, 'PRESS ANY KEY TO QUIT', [400, 170])
        pygame.display.update()
