import math

import arcade
from arcade.types import Color

from isosine import IsometricSineTunnel

class IsometricSineView(arcade.Window):
    def __init__(self):
        super().__init__(width=800, height=600, title="Vertical Isometric Sine Curve")

        self.kurwes = []
        for i in range(254):
            sine = IsometricSineTunnel(Color(abs(i - 128), 128, int(255 * math.sin(i / 20))), angle_deg=int(370 * i / 255))
            self.kurwes.append(sine)

        self.amplitude = 15
        self.frequency = 0.05
        self.speed = 160
        self.horizon_x = self.width * 0.01

    def on_draw(self):
        self.clear()
        for sine in self.kurwes:
            sine.draw(
                surface_width=self.width*2,
                surface_height=self.height*2-0*200,
                amplitude=self.amplitude,
                frequency=self.frequency,
                horizon_x=self.horizon_x
            )

    def on_update(self, delta_time):
        for sine in self.kurwes:
            sine.update(delta_time, self.speed)

def main():
    window = IsometricSineView()
    arcade.run()


if __name__ == "__main__":
    main()
