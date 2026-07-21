import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, K_ESCAPE, OPENGL, QUIT
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_TEXTURE_2D,
    glClear,
    glClearColor,
    glEnable,
    glLoadIdentity,
    glMatrixMode,
    glRotatef,
    glTranslatef,
)
from OpenGL.GLU import gluPerspective

from cube3d.libs.caption import Caption

WINDOW_SIZE = (900, 500)
CAMERA_Z = -20.0
ROTATION_SPEED = 20.0  # degrees per second


def main():
    pygame.init()
    pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Caption demo - bake a cake")
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.05, 0.05, 0.08, 1.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.1, 60.0)
    glMatrixMode(GL_MODELVIEW)

    caption = Caption("The quick brown fox jumps over the lazy dog")
    angle = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        angle += ROTATION_SPEED * dt

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, CAMERA_Z)
        glRotatef(15.0, 1, 0, 0)
        glRotatef(angle, 0, 1, 0)

        caption.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
