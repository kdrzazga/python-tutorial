class Morphing:
    def __init__(self, width, height, duration=360):
        self.width = width
        self.height = height
        self.duration = duration
        self.frame = 0
        self.background = (10, 10, 20)
        self.title = "Morphing"

    def reset(self):
        self.frame = 0

    def update(self):
        if self.frame < self.duration:
            self.frame += 1

    @property
    def progress(self):
        return self.frame / self.duration if self.duration else 1.0

    def is_complete(self):
        return self.frame >= self.duration

    def phase(self, start, end):
        progress = self.progress
        if progress <= start:
            return 0.0
        if progress >= end:
            return 1.0
        return (progress - start) / (end - start)

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def smoothstep(t):
        t = max(0.0, min(1.0, t))
        return t * t * (3 - 2 * t)

    def draw(self, surface):
        surface.fill(self.background)
        self.render(surface)

    def render(self, surface):
        pass
