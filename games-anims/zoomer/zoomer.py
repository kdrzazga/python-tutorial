import pygame
import sys
import time

class Constants:
    WIDTH, HEIGHT = 800, 600
    LIGHT_BLUE = (96, 96, 192)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BROWN = (185, 122, 85)
    PURPLE = (200, 130, 200)
    YELLOW = (255, 255, 0)
    BLUE = (32, 0, 128)
    
class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Blinking Square and Zooming Rectangle")
        self.font_path = "resources/C64_Pro_Mono-STYLE.ttf"
        self.rectangle_width, self.rectangle_height = 400, 300
        self.zoom_factor = 1.0
        self.zoom_speed = 0.03
        self.blinking = True
        self.blink_interval = 0.6
        self.last_blink_time = time.time()
        self.font_size = 12
        self.square_base_size = self.font_size
        self.running = True
        self.font = pygame.font.Font(self.font_path, self.font_size)
        
        self.caption_x = 0
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.mouse.set_pos((self.width - 1, self.height - 1))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            pygame.time.delay(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.zoom_factor += self.zoom_speed
        if self.zoom_factor >= 1.5 or self.zoom_factor <= 0.5:
            self.zoom_speed *= -1

        current_time = time.time()
        if current_time - self.last_blink_time > self.blink_interval:
            self.blinking = not self.blinking
            self.last_blink_time = current_time
            
    def render(self):
        self.screen.fill(Constants.LIGHT_BLUE)
        rect_width = int(self.rectangle_width * self.zoom_factor)
        rect_height = int(self.rectangle_height * self.zoom_factor)
        rect_x = (self.width - rect_width) // 2
        rect_y = (self.height - rect_height) // 2

        pygame.draw.rect(self.screen, Constants.BLUE, (rect_x, rect_y, rect_width, rect_height))

        if self.blinking:
            square_size = int(self.square_base_size * self.zoom_factor)
            square_x = rect_x
            square_y = rect_y + 7.5 * square_size
            pygame.draw.rect(self.screen, Constants.LIGHT_BLUE, (square_x, square_y, square_size, square_size))

        self.font_size = int(10 * self.zoom_factor)
        self.font = pygame.font.Font(self.font_path, self.font_size)
        
        self.write(1, "   **** COMMODORE 64 BASIC V2 ****   ", rect_x, rect_y, rect_width)
        self.write(3, " 64K RAM SYSTEM  39811 BASIC BYTES FREE ", rect_x, rect_y, rect_width)
        self.write(5, "READY.", rect_x, rect_y, rect_width, False)
        self.write(6, "?MOS VIC-II FAILURE ERROR", rect_x, rect_y, rect_width, False)
        self.write(8, "READY.", rect_x, rect_y, rect_width, False)

    def write(self, line: int, text: str, rect_x: int, rect_y: int, rect_width: int, centered=True):
        caption_text = self.font.render(text, True, Constants.LIGHT_BLUE)
        caption_x = rect_x + (rect_width - caption_text.get_width()) // 2 if centered else rect_x
        caption_y = rect_y + line * caption_text.get_height()
        self.screen.blit(caption_text, (caption_x, caption_y))

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    c64 = Game()
    c64.run()
    c64.quit()
    
