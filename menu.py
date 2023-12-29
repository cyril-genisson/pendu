import pygame as pg
import pygame_menu as pgm
from hangman import Hangman
import parameters as prm


class Menu(object):
    def __init__(self):
        self.width = prm.MENU_WIDTH
        self.height = prm.MENU_HEIGHT
        self.difficulty = prm.DIFFICULTY
        self.score = {}
        self.user = 'Devil My Cry'
        self.game_stop = False
        self.menu_sound = pg.mixer.Sound("music/ghosts.mp3")

        self.menu_theme = pgm.themes.THEME_DARK.copy()
        self.menu_theme.title_background_color = (10, 10, 10, 10)
        self.menu_theme.background_color = (0, 0, 0, 10)
        self.menu_theme.title_font_color = (0, 255, 0)
        self.menu_theme.title_font_size = 40
        self.menu_theme.text_font_size = 30
        self.menu_theme.text_color = prm.RED
        self.menu_theme.text_color = (0, 255, 255)
        self.menu_theme.text_font_color = (0, 255, 0)
        self.menu_theme.title_close_button = True
        self.menu_theme.text_align = 'center'

        self.word_menu = pgm.Menu("Words", self.width, self.height, True, theme=self.menu_theme)
        self.word_menu.add.text_input('Enter a word: ', default="NewWord", maxchar=30, font='Arial',
                                      textinput_id='word')
        self.word_menu.add.vertical_margin(30)
        self.word_menu.add.button('Save new word', self.add_word, button_id='save_word')
        self.word_menu.add.vertical_margin(30)
        self.word_menu.add.button('Return to menu', pgm.events.BACK)

        self.score_menu = pgm.Menu("Score", self.width, self.height, True, theme=self.menu_theme)
        self.score_menu.add.button('Return to menu', pgm.events.BACK)

        self.about_menu = pgm.Menu('About', self.width, self.height, True, theme=self.menu_theme)
        for m in prm.ABOUT:
            self.about_menu.add.label(m, align=pgm.locals.ALIGN_CENTER, font_size=40, font_color=prm.GREEN)
        self.about_menu.add.vertical_margin(30)
        self.about_menu.add.button('Return to menu', pgm.events.BACK)

        self.main_menu = pgm.Menu("Hangman", self.width, self.height, True,
                                  theme=self.menu_theme)
        self.main_menu.add.text_input('User: ', default="John Doe", maxchar=20, font='arial', textinput_id='user')
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.selector('Difficulty: ', [('Easy', 1), ('Medium', 2), ('Hard', 3)])
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('Play', self.play_game)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('Add word in list', self.word_menu)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('High score', self.score_menu)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('About',  self.about_menu)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('Quit', self.quit)

    def play_game(self):
        """
        Plays game
        :return:
        """
        data = self.main_menu.get_input_data()
        for k in data.keys():
            if k == 'user':
                self.user = data[k]
            else:
                self.difficulty = data[k][0][1]
        game = Hangman(difficulty=self.difficulty, user=self.user)
        self.main_menu.disable()
        self.game_stop = False
        pg.mixer.Sound.stop(self.menu_sound)
        while not self.game_stop:
            if not game.play():
                self.game_stop = True
                pg.mixer.Sound.stop(game.suspense)
        self.main_menu.enable()
        pg.mixer.Sound.play(self.menu_sound, loops=-1)

    def add_word(self):
        """
        Adds word to
        :return:
        """
        with open('words.txt', 'a') as f:
            data = self.word_menu.get_input_data()
            for k in data.keys():
                f.write(data[k].upper() + '\n')
                font = pg.font.SysFont("ArialBlack", 40)
                text = font.render(f"{data[k]} was add!", True, prm.GREEN)
                text_width, text_height = text.get_size()
                prm.SCREEN.blit(text, (prm.MENU_WIDTH / 2 - text_width / 2, prm.MENU_HEIGHT * 0.75 + text_height / 2))
                pg.display.update()
                pg.time.delay(1500)

    def quit(self):
        """
        Quits the game
        :return:
        """
        self.main_menu.disable()
        return True
