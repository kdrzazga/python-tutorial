import arcade

from globals import Globals
from animated_sprite import AnimatedSprite


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, Globals.SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.animated_sprite = AnimatedSprite(
            Globals.SPRITESHEET_PATH,
            position_x=Globals.SCREEN_WIDTH // 2,
            position_y=Globals.SCREEN_HEIGHT // 2,
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
