import numpy as np


class AudioClip:
    def __init__(self, samples, sample_rate):
        self._samples = np.asarray(samples, dtype=np.float64)
        self._sample_rate = int(sample_rate)

    @property
    def samples(self):
        return self._samples

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def length(self):
        return self._samples.shape[0]

    @property
    def channel_count(self):
        return 1 if self._samples.ndim == 1 else self._samples.shape[1]

    @property
    def channels(self):
        if self._samples.ndim == 1:
            return (self._samples,)
        return tuple(self._samples[:, index] for index in range(self._samples.shape[1]))

    @classmethod
    def from_channels(cls, channels, sample_rate):
        channels = tuple(channels)
        if len(channels) == 1:
            return cls(channels[0], sample_rate)
        return cls(np.column_stack(channels), sample_rate)
