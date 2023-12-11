import random

import pygame.display

from clicks import *
from player import *
from sprite_group import *


class Manager:
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.screen_size)
        pygame.display.set_caption(Settings.name)

        self.game = False
        self.vic = False
        self.level = 0
        self.click_play = ClickPlay()
        self.click_next = ClickNext()
        self.victory = Victory()
        self.player = Player()
        self.group_invaders = MyGroupI()
        self.group_p_shots = MyGroup()
        self.group_i_shots = MyGroup()
        self.group_p_lives = MyGroup()
        self.group_blocks = MyGroup()

        self.invaders_dir = 1
        self.invaders_h = 0

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            self.care_screen()
            self.care_events()
            if self.game:
                self.running()
            pygame.display.update()
            pygame.display.flip()
            clock.tick(160)

    def care_screen(self):
        self.screen.fill('Black')
        self.screen.blit(self.player.player_surf, self.player.rect)
        if not self.game:
            if not self.vic:
                self.screen.blit(self.click_play.text, self.click_play.rect)
            if self.vic:
                self.screen.blit(self.click_next.text, self.click_next.rect)
                self.screen.blit(self.victory.text, self.victory.rect)

    def care_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_over_click(event.pos) and not self.game:
                self.init_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game:
                self.player.p_shot = True

    def mouse_over_click(self, pos):
        if not self.vic:
            return self.click_play.rect.collidepoint(pos)
        if self.vic:
            return self.click_next.rect.collidepoint(pos)

    def form_invaders(self):
        for r in range(Settings.alien_rows):
            for c in range(Settings.alien_columns):
                self.group_invaders.add(form_inv(r, c))
        for inv in self.group_invaders:
            inv.lives = inv.lives + 3 * self.level

    def form_p_lives(self):
        for i in range(3):
            self.group_p_lives.add(form_b(Settings.p_lives_size,
                                          (Settings.x_l + 25 * i, Settings.y_l),
                                          Settings.p_lives_color))

    def create_blocks(self):
        for b in range(4):
            for i in range(15):
                for j in range(3):
                    self.group_blocks.add(form_b(p=(100 + 175 * b + 5 * i, 280 - 5 * j)))

    def create_objects(self):
        self.form_invaders()
        self.form_p_lives()
        self.create_blocks()

    def init_game(self):
        lev = self.level
        self.__init__()
        self.game = True
        self.level = lev
        self.create_objects()

    def running(self):
        self.care_keys()
        self.group_invaders.draw(self.screen)
        self.group_p_lives.draw(self.screen)
        self.group_p_shots.draw(self.screen)
        self.group_i_shots.draw(self.screen)
        self.group_blocks.draw(self.screen)
        self.shots_inv()
        self.care_shots()
        self.care_invaders_dir_h()
        self.group_invaders.update(self.invaders_dir, self.invaders_h)
        self.invaders_h = 0
        self.group_p_shots.update()
        self.group_i_shots.update()
        if self.end_game():
            self.game = False

    def care_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('Left')
        if keys[pygame.K_RIGHT]:
            self.player.move('Right')
        if keys[pygame.K_SPACE] and self.player.p_shot:
            self.group_p_shots.add(self.player.shot())
            self.player.p_shot = False

    def shots_inv(self):
        if len(self.group_i_shots) < 3:
            if self.group_invaders:
                rand_inv = random.choice(self.group_invaders.sprites())
                self.group_i_shots.add(rand_inv.shot_inv())

    def care_shots(self):
        self.c_p_shots()
        self.c_i_shots()
        self.c_blocks()

    def c_blocks(self):
        for block in self.group_blocks:
            for shot in self.group_p_shots:
                if block.rect.colliderect(shot.rect):
                    block.kill()
                    shot.kill()
            for i_shot in self.group_i_shots:
                if block.rect.colliderect(i_shot.rect):
                    block.kill()
                    i_shot.kill()

    def c_p_shots(self):
        for p_shot in self.group_p_shots:
            if p_shot.rect.top < 0:
                p_shot.kill()
            for inv in self.group_invaders:
                if inv.rect.colliderect(p_shot.rect):
                    p_shot.kill()
                    inv.lives -= 1
            for i_shot in self.group_i_shots:
                if i_shot.rect.colliderect(p_shot.rect):
                    p_shot.kill()
                    i_shot.kill()

    def c_i_shots(self):
        for i_shot in self.group_i_shots:
            if i_shot.rect.bottom > Settings.height:
                i_shot.kill()
            if i_shot.rect.colliderect(self.player.rect):
                i_shot.kill()
                self.player.lives -= 1
                self.group_p_lives.sprites()[0].kill()

    def care_invaders_dir_h(self):
        self.c_i()
        self.c_i_d()
        self.c_i_h()

    def c_i(self):
        for inv in self.group_invaders:
            if inv.lives < 1:
                inv.kill()

    def c_i_d(self):
        for inv in self.group_invaders:
            if inv.rect.left < 0:
                self.invaders_h = 3
                self.invaders_dir = 1

    def c_i_h(self):
        for inv in self.group_invaders:
            if inv.rect.right > Settings.width:
                self.invaders_h = 3
                self.invaders_dir = - 1

    def end_game(self):
        if not self.group_invaders:
            self.vic = True
            self.level += 1
        elif (self.player.lives < 1
                or self.group_invaders.sprites()[- 1].rect.bottom > Settings.height // 2):
            self.vic = False
            self.level = 0
        return ((len(self.group_invaders) == 0 or self.player.lives < 1)
                or (self.group_invaders.sprites()[- 1].rect.bottom > Settings.height // 2))
