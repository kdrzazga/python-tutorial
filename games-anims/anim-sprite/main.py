import arcade

from globals import Globals
from animated_sprite import AnimatedSprite


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Animated Sprite Example")
        arcade.set_background_color(arcade.color.WHITE)

        window = arcade.get_window()
        current_width = window.width
        current_height = window.height

        self.animated_sprite = AnimatedSprite(
            Globals.SPRITESHEET_PATH,
            position_x=current_width // 2,
            position_y=current_height // 2,
            frame_width= Globals.FRAME_WIDTH,
            frame_height=Globals.FRAME_HEIGHT,
            num_frames=Globals.NUM_FRAMES,
            frame_delay=0.2
        )

    def on_update(self, delta_time):
        self.animated_sprite.update(delta_time)

    def on_draw(self):
        #arcade.start_render()
        self.animated_sprite.draw()


def main():
    game = MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
