import arcade

from lib import Constants
from player import PlatformPlayer, PlayerStatus


class Board:
    def __init__(self):
        self.platforms = []
        self.platforms.append(arcade.SpriteSolidColor(800, 20, arcade.color.BROWN))
        self.platforms[0].position = (400, 30)
        self.platforms.append(arcade.SpriteSolidColor(300, 20, arcade.color.BROWN))
        self.platforms[1].position = (400, 200)
        self.platforms.append(arcade.SpriteSolidColor(500, 20, arcade.color.BROWN))
        self.platforms[2].position = (400, 400)

    def draw(self):
        for platform in self.platforms:
            platform.draw()

    def platform_under(self, player: PlatformPlayer) -> bool:
        for i, platform in enumerate(self.platforms):
            if (platform.center_x - platform.width // 2 < player.center_x < platform.center_x + platform.width // 2
                    and platform.center_y - platform.height // 2 < player.center_y < platform.center_y
                    + platform.height // 2):
                print(f"Player on platform {i}")
                return True

        return False

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Platform Game")
        self.player = PlatformPlayer()
        self.board = Board()
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()
        self.handle_keys()

    def handle_keys(self):
        print(f"Platform under = {self.board.platform_under(self.player)}")

    def on_key_press(self, key, modifiers):
        self.player.info()
        if key == arcade.key.LEFT:
            if self.player.status != PlayerStatus.FALLING:
                self.player.change_x = -5

        elif key == arcade.key.RIGHT:
            if self.player.status != PlayerStatus.FALLING:
                self.player.change_x = 5
        elif key == arcade.key.UP and not self.player.jumping:
            self.player.change_y = Constants.JUMP_HEIGHT
            self.player.jumping = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
