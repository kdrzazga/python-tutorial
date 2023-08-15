import logging
import pygame
import math

from level_manager import LevelManager
from constants import Constants
from cloud import Cloud

class Loco:
    
    def __init__(self):
    
        pygame.init()
        
        mp3_file = "resources/audio/steam-locomotive.mp3"
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play(-1)  # -1: infinite loop
        
        whistle_path = "resources/audio/whistle.mp3"
        self.whistle = pygame.mixer.Sound(whistle_path)
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s <%(levelname)s> %(message)s')
        
        self.level_mgr = LevelManager()
        
        self.wheels_angle_deg = 0
        self.wheels_bitmap = pygame.image.load("resources/wheels.png")
        self.loco_y= 182
        
        
    def keys_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_RSHIFT] or keys[pygame.K_RALT] \
                or keys[pygame.K_RCTRL]:
            logging.info("key pressed")            
            self.cloud.draw()
            self.whistle.play()
        
    
    def rotate_wheels(self):
        r = 10
        self.wheels_angle_deg += 16
        x = 552 - r
        y = 86 + self.loco_y - r
        self.screen.blit(self.wheels_bitmap, (x, y))
        xplus = x + 5
        
        x1 = xplus + r* math.cos (math.radians(self.wheels_angle_deg))
        y1 = y + r* math.sin(math.radians(self.wheels_angle_deg))        
        x2 = xplus + r* math.cos (math.radians(self.wheels_angle_deg + 45))
        y2 = y + r* math.sin(math.radians(self.wheels_angle_deg + 45))

        pygame.draw.line(self.screen, Constants.BLACK, (x1, y1), (x2 + 90, y2 + 20), 4)
        pygame.display.update()

    
    def main(self):
        self.screen = pygame.display.set_mode((Constants.canvas_width, Constants.canvas_height))
        pygame.display.set_caption("atari LOCO")
        self.cloud = Cloud(Constants.canvas_width // 2, 100, 100, 50, self.screen, Constants.canvas_width, Constants.canvas_height)
                
        railroad_bitmap = pygame.image.load("resources/railroad.png")
        loco_bitmap = pygame.image.load("resources/loco.png")
        
        double_bitmap_width = railroad_bitmap.get_width() * 2
        double_bitmap = pygame.Surface((double_bitmap_width, railroad_bitmap.get_height()))
        double_bitmap.blit(railroad_bitmap, (0, 0))  # constant background
        double_bitmap.blit(railroad_bitmap, (railroad_bitmap.get_width(), 0))  # animated background
        
        background_x = 0
        self.running = True
        self.clock = pygame.time.Clock()
        scroll_speed = 5
        
        self.screen.fill(Constants.BLACK)
        blue_rectLB = pygame.Rect(0, 91, 530, 183)
        pygame.draw.rect(self.screen, Constants.SKY, blue_rectLB)
        blue_rectR = pygame.Rect(Constants.canvas_width - 472, 0, Constants.canvas_width, 294)
        pygame.draw.rect(self.screen, Constants.SKY, blue_rectR)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            self.screen.blit(loco_bitmap, (0, self.loco_y))
            pygame.display.update()
            self.screen.blit(double_bitmap, (background_x, 294))
        
            background_x -= scroll_speed
            if background_x <= -railroad_bitmap.get_width():
                background_x = 0
            
            self.rotate_wheels()
        
            self.keys_input()
            
            if self.cloud != None:
                self.cloud.counter += 1
            
                if self.cloud.check_limit():
                    self.cloud.clear()
                    self.cloud.counter = 0

                print(self.cloud.counter)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        
if __name__ == '__main__':
    loco = Loco()
    loco.main()
