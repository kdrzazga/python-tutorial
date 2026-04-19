import arcade
from arcade import Sprite, SpriteList, Rect
from arcade.color import WHITE

from common import Globals


class Stage4:

	START_TIMER = 600

	def __init__(self):
		self.logo = arcade.load_texture("res/1.jpg")

	def on_draw(self, timer):

		rect = Rect(
			x=Globals.WIDTH // 2,  # center x
			y=Globals.HEIGHT // 2,  # center y
			width=self.logo.width,
			height=self.logo.height,
			left=Globals.WIDTH // 2,  # optional, defaults to x - width/2
			right=Globals.HEIGHT // 2,  # optional, defaults to x + width/2
			bottom=0,  # optional, defaults to y - height/2
			top=0  # optional, defaults to y + height/2
		)

		tr = min(2 * timer, 255)

		arcade.draw_texture_rect(
			texture=self.logo,
			rect=rect,
			color=WHITE,
			angle=0.0,
			blend=True,
			alpha=tr,
			pixelated=False
		)