import numpy as np
from PIL import Image
from OpenGL.GL import (
    GL_ALPHA_TEST,
    GL_COMPILE,
    GL_GREATER,
    GL_LINEAR,
    GL_QUADS,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glAlphaFunc,
    glBegin,
    glBindTexture,
    glCallList,
    glColor4f,
    glDisable,
    glEnable,
    glEnd,
    glEndList,
    glGenLists,
    glGenTextures,
    glNewList,
    glTexCoord2f,
    glTexImage2D,
    glTexParameteri,
    glVertex3f,
)

THICKNESS = 0.25     # slab depth
WALL_STEP = 3        # pixels per wall segment along the outline
EDGE_SHADE = 0.65    # side walls darker than the face they belong to


def load_rgba(image_path):
    """RGBA pixels as a (height, width, 4) array; needs no display."""
    return np.array(Image.open(image_path).convert("RGBA"))


class LogoSlab:
    """Transparent RGBA artwork extruded into a solid. Walls are raised along
    every opaque/transparent boundary, so holes and concave shapes get real
    depth instead of being treated as a flat card."""

    def __init__(self, rgba, height):
        self.rgba = rgba
        self.half_h = height / 2.0
        self.half_w = self.half_h * rgba.shape[1] / rgba.shape[0]
        self.display_list = None

    def draw(self):
        if self.display_list is None:
            self.display_list = self._build()

        glEnable(GL_ALPHA_TEST)     # transparent texels must not block the walls
        glAlphaFunc(GL_GREATER, 0.5)
        glCallList(self.display_list)
        glDisable(GL_ALPHA_TEST)

    def _build(self):
        texture_id = self._upload_texture()

        list_id = glGenLists(1)
        glNewList(list_id, GL_COMPILE)
        self._draw_faces(texture_id)
        self._draw_walls()
        glEndList()
        return list_id

    def _upload_texture(self):
        height, width = self.rgba.shape[:2]
        data = np.ascontiguousarray(np.flipud(self.rgba)).tobytes()  # GL origin is bottom-left

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, data)
        return texture_id

    def _to_model_x(self, px):
        return (px / self.rgba.shape[1] - 0.5) * 2.0 * self.half_w

    def _to_model_y(self, py):
        return (0.5 - py / self.rgba.shape[0]) * 2.0 * self.half_h

    def _draw_faces(self, texture_id):
        front, back = THICKNESS / 2.0, -THICKNESS / 2.0

        glEnable(GL_TEXTURE_2D)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-self.half_w, -self.half_h, front)
        glTexCoord2f(1.0, 0.0); glVertex3f(self.half_w, -self.half_h, front)
        glTexCoord2f(1.0, 1.0); glVertex3f(self.half_w, self.half_h, front)
        glTexCoord2f(0.0, 1.0); glVertex3f(-self.half_w, self.half_h, front)

        # mirrored so the artwork also reads correctly from behind
        glTexCoord2f(1.0, 0.0); glVertex3f(-self.half_w, -self.half_h, back)
        glTexCoord2f(0.0, 0.0); glVertex3f(self.half_w, -self.half_h, back)
        glTexCoord2f(0.0, 1.0); glVertex3f(self.half_w, self.half_h, back)
        glTexCoord2f(1.0, 1.0); glVertex3f(-self.half_w, self.half_h, back)
        glEnd()

    def _draw_walls(self):
        inside = (self.rgba[::WALL_STEP, ::WALL_STEP, 3] >= 128)
        colors = self.rgba[::WALL_STEP, ::WALL_STEP, :3] / 255.0 * EDGE_SHADE
        front, back = THICKNESS / 2.0, -THICKNESS / 2.0

        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        for edge, (dy, dx) in (("left", (0, -1)), ("right", (0, 1)),
                               ("top", (-1, 0)), ("bottom", (1, 0))):
            for gy, gx in zip(*np.nonzero(inside & ~self._neighbour(inside, dy, dx))):
                glColor4f(*colors[gy, gx], 1.0)
                (x1, y1), (x2, y2) = self._edge_corners(edge, gx, gy)
                glVertex3f(x1, y1, front)
                glVertex3f(x1, y1, back)
                glVertex3f(x2, y2, back)
                glVertex3f(x2, y2, front)
        glEnd()
        glEnable(GL_TEXTURE_2D)

    def _neighbour(self, inside, dy, dx):
        """`inside` shifted so each cell sees its neighbour; off-grid counts as empty."""
        shifted = np.zeros_like(inside)
        ys = slice(max(dy, 0), inside.shape[0] + min(dy, 0))
        xs = slice(max(dx, 0), inside.shape[1] + min(dx, 0))
        ys_src = slice(max(-dy, 0), inside.shape[0] + min(-dy, 0))
        xs_src = slice(max(-dx, 0), inside.shape[1] + min(-dx, 0))
        shifted[ys, xs] = inside[ys_src, xs_src]
        return shifted

    def _edge_corners(self, edge, gx, gy):
        left, right = self._to_model_x(gx * WALL_STEP), self._to_model_x((gx + 1) * WALL_STEP)
        top, bottom = self._to_model_y(gy * WALL_STEP), self._to_model_y((gy + 1) * WALL_STEP)
        return {
            "left": ((left, top), (left, bottom)),
            "right": ((right, bottom), (right, top)),
            "top": ((right, top), (left, top)),
            "bottom": ((left, bottom), (right, bottom)),
        }[edge]
