import pygame

from archimedean_spiral import ArchimedeanSpiral
from bio_harmonic_loop import BioHarmonicLoop
from cardioid import Cardioid
from limacon_trisectrix import LimaconTrisectrix
from shifted_butterfly import ShiftedButterfly
from smooth_dual_loop import SmoothDualLoop
from three_petal_rose import ThreePetalRose

WIDTH = 800
HEIGHT = 800
HOLD_FRAMES = 90


def run(curves):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    index = 0
    hold = 0
    while running and index < len(curves):
        curve = curves[index]
        pygame.display.set_caption(curve.title)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not curve.is_complete():
            curve.update()
        else:
            hold += 1
            if hold >= HOLD_FRAMES:
                hold = 0
                index += 1

        curve.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run([
        BioHarmonicLoop(WIDTH, HEIGHT),
        LimaconTrisectrix(WIDTH, HEIGHT),
        Cardioid(WIDTH, HEIGHT),
        SmoothDualLoop(WIDTH, HEIGHT),
        ThreePetalRose(WIDTH, HEIGHT),
        ShiftedButterfly(WIDTH, HEIGHT),
        ArchimedeanSpiral(WIDTH, HEIGHT),
    ])
