class Scene:
    def __init__(self, width, height, elements, background):
        self.width = width
        self.height = height
        self.elements = tuple(elements)
        self.background = background

    def render(self, painter, time):
        painter.begin_frame(self.background)
        for element in self.elements:
            element.render(painter, time)
