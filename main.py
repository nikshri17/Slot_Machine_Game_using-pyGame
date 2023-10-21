from machine import Machine
from settings import *
import pygame, sys

class Game:
    def __init__(self):

        #normal setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # FOR SETTING CAPTION/DISPLAYING NAME
        pygame.display.set_caption('Slot Machine')
        #used to keep track of time
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        
        #creating machine class
        self.machine = Machine()
        self.delta_time = 0

        # Sounds
        # main_sound = pygame.mixer.Sound('audio/audio_track.mp3')
        # main_sound.play(loops = -1) #for endless looping of song

    def run(self):
        self.start_time = pygame.time.get_ticks() #current time is captured by get_ticks() and assigned to self.start_time
     
        while True:
            #Handling Quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() #uninitializing all the Pygame modules when game is about to exit
                    sys.exit()
            #Time VARIABLES
            #delta time ->time between 2 frames i.e image for animation
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000 # converting from milliseconds to seconds
            self.start_time = pygame.time.get_ticks() #current time is captured by get_ticks() and assigned to self.start_time
            pygame.display.update() #display the evry tick
            self.screen.blit(self.bg_image, (0,0)) #blit-> copying/overlaying image onto screen
            self.machine.update(self.delta_time)
            self.screen.blit(self.grid_image, (0,0))
            self.clock.tick(FPS) #set limit on maximum frames per second

if __name__ == '__main__':
    game = Game()
    game.run()        





