import arcade
import sys

from datetime import datetime
from arcade.color import CYAN, ORANGE, WHITE, YELLOW, GREEN, ARCADE_YELLOW, AQUA, BLACK

from lib.tunnel import TunnelEffect
from lib.common import Globals


class Stage5:

	START_TIMER = 700

	def __init__(self):
		self.logo = arcade.load_texture("res/1.jpg")
		arcade.set_background_color(arcade.color.BLACK)
		self.effect = TunnelEffect(9)

	def on_draw(self, timer):
		self.effect.draw()
		self.effect.update()
		self.display_text(timer)

	def display_text(self, timer):
		t = timer - Stage5.START_TIMER
		duration = 11
		print(t)
		if 2 < t < 2 + duration:
			arcade.draw_text("Commodore 64", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=CYAN, font_size=60,
		                 anchor_x="center")

		elif 2 + duration + 2 < t < 2 + 2*duration + 2:
			arcade.draw_text("Atari 800", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=ORANGE, font_size=60,
		                 anchor_x="center")

		elif 2 + 2*duration + 4 < t < 2 + 3*duration + 2:
			arcade.draw_text("Amiga 500", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=WHITE, font_size=60,
		                 anchor_x="center")

		elif 2 + 3*duration + 4 < t < 2 + 4*duration + 2:
			arcade.draw_text("Amstrad", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=YELLOW, font_size=60,
		                 anchor_x="center")

		elif 2 + 4*duration + 4 < t < 2 + 5*duration + 2:
			arcade.draw_text("NES", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=GREEN, font_size=60,
		                 anchor_x="center")

		elif 2 + 5*duration + 4 < t < 2 + 6*duration + 2:
			arcade.draw_text("Playstation", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=AQUA, font_size=60,
		                 anchor_x="center")

		elif 2 + 6*duration + 4 < t < 2 + 7*duration + 2:
			arcade.draw_text("VIC-20", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=ARCADE_YELLOW, font_size=60,
		                 anchor_x="center")

		elif  2 + 9*duration + 2 < t < 12.5 * duration:
			arcade.draw_text("Pixelove OLE", 0.5 * Globals.WIDTH, Globals.HEIGHT - 82, color=BLACK, font_size=77,
		                 anchor_x="center")
			arcade.draw_text("23.07.2026", 0.5 * Globals.WIDTH, Globals.HEIGHT - 192, color=BLACK, font_size=99,
		                 anchor_x="center")
			arcade.draw_text("Lotnisko w Spalicach", 0.5 * Globals.WIDTH, Globals.HEIGHT//3, color=BLACK, font_size=66,
		                 anchor_x="center")

		elif t > 13*duration:
			dur = datetime.now() - Globals.start
			print("Invitro duration: " + str(dur))
			sys.exit(0)
