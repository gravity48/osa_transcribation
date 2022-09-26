import bitarray
import subprocess
import os
import shlex
from decoder.AMR_transcoding import AMR_244, AMR_148, AMR_159, AMR_204, AMR_134, AMR_118, AMR_103, AMR_95

period_from_speed = {
    '111': (244, AMR_244),
    '011': (204, AMR_204),
    '101': (159, AMR_159),
    '001': (148, AMR_148),
    '110': (134, AMR_134),
    '010': (118, AMR_118),
    '100': (103, AMR_103),
    '000': (95, AMR_95),
}


def from_bytes_to_bytes(
        input_bytes: bytes,
        action=f"/usr/bin/ffmpeg -loglevel error -hide_banner -i pipe:.amr -f wav -ac 1 -ar 16000 pipe:1"):
    process = subprocess.Popen(action, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    process.communicate(input_bytes)
    process.wait()
    out, err = process.communicate()
    return out


def from_bytes_to_wav(input_bytes: bytes,
                      action=f"/usr/bin/ffmpeg -i pipe:.amr -f wav -ac 1 -ar 16000 test123.wav"):
    process = subprocess.Popen(action, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    process.communicate(input_bytes)
    process.wait()
    return


def gsm_decoder(speech_gsm):
    output_file = b''
    header = b'\x23\x21\x41\x4D\x52\x0A'
    output_file += header
    # file_output = open('test50.amr', 'wb')
    # file_output.write(header)
    pause_number = 0
    for item in range(0, len(speech_gsm), 34):
        delta_bytes = speech_gsm[item:item + 34]
        if delta_bytes[-1] == 0x18 and delta_bytes[-2] == 0x30:
            continue
        if delta_bytes[-1] == 0x18 and delta_bytes[-2] == 0x10:
            continue
        delta_bit = bitarray.bitarray()
        delta_bit.frombytes(delta_bytes)
        if delta_bit[264]:
            pause_number += 1
        else:
            pause_number = 0
        if pause_number >= 10:
            continue
        speed = str(delta_bit[256]) + str(delta_bit[271]) + str(delta_bit[270])
        package_header = '001' + speed + '00'
        package_header = bitarray.bitarray(package_header)
        try:
            period, AMR = period_from_speed[speed]
        except KeyError:
            continue
        data = delta_bit[0:period]
        data.bytereverse()
        transposition = bitarray.bitarray(period)
        for position in range(period):
            transposition[position] = data[AMR[position]]
        transposition.bytereverse()
        package = package_header + transposition
        package.bytereverse()
        output_file += package.tobytes()
        # package.tofile(file_output)
    # file_output.close()
    result = from_bytes_to_bytes(output_file)
    #from_bytes_to_wav(output_file)
    return result


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
