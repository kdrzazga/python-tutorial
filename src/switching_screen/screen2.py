class Screen2:

    def __init__(self):
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    @staticmethod
    def main():
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 255, 255))
            clock.tick(1)

