import os
import sys

import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "curves"))

from snowman import Snowman
from morphing import Morphing

REF_PATH = os.path.join(os.path.dirname(__file__), "snowman_drawing.png")


class SnowmanMorphing(Morphing):
    top_unit = 1.34
    bottom_unit = -1.0

    def __init__(self, width, height, duration=360):
        super().__init__(width, height, duration)
        self.title = "Snowman Morphing"
        self.scale = 240
        self.center = (width // 2, 420)

        self.snowman = Snowman(width, height)
        self.snowman.progress = 1.0
        self.snowman.scale = self.scale
        self.snowman.center = self.center
        self.snowman.show_scarf = False
        self.snowman.show_balls = False
        self.snowman.fill_background = False
        self.body_stretch = 1.25

        self.reference, self.ref_pos = self.load_reference()
        self.arm_target_width = max(6, int(self.scale * 0.05))

        self.phases = {
            "body": (0.05, 0.35),
            "arms": (0.05, 0.45),
            "scarf": (0.30, 0.60),
            "hat": (0.45, 0.70),
            "nose": (0.55, 0.80),
            "face": (0.65, 0.95),
        }

    def load_reference(self):
        image = pygame.image.load(REF_PATH).convert_alpha()
        full_height = (self.top_unit - self.bottom_unit) * self.scale
        ratio = full_height / image.get_height()
        size = (int(image.get_width() * ratio), int(full_height))
        scaled = pygame.transform.smoothscale(image, size)
        top = self.center[1] - self.top_unit * self.scale
        left = self.center[0] - size[0] // 2
        return scaled, (int(left), int(top))

    def arm_rects(self):
        w, h = self.reference.get_size()
        left, top = self.ref_pos
        bands = [(0.00, 0.34), (0.66, 1.00)]
        rects = []
        for x0, x1 in bands:
            rects.append(pygame.Rect(left + int(x0 * w), top + int(0.26 * h),
                                     int((x1 - x0) * w), int(0.22 * h)))
        return rects

    def render(self, surface):
        self.morph_body(surface)
        self.draw_base(surface)
        self.morph_arms(surface)
        self.morph_scarf(surface)
        self.morph_hat(surface)
        self.morph_nose(surface)
        self.morph_face(surface)

    def draw_base(self, surface):
        self.snowman.draw(surface)

    def morph_body(self, surface):
        p = self.phase(*self.phases["body"])
        stretch = self.lerp(1.0, self.body_stretch, self.smoothstep(p))
        white = (235, 235, 245)
        sm = self.snowman
        for outline in sm.ball_outlines:
            points = [sm.to_screen((x * stretch, y)) for x, y in outline]
            pygame.draw.polygon(surface, white, points)

    def blend_reference(self, surface, rects, alpha):
        self.reference.set_alpha(alpha)
        for rect in rects:
            surface.set_clip(rect)
            surface.blit(self.reference, self.ref_pos)
        surface.set_clip(None)
        self.reference.set_alpha(255)

    def morph_arms(self, surface):
        p = self.phase(*self.phases["arms"])
        if p <= 0.0:
            return

        grow = self.smoothstep(min(1.0, p / 0.6))
        width = int(self.lerp(3, self.arm_target_width, grow))
        brown = (120, 72, 40)
        sm = self.snowman
        for segment in (sm.left_arm, sm.right_arm, sm.left_twig, sm.right_twig):
            pygame.draw.line(surface, brown, sm.to_screen(segment[0]),
                             sm.to_screen(segment[1]), max(3, width))

        if p > 0.6:
            alpha = int(self.smoothstep((p - 0.6) / 0.4) * 255)
            self.blend_reference(surface, self.arm_rects(), alpha)

    def draw_scarf(self, surface, dy_px, thickness_scale):
        sm = self.snowman
        dy = dy_px / self.scale

        def transform(point):
            x, y = point
            return (x, y - dy)

        red = (200, 40, 50)
        width = max(3, int(max(6, int(self.scale * 0.05)) * thickness_scale))
        pygame.draw.lines(surface, red, False,
                          [sm.to_screen(transform(p)) for p in sm.scarf], width)
        pygame.draw.lines(surface, red, False,
                          [sm.to_screen(transform(p)) for p in sm.scarf_tail], width)

    def morph_scarf(self, surface):
        p = self.phase(*self.phases["scarf"])
        lower_t = self.smoothstep(min(1.0, p / 0.5))
        thick_t = self.smoothstep(max(0.0, (p - 0.5) / 0.5))
        dy_px = self.lerp(0.0, 35.0, lower_t)
        thickness_scale = self.lerp(1.0, 3.0, thick_t)
        self.draw_scarf(surface, dy_px, thickness_scale)

    def morph_hat(self, surface):
        """TODO: morph the drawn top hat into the PNG top hat."""
        pass

    def morph_nose(self, surface):
        """TODO: morph the carrot nose into the PNG nose."""
        pass

    def morph_face(self, surface):
        """TODO: morph eyes/brows/mouth into the PNG face."""
        pass
