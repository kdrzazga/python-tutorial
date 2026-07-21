import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, K_ESCAPE, K_SPACE, OPENGL, QUIT
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_MODELVIEW,
    GL_PROJECTION,
    glClear,
    glClearColor,
    glEnable,
    glLoadIdentity,
    glMatrixMode,
    glTranslatef,
)
from OpenGL.GLU import gluPerspective

from cube3d.libs.amiga_ball import AmigaBall

WINDOW_SIZE = (900, 700)
CAMERA_Z = -8.0


def main():
    pygame.init()
    pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Amiga ball demo - space toggles direction")
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.85, 0.85, 0.85, 1.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    ball = AmigaBall(radius=2.5)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    ball.clockwise = not ball.clockwise

        ball.update(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, CAMERA_Z)
        ball.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
