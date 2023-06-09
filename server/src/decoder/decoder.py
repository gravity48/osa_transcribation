from .GSM import gsm_to_wav


def postwork_decoder(f_speech, r_speech, codec_type):
    data = None
    if f_speech == b'' and r_speech == b'':
        return None
    if codec_type == 'GSM':
        data = gsm_to_wav(f_speech, r_speech)
    return data
