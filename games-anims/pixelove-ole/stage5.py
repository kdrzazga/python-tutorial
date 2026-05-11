import arcade
import sys
import os

from datetime import datetime

from arcade import Rect
from arcade.color import CYAN, ORANGE, WHITE, YELLOW, GREEN, ARCADE_YELLOW, AQUA, BLACK

from lib.tunnel import TunnelEffect
from lib.common import Globals


class Stage5:

	START_TIMER = 700

	def on_draw(self, timer):
		self.display_text(timer)

	def display_text(self, timer):
		t = timer - Stage5.START_TIMER

		x = 0.5 * Globals.WIDTH
		y = Globals.HEIGHT - 82

		arcade.draw_text("Pozdrowienia", x, y, color=CYAN, font_size=60, anchor_x="center")