import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define the vertices of the triangle
vertices = [
    (1, -1, 0),
    (1, 1, 0),
    (-1, 1, 0),
]

# Define the edges connecting the vertices
edges = [
    (0, 1),
    (1, 2),
    (2, 0),
]


def draw_triangle():
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINES)  # Start drawing lines
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])  # Specify vertex position
    glEnd()  # End drawing


def main():
    pygame.init()
    display = (800, 600)  # Set the window size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Create OpenGL context
    glTranslatef(0.0, 0.0, 15)  # Move the triangle away from the viewer

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                pygame.quit()
                return

        glRotatef(1, 0, 1, 0)  # Rotate the triangle
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
        draw_triangle()  # Draw the triangle
        pygame.display.flip()  # Update the display
        pygame.time.wait(10)  # Limit the frame rate


if __name__ == "__main__":
    main()
