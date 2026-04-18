import math
import os

import arcade
from arcade import Sprite
from arcade.color import CYAN

from common import Globals
from datetime import datetime


class Stage2:

    ACTIVE = False

    def __init__(self, timer):

        invite_speech = arcade.load_sound("res/invite.mp3")
        Stage2.ACTIVE = True

        self.media_player = invite_speech.play()
        self.media_player.loop = False

        self.stripe = Sprite("res/stripe.jpg")
        self.stripe.center_x = Globals.WIDTH//2
        self.stripe.center_y = Globals.HEIGHT - self.stripe.height//2

        self.stripe2 = Sprite("res/stripe.jpg")
        self.stripe2.center_x = -Globals.WIDTH//2
        self.stripe2.center_y = 3*self.stripe2.height//2

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.stripe)
        self.sprite_list.append(self.stripe2)

        print(datetime.now() - Globals.start)

    def on_draw(self, timer):

        lines = ("Serdecznie zapraszamy na imprezę Pixelove Ole w mieście Oleśnica!",
                 " To wyjątkowa okazja, aby powrócić do czasów retro i zanurzyć się ",
                 "w świecie klasycznych komputerów i konsol.",
                 " Przyjdź 23 lipca 2026 roku i spędź niezapomniany dzień pełen gier,",
                 " muzyki i wspomnień!",
                 " Czekamy na Ciebie, ty głupi poyebie!")

        font_size = 22

        for i, line in enumerate(lines):
            font_path = os.getcwd() + "res/C64_Pro_Mono-STYLE.ttf"
            y = 11*Globals.HEIGHT//16 - i * 1.2*font_size + 5*timer/6 - 200

            print(timer)

            arcade.draw_text(line, 0.5 * Globals.WIDTH, y, color=CYAN,
                             font_size=font_size
                             , font_name=font_path, anchor_x="center")

        self.sprite_list.draw()
        self.sprite_list[0].center_x -= 1
        self.sprite_list[1].center_x += 1

