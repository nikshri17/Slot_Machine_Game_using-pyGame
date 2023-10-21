from player import Player
from settings import *
import pygame, random

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        # self.win_text_angle = random.randint(-3,1)
        
    def display_info(self):
        player_data = self.player.get_data()

        # balance and bet size
        balance_surf = self.font.render("Balance: Rs " + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 10, self.display_surface.get_size()[1] - 13 #get_size() retrieves the width & height AND [1] is about 1st index element i.e height
        balance_rect = balance_surf.get_rect(bottomleft = (x, y))

        bet_surf = self.bet_font.render("Wager: Rs " + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 10
        bet_rect = bet_surf.get_rect(bottomright = (x, y))

        # Draw player data
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)

        # print last win if applicable
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! Rs " + last_payout, True, TEXT_COLOR, None)
            x1 = 400
            y1 = self.display_surface.get_size()[1] - 20
            # win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center = (x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 450, 800, 50))
        self.display_info()