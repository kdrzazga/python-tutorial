import math

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_ONE,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_QUADS,
    GL_QUAD_STRIP,
    GL_SRC_ALPHA,
    GL_TRIANGLE_FAN,
    GL_TRIANGLE_STRIP,
    glBegin,
    glBlendFunc,
    glClear,
    glClearColor,
    glColor4f,
    glEnd,
    glVertex2f,
)


class Painter:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def begin_frame(self, background):
        glClearColor(background[0], background[1], background[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def alpha_blend(self):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def additive_blend(self):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    def gradient_rect(self, x0, y0, x1, y1, bottom_color, top_color):
        glBegin(GL_QUADS)
        glColor4f(*bottom_color)
        glVertex2f(x0, y0)
        glColor4f(*bottom_color)
        glVertex2f(x1, y0)
        glColor4f(*top_color)
        glVertex2f(x1, y1)
        glColor4f(*top_color)
        glVertex2f(x0, y1)
        glEnd()

    def radial(self, center_x, center_y, radius, inner_color, outer_color, segments=64):
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(*inner_color)
        glVertex2f(center_x, center_y)
        glColor4f(*outer_color)
        for step in range(segments + 1):
            angle = 2.0 * math.pi * step / segments
            glVertex2f(center_x + math.cos(angle) * radius, center_y + math.sin(angle) * radius)
        glEnd()

    def ellipse(self, center_x, center_y, radius_x, radius_y, inner_color, outer_color, segments=64):
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(*inner_color)
        glVertex2f(center_x, center_y)
        glColor4f(*outer_color)
        for step in range(segments + 1):
            angle = 2.0 * math.pi * step / segments
            glVertex2f(center_x + math.cos(angle) * radius_x, center_y + math.sin(angle) * radius_y)
        glEnd()

    def ring(self, center_x, center_y, inner_radius, outer_radius, inner_color, outer_color, segments=72):
        glBegin(GL_QUAD_STRIP)
        for step in range(segments + 1):
            angle = 2.0 * math.pi * step / segments
            cosine = math.cos(angle)
            sine = math.sin(angle)
            glColor4f(*inner_color)
            glVertex2f(center_x + cosine * inner_radius, center_y + sine * inner_radius)
            glColor4f(*outer_color)
            glVertex2f(center_x + cosine * outer_radius, center_y + sine * outer_radius)
        glEnd()

    def fan(self, center_x, center_y, outline, center_color, edge_color):
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(*center_color)
        glVertex2f(center_x, center_y)
        glColor4f(*edge_color)
        for point in outline:
            glVertex2f(point[0], point[1])
        glEnd()

    def column_strip(self, columns):
        glBegin(GL_QUAD_STRIP)
        for x, y_bottom, y_top, color_bottom, color_top in columns:
            glColor4f(*color_bottom)
            glVertex2f(x, y_bottom)
            glColor4f(*color_top)
            glVertex2f(x, y_top)
        glEnd()

    def horizontal_beam(self, center_x, y_bottom, y_top, half_width, center_color, edge_color):
        glBegin(GL_TRIANGLE_STRIP)
        glColor4f(*edge_color)
        glVertex2f(center_x - half_width, y_bottom)
        glColor4f(*edge_color)
        glVertex2f(center_x - half_width, y_top)
        glColor4f(*center_color)
        glVertex2f(center_x, y_bottom)
        glColor4f(*center_color)
        glVertex2f(center_x, y_top)
        glColor4f(*edge_color)
        glVertex2f(center_x + half_width, y_bottom)
        glColor4f(*edge_color)
        glVertex2f(center_x + half_width, y_top)
        glEnd()

    def tapered_segment(self, x0, y0, x1, y1, width0, width1, color0, color1):
        direction_x = x1 - x0
        direction_y = y1 - y0
        length = math.hypot(direction_x, direction_y) or 1.0
        normal_x = -direction_y / length
        normal_y = direction_x / length
        glBegin(GL_QUADS)
        glColor4f(*color0)
        glVertex2f(x0 + normal_x * width0, y0 + normal_y * width0)
        glColor4f(*color0)
        glVertex2f(x0 - normal_x * width0, y0 - normal_y * width0)
        glColor4f(*color1)
        glVertex2f(x1 - normal_x * width1, y1 - normal_y * width1)
        glColor4f(*color1)
        glVertex2f(x1 + normal_x * width1, y1 + normal_y * width1)
        glEnd()

    def glow_dot(self, x, y, radius, color, segments=12):
        transparent = (color[0], color[1], color[2], 0.0)
        self.radial(x, y, radius, color, transparent, segments)
