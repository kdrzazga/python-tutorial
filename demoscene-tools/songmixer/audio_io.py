import os

import numpy as np
import soundfile as sf

from .audio_clip import AudioClip


class AudioReader:
    def __init__(self, supported=(".wav", ".mp3")):
        self._supported = tuple(extension.lower() for extension in supported)

    @property
    def supported(self):
        return self._supported

    def load(self, path):
        extension = os.path.splitext(path)[1].lower()
        if extension not in self._supported:
            raise ValueError("unsupported input format: {0}".format(extension))
        samples, sample_rate = sf.read(path, dtype="float64", always_2d=False)
        return AudioClip(samples, sample_rate)


class AudioWriter:
    def __init__(self, subtype="PCM_16"):
        self._subtype = subtype

    @property
    def subtype(self):
        return self._subtype

    def save(self, clip, path):
        data = np.clip(clip.samples, -1.0, 1.0)
        sf.write(path, data, clip.sample_rate, subtype=self._subtype)
        return path
