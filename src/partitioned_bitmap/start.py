import sys
import pygame

from constants import Constants
from loader import PartBitmapDisplay
from main import Main


def init():
    pygame.init()

    screen = pygame.display.set_mode((Constants.width, Constants.height))
    pygame.display.set_caption("Bitmap Animation")

    loader = PartBitmapDisplay(screen)
    loader.main()

    main = Main(screen)
    main.draw_background()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    init()
