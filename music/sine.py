import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, fs=44100):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

note_frequencies = {
    'C4': 261.63,
    'C#4': 277.18,
    'D4': 293.66,
    'D#4': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F#4': 369.99,
    'G4': 392.00,
    'G#4': 415.30,
    'A4': 440.00,
    'A#4': 466.16,
    'B4': 493.88
}

notes = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4']
duration = 0.5

print("Playing the whole scale of OCTAVE 4")
for note in notes:
    frequency = note_frequencies[note]
    print(note, end=" ", flush=True)
    sine_wave = generate_sine_wave(frequency, duration)
    sd.play(sine_wave, 44100)
    sd.wait()

print()
