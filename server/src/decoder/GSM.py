import os
import subprocess


def from_bytes_to_bytes(
    input_bytes: bytes,
    action=f"/usr/bin/ffmpeg -loglevel error -hide_banner -i pipe:.amr -f wav -ac 1 -ar 16000 pipe:1",
):
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
    return out


def from_bytes_to_s16le(input_bytes: bytes):
    path_to_lib = f'{os.getcwd()}/replica_decoder/'
    action = f"replica_decoder/replica_decoder stdout {len(input_bytes)} {path_to_lib}"
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


def from_s16le_to_wav(input_bytes: bytes):
    action = f"/usr/bin/ffmpeg -loglevel error -hide_banner -f s16le -ac 1 -ar 8000 -i pipe:0 -f wav -ac 1 -ar 8000 pipe:1"
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
    return out


def gsm_decoder(speech_gsm):
    s16le = from_bytes_to_s16le(speech_gsm)
    return s16le


def gsm_to_wav(f_speech, r_speech):
    if f_speech:
        f_speech_wav = gsm_decoder(f_speech)
    else:
        f_speech_wav = b''
    if r_speech:
        r_speech_wav = gsm_decoder(r_speech)
    else:
        r_speech_wav = b''
    return f_speech_wav, r_speech_wav
