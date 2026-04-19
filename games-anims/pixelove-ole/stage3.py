import math

from arcade import Sprite, SpriteList
from common import Globals


class Stage3:

	START_TIMER = 446

	def __init__(self):
		slide1 = Sprite("res/slideshow/party (1).jpeg")
		slide2 = Sprite("res/slideshow/party (2).jpeg")
		slide3 = Sprite("res/slideshow/party (3).jpeg")
		slide4 = Sprite("res/slideshow/party (4).jpeg")
		slide5 = Sprite("res/slideshow/party (5).jpeg")
		slide6 = Sprite("res/slideshow/party (6).jpeg")

		self.slides = SpriteList()
		all_slides = (slide1, slide2, slide3, slide4, slide5, slide6)

		for slide in all_slides:
			self.slides.append(slide)

	def on_draw(self, timer):
		base_angle = (timer - Stage3.START_TIMER)*math.pi/50
		#base_angle = base_angle % 6.28

		for i, slide in enumerate(self.slides):
			self.slides[i].scale = 0.3
			angle = (1+i) * base_angle/len(self.slides)
			radius = 400
			x1 = Globals.WIDTH // 2 + radius * math.sin(angle)
			y1 = Globals.HEIGHT // 2 + radius * math.cos(angle)
			self.slides[i].center_x = x1
			self.slides[i].center_y = y1

		self.slides.draw()

		print(base_angle, end=' ')
