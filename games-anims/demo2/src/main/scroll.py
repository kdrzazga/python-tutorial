import math

import pygame


class Scroll:
    BG_COLOR = (124, 112, 218)

    def __init__(self, screen, canvas_width, canvas_height, scroll_speed):
        self.image_path = "src/main/resources/eod.png"

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.scroll_speed = scroll_speed
        self.background_x = 0

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.background_bitmap = pygame.image.load(self.image_path)
        self.double_bitmap_width = self.background_bitmap.get_width() * 2
        self.double_bitmap = pygame.Surface((self.double_bitmap_width, self.canvas_height))
        self.double_bitmap.blit(self.background_bitmap, (0, 0))
        self.double_bitmap.blit(self.background_bitmap, (self.background_bitmap.get_width(), 0))

        self.initial_dbl_bitmap = self.double_bitmap

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update_display(self):
        self.screen.fill(Scroll.BG_COLOR)

        self.background_x -= self.scroll_speed
        if self.background_x <= -self.background_bitmap.get_width():
            self.background_x = 0

        # Calculate the height as a sinusoidal function of time
        height_offset = (self.canvas_height - self.canvas_height / 2) * (
                    1 + math.sin(pygame.time.get_ticks() / 1000)) + 250
        height_offset = int(height_offset)

        self.double_bitmap = pygame.transform.scale(self.initial_dbl_bitmap, (self.double_bitmap_width, height_offset))

        self.screen.blit(self.double_bitmap, (self.background_x, 0))

        pygame.display.flip()
        self.clock.tick(76)

    def run(self, duration_ms):
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time <= duration_ms:
            running = self.handle_events()
            self.update_display()


# Usage
if __name__ == "__main__":
    pygame.init()
    canvas_width = 800
    cycles = 0
    screen = pygame.display.set_mode((canvas_width, 600))
    pygame.display.set_caption("EoD")

    scroll_instance = Scroll(screen, canvas_width, canvas_height=368, scroll_speed=5)
    while True:
        scroll_instance.run(19000)
        cycles += 1
        print(cycles)

    pygame.quit()
