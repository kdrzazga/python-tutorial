class WindowPanel:
    def __init__(self, corner_points, is_illuminated):
        self.corner_points = corner_points
        self.is_illuminated = is_illuminated

    def render_using(self, renderer, palette):
        if self.is_illuminated:
            renderer.render_emissive_quad(self.corner_points, palette.lit_window_color)
        else:
            renderer.render_shaded_quad(self.corner_points, palette.unlit_window_color)
