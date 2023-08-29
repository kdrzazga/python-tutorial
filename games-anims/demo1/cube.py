import pygame
import math
import sys

from lib3d import Rotation

class CubeRotation:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_width(), screen.get_height()
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.clock = pygame.time.Clock()
        self.angle_x = 0
        self.angle_y = 0
        self.angle_change = 1
        self.cube_vertices = [
            (1, 1, -1),
            (1, -1, -1),
            (-1, -1, -1),
            (-1, 1, -1),
            (1, 1, 1),
            (1, -1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        ]
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    def project(self, vertex):
        x, y, z = vertex
        f = 200 / (z + 3)
        x, y = x * f, y * f
        return x, y

    def rotate_cube(self):
        rotated_vertices = []
        for vertex in self.cube_vertices:
            rotated_vertex_x = Rotation.rotate_point_x(*vertex, self.angle_x)
            rotated_vertex_xy = Rotation.rotate_point_y(*rotated_vertex_x, self.angle_y)
            rotated_vertices.append(rotated_vertex_xy)
        return rotated_vertices

    def draw_cube(self):
        rotated_vertices = self.rotate_cube()
        projected_vertices = [self.project(vertex) for vertex in rotated_vertices]

        for edge in self.edges:
            x1, y1 = projected_vertices[edge[0]]
            x2, y2 = projected_vertices[edge[1]]
            pygame.draw.line(self.screen, self.WHITE, (x1 + self.CENTER[0], y1 + self.CENTER[1]), (x2 + self.CENTER[0], y2 + self.CENTER[1]))

    def update(self):
        self.angle_x += self.angle_change
        self.angle_y += 1

    def rotation_procedure(self, duration_ms):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.update()
            self.screen.fill(self.BLACK)
            self.draw_cube()
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        self.rotation_procedure(5000)
        for _ in range(7):
            self.angle_change +=1
            self.rotation_procedure(1000)
        for _ in range(7):
            self.angle_change -=1
            self.rotation_procedure(1000)
    
        self.rotation_procedure(5000)

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cube Rotation")
    
    app = CubeRotation(screen)
    app.run()
    pygame.quit()
    sys.exit()
