import pygame
vector = pygame.math.Vector2
# Screen Constants

WIDTH = 800
HEIGHT = 455
WINDOW_TITLE = 'BombITA'
FPS = 60

MENU_BACKGROUND = 'menu_background.png'
SINGLE_BACKGROUND = 'single_background.png'
GAME_OVER_BACKGROUND = 'game_over_background.png'

MENU_TEXT_SIZE = 35
MENU_TEXT_FONT = 'comicsansms'

X_CELLS = 17
Y_CELLS = 13

# Color Constants

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)
RED = (255, 0, 0)

# Player Constants
PLAYER_START_POS = vector(2, 1)

# Game Constants
BLOCKS_NUMBER = 10

# Enemy Constants

ENEMY_START_POS = vector(6, 6)
