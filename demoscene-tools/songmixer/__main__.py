import argparse

from .audio_io import AudioReader, AudioWriter
from .shifters import ResamplePitchShifter, PhaseVocoderPitchShifter
from .mixer import OctaveMixer


class ShifterFactory:
    def __init__(self, semitones):
        self._semitones = semitones
        self._builders = {
            "vocoder": self._build_vocoder,
            "resample": self._build_resample,
        }

    def create(self, methods):
        return tuple(self._builders[method]() for method in methods)

    def _build_vocoder(self):
        return PhaseVocoderPitchShifter(self._semitones)

    def _build_resample(self):
        return ResamplePitchShifter(self._semitones)


class CommandLine:
    def __init__(self, argv=None):
        self._argv = argv

    def run(self):
        args = self._parse()
        methods = ("vocoder", "resample") if args.method == "both" else (args.method,)
        shifters = ShifterFactory(args.semitones).create(methods)
        mixer = OctaveMixer(AudioReader(), AudioWriter(), shifters)
        for path in mixer.process(args.input, args.output_dir):
            print(path)

    def _parse(self):
        parser = argparse.ArgumentParser(prog="songmixer")
        parser.add_argument("input")
        parser.add_argument("-s", "--semitones", type=float, default=12.0)
        parser.add_argument("-m", "--method", choices=("vocoder", "resample", "both"), default="both")
        parser.add_argument("-o", "--output-dir", default=None)
        return parser.parse_args(self._argv)


def main():
    CommandLine().run()


if __name__ == "__main__":
    main()
