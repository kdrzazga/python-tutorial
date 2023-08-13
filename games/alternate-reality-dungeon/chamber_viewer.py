import requests
import logging
import pygame

BACKGROUND = (0, 0, 0)
PLAYER_COLOR = (12, 222, 222)


def load(index):
    url = "http://localhost:9991/" + str(index)

    response = requests.get(url)
    if response.status_code == 200:
        path = response.text

        logging.info("Read path: %s", path)

        bitmap = pygame.image.load(path).convert_alpha()


def setup():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    pygame.init()
    pygame.key.set_repeat(0, 0)

    canvas_width = 640
    canvas_height = 480
    screen = pygame.display.set_mode((canvas_width, canvas_height))
    pygame.display.set_caption("Chamber Viewer")


if __name__ == '__main__':
    setup()
    load(2)
