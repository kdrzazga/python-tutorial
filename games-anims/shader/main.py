"""
HelloShader - the "Hello World" of 3D shaders, in pygame, with a textured sphere.

pygame only gives us a window + an OpenGL context; the 3D image is drawn by a
GLSL fragment (pixel) shader running on the GPU. We draw one fullscreen
triangle and, for every pixel, march a ray into the scene until it hits a
single sphere. The bitmap is then wrapped as a belt around the sphere's
equator (the poles are left plain).

Structure:
    Shader  - a reusable compiled GLSL program with uniform setters.
    Ball    - the ray-marched, textured sphere; owns a Shader and draws itself.
    main()  - opens the window and runs the render loop.

The bitmap is loaded from `resources/k&a+.png`.

Run:   python main.py     (Esc or close the window to quit)
Needs: pygame, PyOpenGL   ->  pip install pygame PyOpenGL
"""

import os
import sys
import textwrap

import pygame
from OpenGL.GL import (
    glCreateShader, glShaderSource, glCompileShader, glGetShaderiv,
    glGetShaderInfoLog, glCreateProgram, glAttachShader, glLinkProgram,
    glGetProgramiv, glGetProgramInfoLog, glUseProgram, glGetUniformLocation,
    glUniform1f, glUniform1i, glUniform2f, glGenVertexArrays, glBindVertexArray,
    glDrawArrays, glViewport, glGenTextures, glBindTexture, glTexImage2D,
    glTexParameteri, glActiveTexture, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
    GL_COMPILE_STATUS, GL_LINK_STATUS, GL_TRUE, GL_TRIANGLES, GL_TEXTURE_2D,
    GL_TEXTURE0, GL_RGBA, GL_UNSIGNED_BYTE, GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
    GL_REPEAT, GL_CLAMP_TO_EDGE,
)


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
        src = textwrap.dedent(src).strip()   # put #version at column 0
        sid = glCreateShader(kind)
        glShaderSource(sid, src)
        glCompileShader(sid)
        if glGetShaderiv(sid, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(sid).decode(errors="replace"))
        return sid

    def use(self):
        glUseProgram(self.program)

    def _loc(self, name):
        """Look up (and cache) a uniform location by name."""
        if name not in self._locations:
            self._locations[name] = glGetUniformLocation(self.program, name)
        return self._locations[name]

    def set_int(self, name, value):
        glUniform1i(self._loc(name), value)

    def set_float(self, name, value):
        glUniform1f(self._loc(name), value)

    def set_vec2(self, name, x, y):
        glUniform2f(self._loc(name), x, y)


class Ball:
    """A ray-marched sphere with a bitmap wrapped around its equator."""

    # Vertex shader: one big triangle covering the screen (no buffers needed).
    VERTEX_SRC = """
    #version 330 core
    void main() {
        vec2 v[3] = vec2[3](vec2(-1.0, -1.0), vec2(3.0, -1.0), vec2(-1.0, 3.0));
        gl_Position = vec4(v[gl_VertexID], 0.0, 1.0);
    }
    """

    # Fragment shader: one ray per pixel, ray-marched against a single sphere.
    FRAGMENT_SRC = """
    #version 330 core
    out vec4 fragColor;
    uniform vec2      u_res;
    uniform float     u_time;
    uniform sampler2D u_tex;      // the bitmap to wrap onto the sphere
    uniform float     u_aspect;   // texture width / height (keeps it undistorted)

    const float PI = 3.14159265;

    // Distance from point p to a sphere of radius r at the origin.
    float sphere(vec3 p, float r) { return length(p) - r; }

    void main() {
        // Screen coords with y up, aspect corrected so the sphere stays round.
        vec2 uv = (gl_FragCoord.xy - 0.5 * u_res) / u_res.y;

        vec3 ro = vec3(0.0, 0.0, -3.0);        // camera / ray origin
        vec3 rd = normalize(vec3(uv, 1.0));    // ray direction

        vec3 col = vec3(0.08, 0.10, 0.16);     // background

        // March along the ray until we hit the sphere (or give up).
        float t = 0.0;
        for (int i = 0; i < 64; i++) {
            vec3 p = ro + rd * t;
            float d = sphere(p, 1.0);
            if (d < 0.001) {
                vec3 n = normalize(p);         // normal = point on the unit sphere

                // Simple diffuse lighting from a fixed direction.
                vec3 lig = normalize(vec3(0.6, 0.7, -0.4));
                float shade = max(dot(n, lig), 0.0) * 0.9 + 0.2;

                // Wrap the bitmap once around the equator as a belt. Its
                // vertical span is derived from the image aspect so texels stay
                // square (no vertical stretch); the poles stay plain.
                float lon = atan(n.z, n.x) / (2.0 * PI) + 0.5 + u_time * 0.05; // spin
                float phi = asin(clamp(n.y, -1.0, 1.0));      // latitude, -PI/2..PI/2
                float band = 2.0 * PI / u_aspect;             // belt height in radians
                float v = phi / band + 0.5;                   // 0..1 inside the belt

                vec3 base = vec3(0.16, 0.18, 0.24);           // plain colour at the poles
                if (v >= 0.0 && v <= 1.0)
                    col = texture(u_tex, vec2(lon, v)).rgb * shade;
                else
                    col = base * shade;
                break;
            }
            t += d;
            if (t > 20.0) break;
        }

        fragColor = vec4(sqrt(col), 1.0);      // sqrt = quick gamma correction
    }
    """

    def __init__(self, texture_path):
        self.shader = Shader(self.VERTEX_SRC, self.FRAGMENT_SRC)
        self.vao = glGenVertexArrays(1)   # core profile needs a bound VAO to draw

        image = pygame.image.load(texture_path)
        self.aspect = image.get_width() / image.get_height()
        self.texture = self._upload_texture(image)

        # Constant uniforms only need to be set once.
        self.shader.use()
        self.shader.set_int("u_tex", 0)          # sampler -> texture unit 0
        self.shader.set_float("u_aspect", self.aspect)

    @staticmethod
    def _upload_texture(surf):
        """Upload a pygame surface to the GPU as an OpenGL 2D texture."""
        w, h = surf.get_size()
        data = pygame.image.tobytes(surf, "RGBA", True)   # flip to GL's origin
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)         # longitude wraps
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)  # clamp at poles
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        return tex

    def render(self, width, height, time):
        """Draw the sphere for one frame."""
        self.shader.use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.shader.set_vec2("u_res", float(width), float(height))
        self.shader.set_float("u_time", time)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)   # draw the fullscreen triangle


def main():
    width, height = 800, 600
    pygame.init()

    # Request an OpenGL 3.3 core context before creating the window.
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("HelloShader")

    # The GL context now exists, so it is safe to build GPU objects.
    texture_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "resources", "k&a+.png")
    ball = Ball(texture_path)
    glViewport(0, 0, width, height)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        ball.render(width, height, pygame.time.get_ticks() / 1000.0)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:                       # noqa: BLE001
        print("Error:", exc, file=sys.stderr)
        pygame.quit()
        sys.exit(1)
