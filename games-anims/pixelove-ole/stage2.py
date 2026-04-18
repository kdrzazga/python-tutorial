import arcade

from common import Globals


class Stage2(arcade.Window):

    def __init__(self):
        super().__init__(Globals.WIDTH, Globals.HEIGHT, "DEMO")
        self.set_fullscreen(Globals.fullscreen)
        self.timer = 0

        invite_speech = arcade.load_sound("res/invite.mp3")
        self.media_player = invite_speech.play()
        self.media_player.loop = False

