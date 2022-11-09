import io
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence
from pydub.exceptions import CouldntDecodeError


def get_duration(stream):
    try:
        sound = AudioSegment(stream)
        audio_chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=-45, keep_silence=50)
        combined = AudioSegment.empty()
        for chunk in audio_chunks:
            combined += chunk
        return combined.duration_seconds
    except EOFError:
        return 0
    except CouldntDecodeError:
        return 0


def format_text(f_text, r_text, model_name):
    text_out = f'\r\n -------------{model_name}-------------- '
    text_out += f'\r\nR_Channel: {r_text} \r\nF_Channel: {f_text}'
    return text_out


def silens_split(stream):
    try:
        combined = AudioSegment.empty()
        sound = AudioSegment(stream,  channels=1, frame_rate=8000, sample_width=2)
        audio_chunks = split_on_silence(sound, min_silence_len=2000, silence_thresh=-45, keep_silence=True)
        normalize_chunks = []
        for chunk in audio_chunks:
            chunk = effects.normalize(chunk)
            normalize_chunks.append(chunk)
            combined += chunk
        #combined.export('555.wav', format='wav')
        #sound.export('555.wav', format='wav')
        return combined.duration_seconds, normalize_chunks
    except Exception as e:
        return 0, None


def get_durations(stream_f, stream_r, active_time):
    f_duration, f_chunk = silens_split(stream_f)
    r_durations, r_chunk = silens_split(stream_r)
    if (f_duration < active_time) and (r_durations < active_time):
        return False, None
    else:
        return True, (f_chunk, r_chunk)


def search_keywords_in_list(keywords, words):
    find_string = ''
    for keyword in keywords:
        if keyword in words:
            find_string += f'{keyword} '
    return find_string
