import string

import pygame
from OpenGL.GL import (
    GL_COMPILE,
    GL_QUADS,
    GL_TEXTURE_2D,
    GL_TRIANGLES,
    glBegin,
    glCallList,
    glColor3f,
    glDisable,
    glEnable,
    glEnd,
    glEndList,
    glGenLists,
    glNewList,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glScalef,
    glVertex3f,
)

from .globals import ALPHABET_PATH

ALPHABET = string.ascii_uppercase
CELL_W, CELL_H = 120, 176
VOXEL = 6            # source pixels per grid cell
SPACE_COLS = 10      # width of a space / unknown character
LETTER_GAP = 2       # empty columns between letters
OVERSHOOT = 4        # M and W are drawn 4px wider than their cell on each side
OVERSIZED = ("M", "W")
DEPTH = 1.5
SCALE = 0.05

FRONT_COLOR = (0.95, 0.95, 1.0)
BACK_COLOR = (0.45, 0.45, 0.65)
SIDE_COLOR = (0.62, 0.62, 0.82)


def _cell_polygons(tl, tr, br, bl, gx, gy):
    """Marching-squares fill for one grid cell. Returns the polygon(s)
    covering the letter area, so diagonal (beveled) corners become real
    triangles/chamfers instead of squares."""
    TL, TR, BR, BL = (gx, gy), (gx + 1, gy), (gx + 1, gy + 1), (gx, gy + 1)
    T, R, B, L = (gx + 0.5, gy), (gx + 1, gy + 0.5), (gx + 0.5, gy + 1), (gx, gy + 0.5)
    mask = (tl, tr, br, bl)

    if mask == (True, True, True, True):
        return [[TL, TR, BR, BL]]
    if mask == (False, False, False, False):
        return []

    count = sum(mask)
    if count == 1:
        if tl: return [[TL, T, L]]
        if tr: return [[TR, R, T]]
        if br: return [[BR, B, R]]
        return [[BL, L, B]]
    if count == 3:
        if not bl: return [[TL, TR, BR, B, L]]
        if not br: return [[TL, TR, R, B, BL]]
        if not tr: return [[TL, T, R, BR, BL]]
        return [[T, TR, BR, BL, L]]
    # count == 2
    if tl and tr: return [[TL, TR, R, L]]
    if tr and br: return [[T, TR, BR, B]]
    if br and bl: return [[L, R, BR, BL]]
    if bl and tl: return [[TL, T, B, BL]]
    if tl and br: return [[TL, T, L], [BR, B, R]]
    return [[TR, R, T], [BL, L, B]]  # tr and bl


class Caption:
    def __init__(self, text):
        self.text = text
        self.lean = 0.0          # degrees; tilts the caption back about the x axis
        self.display_list = None

    @property
    def world_width(self):
        """Total caption width in world units, i.e. after SCALE is applied."""
        columns = [self._letter_window(char)[1] if char in ALPHABET else SPACE_COLS
                   for char in self.text.upper()]
        if not columns:
            return 0.0
        return (sum(columns) + LETTER_GAP * (len(columns) - 1)) * SCALE

    def prepare(self):
        """Build the geometry up front so the first render costs nothing."""
        if self.display_list is None:
            self.display_list = self._build()

    def render(self):
        self.prepare()

        glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glRotatef(self.lean, 1, 0, 0)
        glScalef(SCALE, SCALE, SCALE)
        glCallList(self.display_list)
        glPopMatrix()
        glEnable(GL_TEXTURE_2D)

    def _build(self):
        sheet = pygame.image.load(ALPHABET_PATH).convert()
        rows = CELL_H // VOXEL

        placed = []
        for char in self.text.upper():
            if char in ALPHABET:
                origin_x, cols = self._letter_window(char)
                placed.append((origin_x, cols))
            else:
                placed.append((None, SPACE_COLS))

        total_cols = sum(cols for _, cols in placed) + LETTER_GAP * (len(placed) - 1)

        front, back, sides = [], [], []
        pen_x = -total_cols / 2.0
        for origin_x, cols in placed:
            if origin_x is not None:
                self._emit_letter(sheet, origin_x, cols, rows, pen_x, front, back, sides)
            pen_x += cols + LETTER_GAP

        return self._compile(front, back, sides)

    def _letter_window(self, char):
        """Sheet x-origin and column count for a letter. M and W are 128px wide
        and overflow OVERSHOOT px into each neighbouring cell, so give them their
        full width and keep their neighbours from sampling that overflow."""
        index = ALPHABET.index(char)
        left = index * CELL_W
        if char in OVERSIZED:
            return left - OVERSHOOT, (CELL_W + 2 * OVERSHOOT) // VOXEL

        right_neighbour = ALPHABET[index + 1] if index + 1 < len(ALPHABET) else ""
        left_neighbour = ALPHABET[index - 1] if index > 0 else ""
        if right_neighbour in OVERSIZED:            # oversized letter bleeds into our right
            return left, (CELL_W - OVERSHOOT) // VOXEL
        if left_neighbour in OVERSIZED:             # oversized letter bleeds into our left
            return left + OVERSHOOT, (CELL_W - OVERSHOOT) // VOXEL
        return left, CELL_W // VOXEL

    def _emit_letter(self, sheet, origin_x, cols, rows, pen_x, front, back, sides):
        sheet_w, sheet_h = sheet.get_size()

        def inside(i, j):
            x = min(origin_x + i * VOXEL, sheet_w - 1)
            y = min(j * VOXEL, sheet_h - 1)
            red, green, blue = sheet.get_at((x, y))[:3]
            return red > 150 and green > 150 and blue > 150

        corner = [[inside(i, j) for j in range(rows + 1)] for i in range(cols + 1)]
        for gx in range(cols):
            for gy in range(rows):
                polygons = _cell_polygons(corner[gx][gy], corner[gx + 1][gy],
                                          corner[gx + 1][gy + 1], corner[gx][gy + 1], gx, gy)
                for polygon in polygons:
                    self._emit_polygon(polygon, pen_x, rows, front, back, sides)

    def _emit_polygon(self, polygon, pen_x, rows, front, back, sides):
        # Image space has y pointing down; flip it and centre the letter vertically.
        pts = [(pen_x + x, rows / 2.0 - y) for x, y in polygon]

        for k in range(1, len(pts) - 1):
            front.extend([(pts[0][0], pts[0][1], DEPTH),
                          (pts[k][0], pts[k][1], DEPTH),
                          (pts[k + 1][0], pts[k + 1][1], DEPTH)])
            back.extend([(pts[0][0], pts[0][1], 0.0),
                         (pts[k + 1][0], pts[k + 1][1], 0.0),
                         (pts[k][0], pts[k][1], 0.0)])

        count = len(pts)
        for k in range(count):
            x1, y1 = pts[k]
            x2, y2 = pts[(k + 1) % count]
            sides.extend([(x1, y1, DEPTH), (x2, y2, DEPTH), (x2, y2, 0.0), (x1, y1, 0.0)])

    def _compile(self, front, back, sides):
        list_id = glGenLists(1)
        glNewList(list_id, GL_COMPILE)

        glColor3f(*FRONT_COLOR)
        glBegin(GL_TRIANGLES)
        for vertex in front:
            glVertex3f(*vertex)
        glEnd()

        glColor3f(*BACK_COLOR)
        glBegin(GL_TRIANGLES)
        for vertex in back:
            glVertex3f(*vertex)
        glEnd()

        glColor3f(*SIDE_COLOR)
        glBegin(GL_QUADS)
        for vertex in sides:
            glVertex3f(*vertex)
        glEnd()

        glEndList()
        return list_id
