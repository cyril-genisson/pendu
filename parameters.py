import pygame as pg
#
# ABOUT
#
ABOUT = [f'HANGMAN',
         f'Version: 0.1',
         f'Author: Cyril GENISSON',
         f'Thanks for all inspiration found',
         f'on Github',
         ]
#
# DICTIONARY FILE
#
FILE = 'wordlist.10000.txt'

#
# COLORS
#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#
# IMAGES PARAMETERS
#
HANGMAN_IMAGES = ['images/hangman0.png', 'images/hangman1.png', 'images/hangman2.png',
                  'images/hangman3.png', 'images/hangman4.png', 'images/hangman5.png',
                  'images/hangman6.png']

#
# DISPLAY
#

DSP_WIDTH = 800
DSP_HEIGHT = 640
FPS = 60
SCREEN = pg.display.set_mode((DSP_WIDTH, DSP_HEIGHT), 0, 0, 0, 0)
pg.display.set_caption("Hangman")
ico = pg.image.load('images/hangman.png')
pg.display.set_icon(ico)

#
# MENU'S PARAMETERS
#
MENU_WIDTH = DSP_WIDTH * 1
MENU_HEIGHT = DSP_HEIGHT * 1
DIFFICULTY = 1
