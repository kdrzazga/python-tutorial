import arcade
import numpy as np
import sounddevice as sd

# Function to generate and play a sine wave beep
def play_beep(frequency=440, duration=0.25, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(audio, sample_rate)
    sd.wait()

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Arcade Sine Wave Beep Example")
        self.background_color = arcade.color.WHITE

    def on_key_press(self, key, modifiers):
        key_multipliers = {
            arcade.key.SPACE: 1,
            arcade.key.ENTER: 2,
            arcade.key.UP: 3,
            arcade.key.DOWN: 4
        }
        
        if key in key_multipliers:
            multiplier = key_multipliers[key]
            frequency = 440 * multiplier
            play_beep(frequency)

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
