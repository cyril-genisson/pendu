import pygame as pg
import parameters as prm
from menu import Menu


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.game_stop = False
        self.game_menu = Menu()
        self.font = pg.font.SysFont("arialblack", 40)

    def draw_text(self, text, font, text_color,  x, y):
        img = self.font.render(text, True, text_color)
        prm.SCREEN.blit(img, (x, y))
        msg_width, msg_height = img.get_size()
        if x + msg_width > prm.DSP_WIDTH:
            end_width = x + msg_width - prm.DSP_WIDTH
            end_rect = pg.Rect(msg_width - end_width, 0, end_width, msg_height)
            end_msg = img.subsurface(end_rect)
            prm.SCREEN.blit(end_msg, (0, y))
        return

    def start(self):
        sound = pg.mixer.Sound("music/death.mp3")
        pg.mixer.Sound.play(sound, loops=-1)
        bg = pg.image.load("images/background.jpg")
        bg = pg.transform.scale(bg, (prm.DSP_WIDTH, prm.DSP_HEIGHT))
        bg.convert(prm.SCREEN)
        prm.SCREEN.blit(bg, (0, 0))
        self.draw_text("Press Space to begin", True, prm.GREEN, prm.DSP_WIDTH * 0.20, prm.DSP_HEIGHT * 0.75)
        runner = True
        self.game_menu.main_menu.disable()
        pos_x = prm.DSP_WIDTH * 0.20
        while runner:
            self.clock.tick(prm.FPS)
            prm.SCREEN.blit(bg, (0, 0))
            self.draw_text("Press Space to begin", True, prm.GREEN, pos_x, prm.DSP_HEIGHT * 0.75)
            pos_x = (pos_x + 0.75) % prm.DSP_WIDTH

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if self.game_menu.main_menu.is_enabled():
                            self.game_menu.main_menu.disable()

                            pg.mixer.Sound.play(sound)
                            prm.SCREEN.blit(bg, (0, 0))
                        else:
                            self.game_menu.main_menu.enable()
                            pg.mixer.Sound.stop(sound)
                            pg.mixer.Sound.play(self.game_menu.menu_sound, loops=-1)
                            self.game_menu.main_menu.update(events)
            if self.game_menu.main_menu.is_enabled():
                self.game_menu.main_menu.update(events)
                prm.SCREEN.blit(bg, (0, 0))
                if self.game_menu.main_menu.mainloop(prm.SCREEN):
                    pg.mixer.Sound.stop(self.game_menu.menu_sound)
                    pg.mixer.Sound.play(sound)
                    prm.SCREEN.blit(bg, (0, 0))
            pg.display.update()
        pg.quit()


def main():
    pg.init()
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
