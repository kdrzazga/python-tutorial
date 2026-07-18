import math

import arcade
import random

from arcade import Rect

WIDTH = 800
HEIGHT = 600
NOISE_DOT_COUNT = 1000  # Total number of dots


class NoiseOverlay:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.texture = self.create_noise_texture()

def create_noise_texture(self):
	# Create a surface for the noise
	arcade.make_soft_square_texture(size=300, color=(10,10,10,128), center_alpha=255, outer_alpha=0)
	surface = arcade.TextureAnimation()
	# Draw random dots
	for _ in range(NOISE_DOT_COUNT):
		x = random.uniform(0, self.width)
		y = random.uniform(0, self.height)
		intensity = random.uniform(50, 200)  # Gray intensity
		alpha = random.uniform(50, 150)  # Transparency
		color = (int(intensity), int(intensity), int(intensity), int(alpha))
		size = random.uniform(1, 3)
		arcade.draw_circle_filled(x, y, size, color)
	return arcade.Texture('noise_texture', surface)


def draw(self):
	...


class MyGame(arcade.Window):

	def __init__(self):

		super().__init__(WIDTH, HEIGHT, "CRT Effect with Noise")
		self.frame = 0

	def on_draw(self):
		intensity = math.floor(random.uniform(50, 200))
		alpha = math.floor(random.uniform(150, 255))
		a = arcade.make_soft_square_texture(size=300, color=(intensity,intensity,intensity, alpha), center_alpha=alpha, outer_alpha=alpha-50)

		radius = 100
		alpha = -math.pi

		self.frame += 1
		bottom = 0
		f = self.frame % 200
		width = 300# + 100 * math.sin(f * math.pi/100)
		height = 300
		right = width
		top = bottom + height

		x = width // 2
		y = bottom + height // 2
		r = Rect(0, right, bottom, top, width, height, x, y)

		while alpha < math.pi:
			xc = math.floor(radius * math.sin(alpha)) + x // 2
			yc = math.floor(radius * math.cos(alpha)) + y // 2
			a.image.putpixel((xc, yc), (0, 255, 255))
			alpha += 0.01

			arcade.draw_texture_rect(a, r)


def main():

	game = MyGame()
	arcade.run()


if __name__ == "__main__":
	main()
