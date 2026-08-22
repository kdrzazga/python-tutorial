import pygame

from snowman_morphing import SnowmanMorphing

WIDTH = 900
HEIGHT = 760


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    morph = SnowmanMorphing(WIDTH, HEIGHT)
    pygame.display.set_caption(morph.title)

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    morph.reset()

        if not paused:
            morph.update()

        morph.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
