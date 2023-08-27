import pygame
import sys

class Screen1:
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
    
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render("Screen1 (Intro)", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            pygame.display.flip()
            clock.tick(60)
            
class Screen2:
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((0, 255, 255))
            font = pygame.font.Font(None, 36)
            text = font.render("Screen2 (Game)", True, (0, 0, 0))
            self.screen.blit(text, (10, 10))
            pygame.display.flip()
            clock.tick(60)

def main():
    pygame.init()

    intro_screen = Screen1(800, 600)
    game_screen = Screen2(640, 480)

    game_screen.main()

    intro_screen.main()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
