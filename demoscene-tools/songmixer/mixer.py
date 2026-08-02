import os


class OctaveMixer:
    def __init__(self, reader, writer, shifters):
        self._reader = reader
        self._writer = writer
        self._shifters = tuple(shifters)

    @property
    def shifters(self):
        return self._shifters

    def process(self, input_path, output_dir=None):
        clip = self._reader.load(input_path)
        outputs = []
        for shifter in self._shifters:
            shifted = shifter.shift(clip)
            output_path = self._output_path(input_path, shifter.suffix, output_dir)
            self._writer.save(shifted, output_path)
            outputs.append(output_path)
        return tuple(outputs)

    def _output_path(self, input_path, suffix, output_dir):
        directory = output_dir if output_dir is not None else os.path.dirname(os.path.abspath(input_path))
        stem = os.path.splitext(os.path.basename(input_path))[0]
        return os.path.join(directory, "{0}_{1}.wav".format(stem, suffix))
