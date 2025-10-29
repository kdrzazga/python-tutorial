import arcade


class AnimateAndShoot(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
        pic1 = arcade.Sprite("pic/logoC.png")
        pic1.scale = 0.9
        pic2 = arcade.Sprite("pic/bottomFlag.png")
        pic3 = arcade.Sprite("pic/upperFlag.png")

        pic1.center_x = -pic1.width // 2
        pic1.center_y = pic1.height // 2

        pic2.center_x = self.width + pic2.width // 2
        pic2.center_y = - pic2.height // 2

        pic3.center_x = self.width + pic3.width // 2
        pic3.center_y = self.height + pic3.height // 2

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(pic1)
        self.sprite_list.append(pic2)
        self.sprite_list.append(pic3)

    def on_update(self, delta_time):
        if self.sprite_list[0].center_x < self.width // 2 - self.sprite_list[0].width // 2 + 30:
            self.sprite_list[0].center_x += 1

        if self.sprite_list[1].center_x > self.width // 2 + self.sprite_list[0].width // 2 - 15:
            self.sprite_list[1].center_x -= 1

        if self.sprite_list[1].center_y < self.height * 0.35 + 10:
            self.sprite_list[1].center_y += 1

        if self.sprite_list[2].center_x > self.width // 2 + self.sprite_list[0].width // 2 - 15:
            self.sprite_list[2].center_x -= 1

        if self.sprite_list[2].center_y > self.height * 0.55 + 10: #blue flag
            self.sprite_list[2].center_y -= 1

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()


if __name__ == "__main__":

    window = arcade.Window(width=800, height=600, title="Animate & screenshot")

    game = AnimateAndShoot()
    #game.setup()

    window.show_view(game)
    arcade.run()
