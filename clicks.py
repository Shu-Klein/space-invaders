import pygame
import pygame.font
from settings import Settings


class Click:
    def __init__(self, text, color):
        pygame.font.init()
        def_font = pygame.font.get_default_font()
        self.click_play = pygame.font.SysFont(def_font, 50)
        self.text_click = text
        self.text = self.click_play.render(self.text_click, True, color)
        self.rect = self.text.get_rect()


class ClickPlay(Click):
    def __init__(self):
        super().__init__(text='Play', color='Blue')
        self.rect.center = (Settings.width // 2, Settings.height // 3)


class ClickNext(Click):
    def __init__(self):
        super().__init__(text='Next Level', color='Blue')
        self.rect.center = (Settings.width // 2, Settings.height // 3)


class Victory(Click):
    def __init__(self):
        super().__init__(text='Victory', color='Orange')
        self.rect.center = (Settings.width // 2, Settings.height // 2)
