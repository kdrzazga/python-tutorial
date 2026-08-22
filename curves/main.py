import pygame

from archimedean_spiral import ArchimedeanSpiral
from bio_harmonic_loop import BioHarmonicLoop
from cardioid import Cardioid
from christmas_tree import ChristmasTree
from scarf import Scarf
from limacon_trisectrix import LimaconTrisectrix
from mittens import Mittens
from santa_claus import SantaClaus
from shifted_butterfly import ShiftedButterfly
from smooth_dual_loop import SmoothDualLoop
from snowflake import Snowflake, Snowflake2
from snowman import Snowman
from star import Star
from three_petal_rose import ThreePetalRose
from winter_cap import WinterCap

WIDTH = 1000
HEIGHT = 800
HOLD_FRAMES = 90

MARGIN = 20
PAD = 12
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_formula(screen, font, curve):
    lines = curve.formula if isinstance(curve.formula, list) else [curve.formula]
    surfaces = [font.render(line, True, BLACK) for line in lines]
    line_height = font.get_linesize()
    text_width = max(surface.get_width() for surface in surfaces)
    text_height = line_height * len(lines)

    brace_surface = None
    brace_width = 0
    if isinstance(curve.formula, list) and len(lines) > 1:
        brace_font = pygame.font.SysFont("arial", int(text_height))
        brace_surface = brace_font.render("{", True, BLACK)
        brace_width = brace_surface.get_width()

    box_width = PAD * 2 + brace_width + text_width
    box_height = PAD * 2 + text_height
    pygame.draw.rect(screen, WHITE, (MARGIN, MARGIN, box_width, box_height))

    text_x = MARGIN + PAD
    if brace_surface is not None:
        brace_y = MARGIN + PAD - (brace_surface.get_height() - text_height) // 2
        screen.blit(brace_surface, (MARGIN + PAD, brace_y))
        text_x += brace_width + 8

    for i, surface in enumerate(surfaces):
        screen.blit(surface, (text_x, MARGIN + PAD + i * line_height))


def run(curves):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, italic=True)

    running = True
    paused = False
    index = 0
    hold = 0
    while running and index < len(curves):
        curve = curves[index]
        pygame.display.set_caption(curve.title)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused

        if not paused:
            if not curve.is_complete():
                curve.update()
            else:
                hold += 1
                if hold >= HOLD_FRAMES:
                    hold = 0
                    index += 1

        curve.draw(screen)
        draw_formula(screen, font, curve)
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
        Star(WIDTH, HEIGHT),
        Snowflake(WIDTH, HEIGHT),
        Snowflake2(WIDTH, HEIGHT),
        Snowman(WIDTH, HEIGHT),
        Scarf(WIDTH, HEIGHT),
        Mittens(WIDTH, HEIGHT),
        WinterCap(WIDTH, HEIGHT),
        SantaClaus(WIDTH, HEIGHT),
        ChristmasTree(WIDTH, HEIGHT),
    ])
