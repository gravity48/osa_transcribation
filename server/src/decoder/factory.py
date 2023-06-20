from decoder.base import AbstractDecoder
from decoder.GSM import GsmDecoder


class DecoderFactory:
    decoders = {'GSM': GsmDecoder}

    def get_decoder(self, codec: str) -> AbstractDecoder:
        decoder = self.decoders.get(codec, None)
        if not decoder:
            raise ValueError('codec not found')
        return decoder()
