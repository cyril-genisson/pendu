import pygame as pg
import parameters as prm
from button import Button
import random


class Hangman:
    def __init__(self, difficulty, user):
        pg.init()
        self.difficulty = difficulty
        self.user = user
        self.status = 0
        self.game = True
        self.score_font = pg.font.SysFont("arialblack", 20)
        self.text = pg.font.SysFont('arialblack', 22)
        self.font = pg.font.SysFont("arialblack", 40)
        self.word_list = []
        self.open_file()
        self.alpha_bottoms = []
        self.SCREEN = pg.display.set_mode((prm.DSP_WIDTH, prm.DSP_HEIGHT), 0, 0, 0, 0)
        self.organs = pg.mixer.Sound("music/organs.mp3")
        self.suspense = pg.mixer.Sound("music/suspense.mp3")

        #  Game settings
        self.SCREENWIDTH = prm.DSP_WIDTH
        self.SCREENHEIGHT = prm.DSP_HEIGHT

        #  Game Variables and load functions
        self.number_of_guesses = self.difficulty - 1
        self.chosen_word = self.select_random_word().upper()
        self.guess_word = [' ' for _ in self.chosen_word]
        self.create_alphabet()
        print(self.chosen_word)
        self.mouse_click = False
        self.game_over = False
        self.win_streak = 0

    def play(self):
        pg.mixer.Sound.play(self.suspense, loops=-1)
        run = True
        while run:
            prm.SCREEN.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_click = True

                    for item in self.alpha_bottoms:
                        if item.imageRect.collidepoint(event.pos):
                            if item.letter in self.chosen_word:
                                for index, let in enumerate(self.chosen_word):
                                    if item.letter == let:
                                        self.guess_word[index] = item.letter
                            elif item.letter not in self.chosen_word and item.active:
                                self.number_of_guesses += 1
                            item.active = False

                elif event.type == pg.MOUSEBUTTONUP:
                    self.mouse_click = False

            self.draw_letter_lines(self.chosen_word)
            self.draw_alpha(self.alpha_bottoms)
            self.draw_hangman(self.number_of_guesses)

            for alpha_b in self.alpha_bottoms:
                if alpha_b.imageRect.collidepoint(pg.mouse.get_pos()):
                    alpha_b.mouse_high_light(prm.SCREEN)

            pg.display.update()

            if ''.join(self.guess_word) == self.chosen_word or self.number_of_guesses == 6:
                self.game_over = True
                self.end_game()

    def open_file(self):
        with open('easyWordList.txt', 'r') as file:
            content = file.readlines()
            new_list = []
            for item_list in content:
                new_list.append(item_list.split(','))

            for wordList in new_list:
                for word in wordList:
                    if not len(word.strip()) < 3 and len(word.strip()) <= 10:
                        self.word_list.append(word.strip())

    def select_random_word(self):
        return random.choice(self.word_list)

    def draw_letters(self, letter):
        print_text = self.text.render(letter, True, prm.GREEN)
        return print_text

    def draw_letter_lines(self, word):
        word_len_x = len(word) * (25 + 15)

        start_xy = [prm.DSP_WIDTH - 50 - word_len_x, 350]
        length_xy = [25, 0]
        spacing = [15, 0]

        for k, letter in enumerate(word):
            pg.draw.line(prm.SCREEN, prm.GREEN, (start_xy[0], start_xy[1]),
                         (start_xy[0] + length_xy[0], start_xy[1] + length_xy[1]), 3)
            prm.SCREEN.blit(self.draw_letters(self.guess_word[k]), (start_xy[0] + 10, 320))
            start_xy[0] = start_xy[0] + length_xy[0] + spacing[0]
            start_xy[1] = start_xy[1] + length_xy[1] + spacing[1]

    def create_alphabet(self):
        alphabet = [chr(k) for k in range(ord('A'), ord('Z') + 1)]
        x_pos = 100
        y_pos = 500
        let_num = 0
        for num in [9, 9, 8]:
            for _ in range(num):
                self.alpha_bottoms.append(Button((x_pos, y_pos), self.draw_letters(alphabet[let_num]),
                                                 alphabet[let_num]))
                let_num += 1
                x_pos += 50
            x_pos = 100
            y_pos += 40

    def draw_alpha(self, item_list):
        for k in item_list:
            k.draw(prm.SCREEN)

        prm.SCREEN.blit(self.draw_letters(f'Winning Streak : {str(self.win_streak)}'), (prm.DSP_WIDTH - 300, 100))

    def end_game(self):
        bg_1 = pg.image.load("images/background_1.jpg")
        bg_1 = pg.transform.scale(bg_1, (prm.DSP_WIDTH, prm.DSP_HEIGHT))
        bg_1.convert(prm.SCREEN)
        prm.SCREEN.blit(bg_1, (0, 0))
        pg.mixer.Sound.stop(self.suspense)
        pg.mixer.Sound.play(self.organs, loops=-1)

        if ''.join(self.guess_word) == self.chosen_word:
            self.win_streak += 1

        while self.game_over:
            self.alpha_bottoms.clear()
            message = self.draw_letters('Move on or die!')
            prm.SCREEN.blit(message, (prm.DSP_WIDTH // 2 - message.get_width() // 2, prm.DSP_HEIGHT * 3 // 4 - 30))

            if ''.join(self.guess_word) == self.chosen_word:
                message = self.draw_letters(f'Your are saved! You guessed {self.chosen_word}!')
                prm.SCREEN.blit(message, (prm.DSP_WIDTH // 2 - message.get_width() // 2, prm.DSP_HEIGHT // 2))
            elif self.number_of_guesses == 6:
                message = self.draw_letters(f'You are died! The word was {self.chosen_word}!')
                prm.SCREEN.blit(message, (prm.DSP_WIDTH // 2 - message.get_width() // 2, prm.DSP_HEIGHT // 2))
                self.win_streak = 0

            pg.display.update()

            for _ in pg.event.get():
                if _.type == pg.MOUSEBUTTONDOWN:
                    self.number_of_guesses = self.difficulty - 1
                    self.chosen_word = self.select_random_word().upper()
                    self.guess_word = [' ' for _ in self.chosen_word]
                    self.create_alphabet()
                    print(self.chosen_word)
                    self.game_over = False
                    pg.mixer.Sound.stop(self.organs)
                    pg.mixer.Sound.play(self.suspense, loops=-1)
                if _.type == pg.KEYDOWN:
                    if _.key == pg.K_ESCAPE or _.key == pg.K_ESCAPE:
                        pg.mixer.Sound.stop(self.organs)
                        pg.quit()
                if _.type == pg.QUIT:
                    pg.mixer.Sound.stop(self.organs)
                    pg.quit()

    @staticmethod
    def draw_gallows():
        pg.draw.line(prm.SCREEN, prm.GREEN, (100, 400), (275, 400), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (125, 400), (125, 50), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (125, 50), (275, 50), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (125, 100), (175, 50), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (275, 50), (275, 125), 3)

    @staticmethod
    def draw_head():
        pg.draw.circle(prm.SCREEN, prm.GREEN, (275, 150), 25, 3)

    @staticmethod
    def draw_body():
        pg.draw.line(prm.SCREEN, prm.GREEN, (275, 175), (275, 225), 3)

    @staticmethod
    def draw_left_arm():
        pg.draw.line(prm.SCREEN, prm.GREEN, (275, 185), (245, 215), 3)

    @staticmethod
    def draw_right_arm():
        pg.draw.line(prm.SCREEN, prm.GREEN, (275, 185), (305, 215), 3)

    @staticmethod
    def draw_left_leg():
        pg.draw.line(prm.SCREEN, prm.GREEN, (275, 225), (250, 250), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (250, 250), (250, 275), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (250, 275), (240, 275), 3)

    @staticmethod
    def draw_right_leg():
        pg.draw.line(prm.SCREEN, prm.GREEN, (275, 225), (300, 250), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (300, 250), (300, 275), 3)
        pg.draw.line(prm.SCREEN, prm.GREEN, (300, 275), (310, 275), 3)

    def draw_hangman(self, nbr_guesses):
        if nbr_guesses >= 0:
            self.draw_gallows()
        if nbr_guesses >= 1:
            self.draw_head()
        if nbr_guesses >= 2:
            self.draw_body()
        if nbr_guesses >= 3:
            self.draw_left_arm()
        if nbr_guesses >= 4:
            self.draw_right_arm()
        if nbr_guesses >= 5:
            self.draw_left_leg()
        if nbr_guesses >= 6:
            self.draw_right_leg()
