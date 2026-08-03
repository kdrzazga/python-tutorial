"""
3D waving stripe in pygame + OpenGL, with a PNG drawn on it.

Unlike a ray-marched scene, a waving flag is real 3D geometry: a long thin
strip is subdivided into a fine grid of vertices, and a vertex shader pushes
each vertex back and forth along Z with a travelling sine wave. The wave's
slope gives us a surface normal for lighting, and the PNG from `resources/`
is mapped across the strip as a texture.

Structure:
    Shader  - a reusable compiled GLSL program with uniform setters.
    Stripe  - the waving, textured strip; owns its mesh + texture, draws itself.
    main()  - opens the window and runs the render loop.

Controls: arrow keys move the stripe in X/Y, Q/E move it in Z (toward/away),
Space pauses the wave, Esc / close quits.

Run:   python stripe.py
Needs: pygame, PyOpenGL, numpy
"""

import ctypes
import math
import os
import sys

import numpy as np
import pygame
from OpenGL.GL import (
    glCreateShader, glShaderSource, glCompileShader, glGetShaderiv,
    glGetShaderInfoLog, glCreateProgram, glAttachShader, glLinkProgram,
    glGetProgramiv, glGetProgramInfoLog, glUseProgram, glGetUniformLocation,
    glUniform1f, glUniform1i, glUniformMatrix3fv, glUniformMatrix4fv,
    glGenVertexArrays, glBindVertexArray, glGenBuffers, glBindBuffer,
    glBufferData, glEnableVertexAttribArray, glVertexAttribPointer,
    glDrawElements, glViewport, glClear, glClearColor, glEnable, glBlendFunc,
    glGenTextures, glBindTexture, glTexImage2D, glTexParameteri, glActiveTexture,
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_COMPILE_STATUS, GL_LINK_STATUS,
    GL_TRUE, GL_FALSE, GL_TRIANGLES, GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER,
    GL_STATIC_DRAW, GL_FLOAT, GL_UNSIGNED_INT, GL_TEXTURE_2D, GL_TEXTURE0,
    GL_RGBA, GL_UNSIGNED_BYTE, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER,
    GL_LINEAR, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE,
    GL_DEPTH_TEST, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
)


# ---------------------------------------------------------------------------
# Small 4x4 / 3x3 matrix helpers (row-major; uploaded with transpose=GL_TRUE).
# ---------------------------------------------------------------------------

def perspective(fovy, aspect, near, far):
    f = 1.0 / math.tan(fovy / 2.0)
    m = np.zeros((4, 4), dtype=np.float32)
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2.0 * far * near) / (near - far)
    m[3, 2] = -1.0
    return m


def translate(x, y, z):
    m = np.identity(4, dtype=np.float32)
    m[0, 3], m[1, 3], m[2, 3] = x, y, z
    return m


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    m = np.identity(4, dtype=np.float32)
    m[1, 1], m[1, 2] = c, -s
    m[2, 1], m[2, 2] = s, c
    return m


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    m = np.identity(4, dtype=np.float32)
    m[0, 0], m[0, 2] = c, s
    m[2, 0], m[2, 2] = -s, c
    return m


class Shader:
    """A compiled + linked GLSL program, with cached uniform locations."""

    def __init__(self, vertex_src, fragment_src):
        self.program = glCreateProgram()
        glAttachShader(self.program, self._compile(vertex_src, GL_VERTEX_SHADER))
        glAttachShader(self.program, self._compile(fragment_src, GL_FRAGMENT_SHADER))
        glLinkProgram(self.program)
        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.program).decode(errors="replace"))
        self._locations = {}

    @staticmethod
    def _compile(src, kind):
        sid = glCreateShader(kind)
        glShaderSource(sid, src.strip())
        glCompileShader(sid)
        if glGetShaderiv(sid, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(sid).decode(errors="replace"))
        return sid

    def use(self):
        glUseProgram(self.program)

    def _loc(self, name):
        if name not in self._locations:
            self._locations[name] = glGetUniformLocation(self.program, name)
        return self._locations[name]

    def set_int(self, name, value):
        glUniform1i(self._loc(name), value)

    def set_float(self, name, value):
        glUniform1f(self._loc(name), value)

    def set_mat4(self, name, mat):
        glUniformMatrix4fv(self._loc(name), 1, GL_TRUE, mat)

    def set_mat3(self, name, mat):
        glUniformMatrix3fv(self._loc(name), 1, GL_TRUE, mat)


class Stripe:
    """A subdivided strip that waves along its length, textured with a PNG."""

    COLS, ROWS = 140, 20      # mesh resolution (finer = smoother wave)
    HALF_W = 1.7              # half length of the strip

    VERTEX_SRC = """
    #version 330 core
    layout(location = 0) in vec2 a_pos;   // grid position in the flat strip
    layout(location = 1) in vec2 a_uv;

    uniform mat4  u_mvp;
    uniform mat3  u_normal;   // model rotation, for lighting the normals
    uniform float u_time;

    out vec2 v_uv;
    out vec3 v_normal;

    void main() {
        float x = a_pos.x;
        float y = a_pos.y;

        // Travelling wave along the strip (+ a gentle vertical ripple).
        float amp = 0.22;
        float k = 4.0;
        float speed = 3.0;
        float phase = k * x - speed * u_time;
        float z = amp * sin(phase) + 0.04 * sin(3.0 * y + speed * u_time);

        // Surface normal from the analytic slope of that wave.
        float dzdx = amp * k * cos(phase);
        float dzdy = 0.12 * cos(3.0 * y + speed * u_time);
        vec3 n = normalize(vec3(-dzdx, -dzdy, 1.0));

        gl_Position = u_mvp * vec4(x, y, z, 1.0);
        v_uv = a_uv;
        v_normal = normalize(u_normal * n);
    }
    """

    FRAGMENT_SRC = """
    #version 330 core
    in vec2 v_uv;
    in vec3 v_normal;
    uniform sampler2D u_tex;
    out vec4 fragColor;

    void main() {
        vec4 tex = texture(u_tex, v_uv);
        if (tex.a < 0.1) discard;               // keep PNG transparency crisp

        // abs() so both faces of the flapping strip are lit.
        vec3 n = normalize(v_normal);
        vec3 lig = normalize(vec3(0.3, 0.5, 0.8));
        float dif = abs(dot(n, lig));

        vec3 col = tex.rgb * (dif * 0.8 + 0.35);
        fragColor = vec4(sqrt(col), tex.a);     // sqrt = quick gamma correction
    }
    """

    def __init__(self, texture_path):
        self.shader = Shader(self.VERTEX_SRC, self.FRAGMENT_SRC)
        self.pos = np.zeros(3, dtype=np.float32)   # the stripe's own position

        image = pygame.image.load(texture_path)
        aspect = image.get_width() / image.get_height()
        half_h = self.HALF_W / aspect             # keep the PNG undistorted
        self.texture = self._upload_texture(image)

        self._build_mesh(half_h)

        self.shader.use()
        self.shader.set_int("u_tex", 0)

    def move(self, x, y, z):
        """Translate the stripe itself (not the camera) by (x, y, z)."""
        self.pos += (x, y, z)

    def _build_mesh(self, half_h):
        """Create the flat grid of vertices (pos.xy + uv) and its triangle indices."""
        cols, rows = self.COLS, self.ROWS
        xs = np.linspace(-self.HALF_W, self.HALF_W, cols)
        ys = np.linspace(-half_h, half_h, rows)

        verts = []
        for j in range(rows):
            for i in range(cols):
                verts += [xs[i], ys[j], i / (cols - 1), j / (rows - 1)]
        verts = np.array(verts, dtype=np.float32)

        indices = []
        for j in range(rows - 1):
            for i in range(cols - 1):
                a = j * cols + i
                b, c, d = a + 1, a + cols, a + cols + 1
                indices += [a, b, c, b, d, c]
        indices = np.array(indices, dtype=np.uint32)
        self.index_count = indices.size

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)

        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        stride = 4 * 4   # 4 floats per vertex
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(8))

    @staticmethod
    def _upload_texture(surf):
        w, h = surf.get_size()
        data = pygame.image.tobytes(surf, "RGBA", True)   # flip to GL's origin
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        return tex

    def render(self, width, height, time):
        # Model: move to the stripe's position, slow yaw, plus a slight tilt.
        model = (translate(self.pos[0], self.pos[1], self.pos[2])
                 @ rot_y(0.5 * math.sin(time * 0.4)) @ rot_x(-0.15))
        view = translate(0.0, 0.0, -4.0)
        proj = perspective(math.radians(45.0), width / height, 0.1, 100.0)
        mvp = proj @ view @ model
        normal_mat = np.ascontiguousarray(model[:3, :3])

        self.shader.use()
        self.shader.set_mat4("u_mvp", mvp)
        self.shader.set_mat3("u_normal", normal_mat)
        self.shader.set_float("u_time", time)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, ctypes.c_void_p(0))


def main():
    width, height = 900, 600
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)   # need a depth buffer
    pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("3D waving stripe")

    texture_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "resources", "k&a+.png")
    stripe = Stripe(texture_path)

    glViewport(0, 0, width, height)
    glClearColor(0.07, 0.08, 0.11, 1.0)
    glEnable(GL_DEPTH_TEST)                     # so wave folds overlap correctly
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    clock = pygame.time.Clock()
    sim_time = 0.0
    paused = False
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        if not paused:
            sim_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        # Move the stripe with held keys (arrows = X/Y, Q/E = Z toward/away).
        keys = pygame.key.get_pressed()

        def axis(pos_key, neg_key):
            return (1 if keys[pos_key] else 0) - (1 if keys[neg_key] else 0)

        step = 2.0 * dt   # units per second
        stripe.move(axis(pygame.K_RIGHT, pygame.K_LEFT) * step,
                    axis(pygame.K_UP, pygame.K_DOWN) * step,
                    axis(pygame.K_e, pygame.K_q) * step)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        stripe.render(width, height, sim_time)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:                       # noqa: BLE001
        print("Error:", exc, file=sys.stderr)
        pygame.quit()
        sys.exit(1)
