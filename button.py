import parameters as prm
import pygame as pg


class Button:
    def __init__(self, position, image, letter):
        self.position = position
        self.letter = letter
        self.image = image
        self.imageRect = pg.Rect(self.position[0] - 5, self.position[1], 30, 30)
        self.active = True

    def mouse_high_light(self, window):
        pg.draw.rect(window, prm.RED,
                     [self.imageRect[0], self.imageRect[1], self.imageRect[2], self.imageRect[3]])
        window.blit(self.image, self.position)
        pg.draw.rect(window, prm.RED,
                     [self.imageRect[0], self.imageRect[1], self.imageRect[2], self.imageRect[3]], 1)

    def draw(self, window):
        if self.active:
            window.blit(self.image, self.position)
            pg.draw.rect(window, prm.GREEN,
                         [self.imageRect[0], self.imageRect[1], self.imageRect[2], self.imageRect[3]], 1)
        else:
            self.mouse_high_light(window)
