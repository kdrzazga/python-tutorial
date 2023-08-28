import pygame
import time

class MusicPlayer:
    
    def __init__(self):
        num_channels = 2
        pygame.mixer.set_num_channels(num_channels)
        self.background_beat = pygame.mixer.Sound('src/resources/music/beat.mp3')
        self.music_track2 = pygame.mixer.Sound('src/resources/music/tune.mp3')
        
        self.channel0 = pygame.mixer.Channel(0)
        self.channel1 = pygame.mixer.Channel(1)

    def play(self):
        self.channel0.play(self.background_beat, loops=-1)
        self.channel1.play(self.music_track2, loops=-1)

        #while self.channel1.get_busy() or self.channel2.get_busy():
        #    pygame.time.wait(100)
        #    pass

#pygame.init()
#MusicPlayer().play()
#pygame.quit()
