import arcade
from pyglet.event import EVENT_HANDLE_STATE


class AnimateAndShoot(arcade.Window):

    def __init__(self):
        super().__init__(width=800, height=600, title="Animate & screenshot")

        arcade.set_background_color(arcade.color.BLACK)
        pic1 = arcade.Sprite("pic/logoC.png")
        pic2 = arcade.Sprite("pic/upperFlag.png")
        pic3 = arcade.Sprite("pic/bottomFlag.png")

        pic1.center_x = -pic1.width*2
        pic1.center_y = pic1.height

        pic2.center_x = self.width + pic1.width*2
        pic2.center_y = self.height + pic1.height*2

        pic3.center_x = self.width + pic1.width*2
        pic3.center_y = self.height + pic1.height*2

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(pic1)
        self.sprite_list.append(pic2)
        self.sprite_list.append(pic3)

    def on_update(self, delta_time):
        self.sprite_list[0].center_x += 1

        self.sprite_list[1].center_x -= 1
        self.sprite_list[1].center_y += 1

        self.sprite_list[2].center_x -= 1
        self.sprite_list[2].center_y -= 1

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.sprite_list.draw()


if __name__ == "__main__":

    window = AnimateAndShoot()
    arcade.run()
