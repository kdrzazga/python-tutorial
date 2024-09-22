import tempfile
import arcade
import base64
import os


def encode_png_to_base64(png_file_path, output_path):
    with open(png_file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(output_path, "w") as file:
        file.write(encoded_string)


def decode_base64_to_texture(textfile):
    with open(textfile, "r") as file:
        base64string = file.read()

    image_data = base64.b64decode(base64string)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(image_data)
        temp_file_path = temp_file.name

    return arcade.load_texture(temp_file_path)


class Viewer(arcade.Window):
    def __init__(self, width, height, title, texture):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.texture = texture

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2,
                                      self.texture.width, self.texture.height,
                                      self.texture)


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    texture = decode_base64_to_texture(os.path.join(root_dir, "..//..//resources", "barbar.txt"))
    game = Viewer(134, 237, "Base64 PNG Viewer", texture)
    arcade.run()


if __name__ == '__main__':
    main()
