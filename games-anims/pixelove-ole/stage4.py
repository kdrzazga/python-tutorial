import random
import arcade
from arcade import Rect
from arcade.color import WHITE, CYAN, MAGENTA, YELLOW, RED, GREEN

from common import Globals


class Stage4:

	START_TIMER = 600

	def __init__(self):
		self.logo = arcade.load_texture("res/1.jpg")

	def on_draw(self, timer):
		y_shift = 50
		timer -= Stage4.START_TIMER

		rect = Rect(
			x=Globals.WIDTH // 2,  # center x
			y=y_shift + Globals.HEIGHT // 2,  # center y
			width=self.logo.width,
			height=self.logo.height,
			left=Globals.WIDTH // 2,  # optional, defaults to x - width/2
			right=Globals.HEIGHT // 2,  # optional, defaults to x + width/2
			bottom=0,  # optional, defaults to y - height/2
			top=0  # optional, defaults to y + height/2
		)

		tr = min(12 * timer, 255)

		arcade.draw_texture_rect(
			texture=self.logo,
			rect=rect,
			color=WHITE,
			angle=0.0,
			blend=True,
			alpha=tr,
			pixelated=False
		)

		if timer > 7:
			self.display_caption(timer, y_shift)

	def display_caption(self, timer, y_shift):

		arcade.draw_text("Ekipa i przyjaciele", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=CYAN, font_size=60,
	                 anchor_x="center")
		t = timer % 30
		if 0 < t < 6 or 21 < t < 25:
			arcade.draw_text("TECT", 0.59 * Globals.WIDTH, y_shift + 505 + random.randint(0,3), color=CYAN, font_size=20, anchor_x="center")
		if 3 < t < 9 or 25 < t < 29:
			arcade.draw_text("Michal", 0.72 * Globals.WIDTH, y_shift + 505 + random.randint(0,3), color=RED, font_size=18, anchor_x="center")
		if 2 < t < 8:
			arcade.draw_text("SMOK", 0.33 * Globals.WIDTH, y_shift + 490 + random.randint(0,3), color=YELLOW, font_size=33, anchor_x="center")
		if 6 < t < 10:
			arcade.draw_text("Borg", 0.5 * Globals.WIDTH, y_shift + 508 + random.randint(0, 3), color=WHITE, font_size=20,
		                 anchor_x="center")
		if 14 < t < 21:
			arcade.draw_text("Brodaty", 0.52 * Globals.WIDTH, y_shift + 386 + random.randint(0, 3), color=MAGENTA, font_size=15,
		                 anchor_x="center")
			arcade.draw_text("Gracz", 0.52 * Globals.WIDTH, y_shift + 368 + random.randint(0, 3), color=MAGENTA, font_size=15,
		                 anchor_x="center")
		if 18 < t < 26:
			arcade.draw_text("MFX", 0.435 * Globals.WIDTH, y_shift + 508 + random.randint(0, 3), color=GREEN, font_size=20,
		                 anchor_x="center")
