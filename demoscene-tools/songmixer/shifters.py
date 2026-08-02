from abc import ABC, abstractmethod

import numpy as np

from .audio_clip import AudioClip


class PitchShifter(ABC):
    def __init__(self, semitones=12.0):
        self._semitones = float(semitones)

    @property
    def semitones(self):
        return self._semitones

    @property
    def ratio(self):
        return 2.0 ** (self._semitones / 12.0)

    @property
    @abstractmethod
    def suffix(self):
        raise NotImplementedError

    @abstractmethod
    def shift(self, clip):
        raise NotImplementedError

    @staticmethod
    def _resample(signal, ratio):
        signal = np.asarray(signal, dtype=np.float64)
        if ratio == 1.0:
            return signal
        length = signal.shape[0]
        new_length = int(np.floor(length / ratio))
        if new_length <= 1:
            return signal[:1]
        positions = np.arange(new_length) * ratio
        return np.interp(positions, np.arange(length), signal)


class ResamplePitchShifter(PitchShifter):
    @property
    def suffix(self):
        return "resample"

    def shift(self, clip):
        ratio = self.ratio
        shifted = tuple(self._resample(channel, ratio) for channel in clip.channels)
        return AudioClip.from_channels(shifted, clip.sample_rate)


class PhaseVocoderPitchShifter(PitchShifter):
    def __init__(self, semitones=12.0, frame_size=2048, hop_size=512):
        super().__init__(semitones)
        self._frame_size = int(frame_size)
        self._hop_size = int(hop_size)
        self._window = np.hanning(self._frame_size)

    @property
    def suffix(self):
        return "vocoder"

    def shift(self, clip):
        ratio = self.ratio
        length = clip.length
        shifted = tuple(
            self._fit(self._resample(self._stretch(channel, 1.0 / ratio), ratio), length)
            for channel in clip.channels
        )
        return AudioClip.from_channels(shifted, clip.sample_rate)

    def _fit(self, signal, length):
        if signal.shape[0] >= length:
            return signal[:length]
        padded = np.zeros(length, dtype=np.float64)
        padded[: signal.shape[0]] = signal
        return padded

    def _stretch(self, signal, rate):
        signal = np.asarray(signal, dtype=np.float64)
        if rate == 1.0 or signal.shape[0] < self._frame_size:
            return signal
        spectrum = self._stft(signal)
        stretched = self._phase_vocoder(spectrum, rate)
        return self._istft(stretched)

    def _stft(self, signal):
        frame = self._frame_size
        hop = self._hop_size
        pad = frame // 2
        padded = np.pad(signal, pad, mode="reflect")
        frame_count = 1 + (padded.shape[0] - frame) // hop
        indices = np.arange(frame)[:, None] + hop * np.arange(frame_count)[None, :]
        windowed = padded[indices] * self._window[:, None]
        return np.fft.rfft(windowed, axis=0)

    def _istft(self, spectrum):
        frame = self._frame_size
        hop = self._hop_size
        frames = np.fft.irfft(spectrum, n=frame, axis=0)
        frame_count = spectrum.shape[1]
        length = frame + hop * (frame_count - 1)
        output = np.zeros(length, dtype=np.float64)
        weights = np.zeros(length, dtype=np.float64)
        squared = self._window ** 2
        for index in range(frame_count):
            start = index * hop
            output[start : start + frame] += frames[:, index] * self._window
            weights[start : start + frame] += squared
        weights = np.where(weights < 1e-8, 1e-8, weights)
        output = output / weights
        pad = frame // 2
        return output[pad : output.shape[0] - pad]

    def _phase_vocoder(self, spectrum, rate):
        bins = spectrum.shape[0]
        steps = np.arange(0.0, spectrum.shape[1], rate)
        stretched = np.zeros((bins, steps.shape[0]), dtype=complex)
        expected = np.linspace(0.0, np.pi * self._hop_size, bins)
        accumulator = np.angle(spectrum[:, 0])
        padded = np.concatenate([spectrum, np.zeros((bins, 2), dtype=complex)], axis=1)
        for index, step in enumerate(steps):
            base = int(step)
            columns = padded[:, base : base + 2]
            alpha = step - base
            magnitude = (1.0 - alpha) * np.abs(columns[:, 0]) + alpha * np.abs(columns[:, 1])
            stretched[:, index] = magnitude * np.exp(1j * accumulator)
            advance = np.angle(columns[:, 1]) - np.angle(columns[:, 0]) - expected
            advance = advance - 2.0 * np.pi * np.round(advance / (2.0 * np.pi))
            accumulator = accumulator + expected + advance
        return stretched
