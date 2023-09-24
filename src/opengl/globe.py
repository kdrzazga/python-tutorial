import pygame
from datetime import datetime
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class GlobeRenderer:
    def __init__(self):
        self.text_to_display = "HELLO"
        self.display = (800, 600)
        pygame.init()
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        self.angle_x = 0
        self.angle_y = 0

        self.load_texture()
        self.setup_opengl()
        self.create_sphere_display_list()

        self.font = pygame.font.Font(None, 36)

    def load_texture(self):
        self.globe_texture = pygame.image.load("resources/globe.jpg")
        self.globe_width, self.globe_height = self.globe_texture.get_size()
        self.globe_data = pygame.image.tostring(self.globe_texture, "RGBA", 1)

    def setup_opengl(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    def create_sphere_display_list(self):
        self.sphere_display_list = glGenLists(1)
        glNewList(self.sphere_display_list, GL_COMPILE)
        glPushMatrix()
        glColor3f(1, 1, 1)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluSphere(quadric, 1, 100, 100)
        glPopMatrix()
        glEndList()

    def render_text(self):
        text_surface = self.font.render(self.text_to_display, True, (255 -  (7* datetime.now().second) % 255, 120 + 125 * math.sin(3.14/(datetime.now().second + 1) / 60), 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", 1)
        text_width, text_height = text_surface.get_size()

        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.5, 0.5, -2.0)
        glTexCoord2f(1, 0)
        glVertex3f(0.5, 0.5, -2.0)
        glTexCoord2f(1, 1)
        glVertex3f(0.5, -0.5, -2.0)
        glTexCoord2f(0, 1)
        glVertex3f(-0.5, -0.5, -2.0)
        glEnd()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            glRotatef(self.angle_x, 1, 0, 0)
            glRotatef(self.angle_y, 0, 1, 0)

            glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.globe_width, self.globe_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.globe_data)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

            glCallList(self.sphere_display_list)

            self.render_text()

            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(3)

            self.angle_x += 0.5
            self.angle_y += 0.1

if __name__ == "__main__":
    globe_renderer = GlobeRenderer()
    globe_renderer.run()
