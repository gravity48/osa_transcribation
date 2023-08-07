import os
import subprocess
from decoder.base import AbstractDecoder


class GsmDecoder(AbstractDecoder):
    @staticmethod
    def from_bytes_to_s16le(input_bytes: bytes) -> bytes:
        path_to_lib = f'{os.getcwd()}/replica_decoder/'
        action = f'replica_decoder/replica_decoder stdout' f' {len(input_bytes)} {path_to_lib}'
        process = subprocess.Popen(
            action,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid,
        )
        process.communicate(input_bytes)
        process.wait()
        out, err = process.communicate()
        if process.poll():
            raise subprocess.CalledProcessError(process.returncode, 'replica_decoder')
        return out

    def decode(self, f_raw_data, r_raw_data):
        f_data, r_data = b'', b''
        if f_raw_data:
            f_data = self.from_bytes_to_s16le(f_raw_data)
        if r_raw_data:
            r_data = self.from_bytes_to_s16le(r_raw_data)
        return f_data, r_data
