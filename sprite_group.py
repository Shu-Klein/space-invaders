import pygame
from pygame import image
from pygame.sprite import Sprite, Group

from settings import Settings


def form_inv(c, r):
    return Invader(invader_pos=(100 + 50 * r, 25 + 30 * c))


def form_b(size=Settings.b_s, p=Settings.b_p, c=Settings.blocks_color):
    return Block(size, p, c)


class Invader(Sprite):
    def __init__(self, invader_pos=(0, 0)):
        super().__init__()
        self.lives = 1
        self.image = image.load(Settings.alien_surf).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.alien_size)
        self.rect = self.image.get_rect(topleft=invader_pos)

    def update(self, inv_dir, h):
        self.rect.x += inv_dir
        self.rect.y += h

    def shot_inv(self):
        return BullInv(pos=self.rect.midbottom)


class Bullet(Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface(Settings.bullet_size)
        self.image.fill(Settings.bullet_color)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.move_ip(0, - 1)


class BullInv(Bullet):
    def __init__(self, pos):
        super().__init__(pos=pos)
        self.image = pygame.Surface(Settings.bullet_i_size)
        self.image.fill(Settings.bull_inv_color)

    def update(self):
        self.rect.move_ip(0, 1)


class MyGroup(Group):
    def __init__(self):
        super().__init__()


class MyGroupI(MyGroup):
    def __init__(self, direction=1, height=0):
        super().__init__()
        self.direction = direction
        self.height = height


class Block(Sprite):
    def __init__(self, size, pos, color):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
