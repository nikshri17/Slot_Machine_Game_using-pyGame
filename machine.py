from debug import debug
from reel import *
from player import Player
from settings import *
from ui import UI
from wins import *
import pygame

class Machine:
    def __init__(self) :
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        # RESULTS
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

        # import sounds
        self.spin_sound = pygame.mixer.Sound('audio/mixkit-winning-an-extra-bonus-2060.wav')
        self.spin_sound.set_volume(0.15)
        self.win_three = pygame.mixer.Sound('audio/mixkit-magical-coin-win-1936.wav')
        self.win_three.set_volume(10)
        self.win_four =  pygame.mixer.Sound('audio/mixkit-melodic-gold-price-2000.wav')
        self.win_four.set_volume(20)
        self.win_five = pygame.mixer.Sound('audio/mixkit-melodic-bonus-collect-1938.wav')
        self.win_five.set_volume(20)

# This method is used to control the cooldown or waiting period before allowing the player to spin again in a game
    def coolsdowns(self):
        
        for reel in self.reel_list:
            # This means that if any reel is currently spinning, the player is not allowed to toggle spinning, and the game is in a spinning state.
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True
        # it further checks if self.can_toggle is False and if the count of False values in the list is is equal to 5. 
        # This implies that all 5 reels are not spinning.
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True #This means that the cooldown period is over, and the player can toggle spinning again.
            # print(self.get_result())
            # print(flip_horizontal(self.get_result()))
            self.spin_result = self.get_result()

            
            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                # play the win sound
                self.play_win_sound(self.win_data)
                self.pay_player(self.win_data, self.currPlayer)
                # print(self.currPlayer.get_data())
                # L43 & L44 # related to the visual presentation of the win animation.
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)


    def input(self):
        keys = pygame.key.get_pressed() #retrieves current state of all keyboard keys

        #checks for space key, ability to toggle spin, and balance to cover bet size
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            # Line54 indicating whether the game is currently spinning or not.
            self.toggle_spinning() #TOGGLE means -> switch or change the state |  
            self.spin_time = pygame.time.get_ticks() #records the current time and keep track of when the spinning started.
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            # print(self.currPlayer.get_data())
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -150
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (150 + X_OFFSET), y_topleft
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft)) #Need to create reel class
            self.reel_index += 1

#toggle_spinning method is called when the space key is pressed,
#If self.can_toggle is True, it sets the spin_time to the current time.
#It toggles the state of the spinning variable from True to False
#sets self.can_toggle to False
#It iterates through a list of reel_list and calls the start_spin method on each reel, 
#  potentially with varying time delays.
    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks() #current time
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in  self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.spin_sound.play()
                self.win_animation_ongoing = False

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result
    
    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in  horizontal:
            for sym in  row:
                if row.count(sym) > 2: #POtential win
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
    # check possible_win for a subsequence longer than 2 and add to hits
                    if len(longest_seq(possible_win)) > 2:
                        # index() method to find the index of row in the horizontal list, and then you add 1 to it (i.e. 0th index).
                        # This index is where the new value will be inserted.
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits
            
    def pay_player(self, win_data, curr_player):
        multiplier = 0
        spin_payout = 0
        for v in win_data.values():
            multiplier += len(v[1]) #len(v) returns the number of elements in a list 
            # print("length is", v)
            spin_payout = (multiplier * curr_player.bet_size)
            curr_player.balance += spin_payout
            self.machine_balance -= spin_payout
            curr_player.last_payout = spin_payout
            curr_player.total_won += spin_payout
            # print("spinning",spin_payout)
    def play_win_sound(self, win_data):
        sum = 0
        for item in win_data.values():
            sum += len(item[1])
        if sum == 3: self.win_three.play()
        elif sum == 4: self.win_four.play()
        elif sum > 4: self.win_five.play()
    
    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in =  True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True  

    def update(self, delta_time):
        self.coolsdowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()