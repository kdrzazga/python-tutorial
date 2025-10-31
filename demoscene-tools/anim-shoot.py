import arcade

from datetime import datetime


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

        self.logo_sprite_list = arcade.SpriteList()
        self.logo_sprite_list.append(pic1)
        self.logo_sprite_list.append(pic2)
        self.logo_sprite_list.append(pic3)

        caption1 = arcade.Sprite("pic/historia.png")
        caption2 = arcade.Sprite("pic/gier.png")
        caption3 = arcade.Sprite("pic/commodore.png")
        caption4 = arcade.Sprite("pic/64.png")

        all_captions = [caption4, caption3, caption2, caption1]

        self.caption_sprite_list = arcade.SpriteList()

        center_y = 250
        for caption in all_captions:
            caption.center_x = self.width // 2
            caption.center_y = center_y
            center_y += 100
            caption.scale = 0.01
            self.caption_sprite_list.append(caption)

        self.whole_intro_screen_list = arcade.SpriteList()
        whole_intro_screen = arcade.Sprite("pic/logo+caption.png")
        whole_intro_screen.center_x = self.width // 2
        whole_intro_screen.center_y = self.height // 2
        whole_intro_screen.scale = 0.7
        self.whole_intro_screen_list.append(whole_intro_screen)

        self.counter = 0
        self.counter_caption_start = 444
        self.counter_caption_end = self.counter_caption_start + 195
        self.index = 0

        self.music = arcade.load_sound("sfx/intro1.wav")
        self.player = self.music.play(volume=1.0)

    def on_update(self, delta_time):

        print(datetime.now())
        self.anim_logo()

        if self.counter_caption_start < self.counter < self.counter_caption_end:
            self.anim_caption()
        elif self.counter >= self.counter_caption_end + 500:
            pass#self.screen_goes_down()

    def anim_caption(self):
        for caption in self.caption_sprite_list:
            if caption.scale[0] < 1:
                s = caption.scale[0]
                s += 0.01
                caption.scale = s

    def anim_logo(self):
        self.counter += 1
        if self.counter % 2 == 0:
            self.index += 1
            self.take_screenshot()
        if self.logo_sprite_list[0].center_x < self.width // 2 - self.logo_sprite_list[0].width // 2 + 30:
            self.logo_sprite_list[0].center_x += 1
        if self.logo_sprite_list[1].center_x > self.width // 2 + self.logo_sprite_list[0].width // 2 - 15:
            self.logo_sprite_list[1].center_x -= 1
        if self.logo_sprite_list[1].center_y < self.height * 0.35 + 10:
            self.logo_sprite_list[1].center_y += 1
        if self.logo_sprite_list[2].center_x > self.width // 2 + self.logo_sprite_list[0].width // 2 - 15:
            self.logo_sprite_list[2].center_x -= 1
        if self.logo_sprite_list[2].center_y > self.height * 0.55 + 10:  # blue flag
            self.logo_sprite_list[2].center_y -= 1

    def on_draw(self):
        self.clear()
        if self.counter < self.counter_caption_end:
            self.logo_sprite_list.draw()
        else:
            self.screen_goes_down()

        if self.counter > self.counter_caption_start:
            self.caption_sprite_list.draw()

    def take_screenshot(self):
        image = arcade.get_image()
        image.save("screenshots./" + str(self.index) + ".png")

    def screen_goes_down(self):
        self.whole_intro_screen_list[0].center_y += 1


if __name__ == "__main__":

    window = arcade.Window(width=850, height=600, title="Animate & screenshot")

    game = AnimateAndShoot()
    window.show_view(game)
    arcade.run()
