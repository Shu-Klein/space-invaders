import pygame
from settings import Settings
from sprite_group import Bullet


class Player:
    def __init__(self):
        self.lives = 3
        self.player_surf = pygame.image.load(Settings.player_surf).convert_alpha()
        self.rect = self.player_surf.get_rect(midbottom=Settings.player_pos)
        self.p_shot = False

    def move(self, l_or_r):
        left = self.rect.left
        right = self.rect.right
        if l_or_r == 'Left' and left > 0:
            self.rect.move_ip(- 1, 0)
        if l_or_r == 'Right' and right < Settings.width:
            self.rect.move_ip(1, 0)

    def shot(self):
        return Bullet(self.rect.midtop)
