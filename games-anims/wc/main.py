import logging
import pygame


class WorldCupWinners:
    def __init__(self):
        self.background_bitmap = None
        self.scroll_speed = None
        self.double_bitmap = None
        self.BG_COLOR = (0, 0, 0)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.video_capture = None
        self.clock = None
        self.screen = None
        self.width, self.height = 800, 600
        self.question_position = (10, self.height - 100)
        self.font_path = "resources/font.otf"

        self.background_x = 0

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def update_display(self):
        self.background_x -= self.scroll_speed
        if self.background_x <= -self.background_bitmap.get_width():
            self.background_x = 0

        height_offset = 100
        self.double_bitmap = pygame.transform.scale(self.initial_dbl_bitmap, (self.double_bitmap_width, height_offset))

        desired_height = 560
        trimmed_image = pygame.Surface((self.double_bitmap.get_width(), desired_height))
        pygame.Surface.blit(trimmed_image, self.double_bitmap, (0, 0),
                            (0, 0, self.double_bitmap.get_width(), desired_height))

        self.screen.fill(self.BG_COLOR)

        caption_surface = pygame.Surface((self.width, self.height))(600, 50)

        self.screen.blit(caption_surface, (0, 0))
        self.screen.blit(self.double_bitmap, (self.background_x, 0))

        pygame.display.flip()
        self.clock.tick(76)
