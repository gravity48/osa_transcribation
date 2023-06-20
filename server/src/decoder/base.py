from typing import Tuple


class S16LE(bytes):
    ...


class AbstractDecoder:
    def decode(self, f_raw_data: bytes, r_raw_data: bytes) -> Tuple[S16LE, S16LE]:
        """
        f_raw_data and r_raw_data - data from database_sprut
        :return Tuple decoded data to s16le
        """
        raise NotImplementedError()
