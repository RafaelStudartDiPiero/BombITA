import pygame
vector = pygame.math.Vector2

# Screen Constants
WIDTH = 800
HEIGHT = 455
WINDOW_TITLE = 'BombITA'
FPS = 60

# Images Filenames
MENU_BACKGROUND = 'menu_background.png'
SINGLE_BACKGROUND = 'single_background.png'
GAME_OVER_BACKGROUND = 'game_over_background.png'

# Text Parameters
MENU_TEXT_SIZE = 35
MENU_TEXT_FONT = 'comicsansms'

# Map Parameters
X_CELLS = 17
Y_CELLS = 13

# Color Constants

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)
RED = (255, 0, 0)

# Player Constants
PLAYER1_START_POS = vector(2, 1)
PLAYER2_START_POS = vector(14, 10)

# Blocks Constants
BLOCKS_NUMBER = 20

# Enemy Constants

ENEMY_START_POS = vector(6, 6)
