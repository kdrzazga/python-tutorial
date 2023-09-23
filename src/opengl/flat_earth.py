import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Window size and display
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Load the globe texture
globe_texture = pygame.image.load("resources/globe.png")
globe_texture_data = pygame.image.tostring(globe_texture, "RGBA", 1)
globe_width, globe_height = globe_texture.get_size()

# Set up OpenGL
glEnable(GL_TEXTURE_2D)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)

# Rotate and tilt the globe
angle_x = 0
angle_y = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexImage2D(GL_TEXTURE_2D, 0, 3, globe_width, globe_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, globe_texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, 0)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, 0)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, 0)
    glEnd()

    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)

    angle_x += 0.5  # Adjust rotation speed
    angle_y += 0.5  # Adjust rotation speed
