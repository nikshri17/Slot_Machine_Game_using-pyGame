from settings import *
import pygame, random

class Reel:
    def __init__(self, pos): #position
        self.symbol_list = pygame.sprite.Group() #sprites -> game objects or images diaplayed
        #using sprite groups, we can efficiently update and draw multiple sprites / managing sprites
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] #slicing used from index 0 to 4, only matters when there are more than 5 symbols 
        # replaces the original list with a new list containing only the first 5 elements.
        self.reel_is_spinning = False

        #Sounds

        for idx, item in enumerate(self.shuffled_keys): #enumerate- iteration 
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos) #converting pos(tuple) into list bcz list are mutable
            pos[1] += 150 #index 1 item increment by 300 w.r.t pos of Y
            pos = tuple(pos) #again converted into tuple which is immutable
    def animate(self, delta_time): #adding delay to when reel spin
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            #stagger reel spin start animation
            # staggered means -> arrange so that they do not occur at the same time
            if self.delay_time <= 0:
                #Iterate through all 5 symbols in reel; truncate; add new random symbol on top of stack
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 50
                    
                    #correct spacing is dependent on above addition eventually hitting 1200
                    if symbol.rect.top == 600: #symbol reaching the bottom of the reel.
                        if reel_is_stopping:
                            self.reel_is_spinning = False #if the symbol has reached the bottom of the reel, and the reel is stopping

                        symbol_idx = symbol.idx
                        symbol.kill() #removing the current symbol
                        #spawn random symbol in place of above
                        #it is selecting a random symbol from a collection of symbols. 
                        #It does so by generating a list of keys from a dictionary called self.shuffled_keys 
                        #and then using random.choice() to pick a random key.
                        #This key is used to access the corresponding symbol from the symbols collection. 
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -150), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        #get & return text representation of symbols in a given reel
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1] #-1, means that the list is iterated in reverse order.
     




class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__() #calls the constructor of the parent class (pygame.sprite.Sprite) to properly initialize the sprite.

        #friendly name for path to file
        self.sym_type = pathToFile.split('/')[3].split('.')[0] #It splits the path using / as a delimiter, takes the 4th part (index 3), and then further splits it using '.' as a delimiter to get the part before the file extension   
        
        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha() #convert_alpha() method is used to optimize the image for faster blitting(copying/overlaying image in screen) in Pygame.
        self.rect = self.image.get_rect(topleft = pos) #rectangle that represents the image's position
        self.x_val = self.rect.left 

        # used for WIN ANIMATION
        self.size_x = 150
        self.size_y = 150
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # slightly increases size of winning symbols
        if self.fade_in:
            if self.size_x < 160:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

            # fades out non-winning symbols
        elif not self.fade_in and self.fade_out:
            if self.alpha > 80:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)