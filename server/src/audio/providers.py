from typing import List, Tuple

from decoder.base import S16LE
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence

from .base import AbstractProvider, WavBytesIO


class PydubProvider(AbstractProvider):
    options = {'channels': 1, 'frame_rate': 8000, 'sample_width': 2}

    def get_durations(self, stream: S16LE) -> int:
        sound = AudioSegment(stream, **self.options)
        return sound.duration_seconds

    @staticmethod
    def _wav_export(chunks: List[AudioSegment]) -> List[WavBytesIO]:
        wav_raw_data = []
        for chunk in chunks:
            stream = WavBytesIO()
            chunk.export(stream, format='wav')
            wav_raw_data.append(stream)
        return wav_raw_data

    def silence_split(self, stream: S16LE, *args, **kwargs) -> Tuple[int, List[WavBytesIO]]:
        if not stream:
            return 0, []
        sound = AudioSegment(
            stream,
            **self.options,
        )
        chunks = split_on_silence(
            sound,
            min_silence_len=2000,
            silence_thresh=-45,
            keep_silence=2000,
        )
        if kwargs.get('normalize'):
            chunks = [effects.normalize(chunk) for chunk in chunks]
        chunk_duration_seconds = sum([chunk.duration_seconds for chunk in chunks])
        return chunk_duration_seconds, self._wav_export(chunks)
