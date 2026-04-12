import arcade

from arcade import Rect
from arcade.color import WHITE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Animated Sprite Example"

SPRITESHEET_PATH = "mikolaje.png"
FRAME_WIDTH = 266
FRAME_HEIGHT = 500
NUM_FRAMES = 3


class AnimatedSprite:
    def __init__(self, spritesheet_path, position_x, position_y, frame_width, frame_height, num_frames, frame_delay=0.2):
        self.spritesheet = arcade.load_texture(spritesheet_path)
        self.frames = []
        for i in range(num_frames):
            x = i * frame_width
            y = 0
            # cut area (x, y, x + frame_width, y + frame_height)  from self.spritesheet
            frame = self.spritesheet.crop(x, y, frame_width, frame_height)
            self.frames.append(frame)

        self.sprite = arcade.Sprite()
        self.sprite.texture = self.frames[0]
        self.sprite.center_x = position_x
        self.sprite.center_y = position_y
        self.current_frame = 0
        self.frame_delay = frame_delay
        self.time_since_last_frame = 0

    def update(self, delta_time):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.sprite.texture = self.frames[self.current_frame]
            self.time_since_last_frame = 0
            print("texture chnge")


    def draw(self):
        rect = Rect(
            x=SCREEN_WIDTH // 2,  # center x
            y=SCREEN_HEIGHT // 2,  # center y
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            left=SCREEN_WIDTH // 2,  # optional, defaults to x - width/2
            right=SCREEN_HEIGHT // 2,  # optional, defaults to x + width/2
            bottom=0,  # optional, defaults to y - height/2
            top=0  # optional, defaults to y + height/2
        )

        arcade.draw_texture_rect(
            texture=self.sprite.texture,
            rect=rect,
            color=WHITE,
            angle=0.0,
            blend=True,
            alpha=255,
            pixelated=False
        )


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.animated_sprite = AnimatedSprite(
            SPRITESHEET_PATH,
            position_x=SCREEN_WIDTH // 2,
            position_y=SCREEN_HEIGHT // 2,
            frame_width=FRAME_WIDTH,
            frame_height=FRAME_HEIGHT,
            num_frames=NUM_FRAMES,
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
