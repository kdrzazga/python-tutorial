import pygame

from src.constants import Constants
from src.sabkar import SaboteurKarateka
from src.intro import LightPointAnimation

if __name__ == "__main__":
    pygame.init()
    screen_intro = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    LightPointAnimation(screen_intro).run()
    
    screen_karateka = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))    
    SaboteurKarateka(screen_karateka).main()
    
    pygame.quit()
    