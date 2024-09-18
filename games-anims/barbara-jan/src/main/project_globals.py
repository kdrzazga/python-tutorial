import os


class Constants:
    SCREEN_WIDTH = 1152
    SCREEN_HEIGHT = 854

    LIGHT_BLUE = (96, 96, 192)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BROWN = (185, 122, 85)
    PURPLE = (200, 130, 200)
    YELLOW = (255, 255, 0)
    BLUE = (32, 0, 128)


class Utils:
    color_index = 0

    @staticmethod
    def get_next_color():
        available_colors = (
            Constants.GREEN, Constants.WHITE, Constants.CYAN, Constants.RED, Constants.YELLOW, (34, 177, 76),
            Constants.BLUE, Constants.PURPLE, Constants.BROWN)
        Utils.color_index = (Utils.color_index + 1) % len(available_colors)
        return available_colors[Utils.color_index]

    @staticmethod
    def color_texture(texture, old_color, new_color):
        width = texture.width
        height = texture.height

        pixels = texture.image.getdata()
        new_pixels = []

        for y in range(height):
            for x in range(width):
                r, g, b, _ = texture.image.getpixel((x, y))

                if (r, g, b) == old_color:
                    texture.image.putpixel((x, y), (new_color[0], new_color[1], new_color[2], 255))

        return texture


class Globals:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    version = "normal"
    woman_image_path = root_dir + "\\..\\..\\resources\\"
