import io
from typing import Union

import librosa
import numpy as np
import scipy.io.wavfile as wave
import soundfile as sf
from pydub import AudioSegment as am

CHANNELS = 1
SR = 16000
SAMPLE_WIDTH = 2 # bytes

class VoiceTooShort(Exception):
    pass

def read_audio(bytedata: bytes):
    byteio = io.BytesIO(bytedata)
    audio = am.from_file(byteio)
    audio = audio.set_sample_width(2) 
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)
    audio = audio.export(format='wav')
    return io.BytesIO(audio.read())

def maybe_get_speech(bytedata: bytes):
    audio, sr = librosa.core.load(
        read_audio(bytedata),
        sr = SR,
    )
    print(len(audio)/sr)
    audio, _ = librosa.effects.trim(audio, top_db=10)
    print(len(audio)/sr)
    if librosa.get_duration(y=audio, sr=sr) < 0.5:
        raise VoiceTooShort("Audio duration is too short, must >= 0.5")
    else:
        return audio, sr

def export_wav(data, filename=None):
    if isinstance(data, bytes):
        byteio = io.BytesIO(data)
        aud, sr = librosa.load(byteio, sr=SR)
    
    elif isinstance(data, np.ndarray):
        aud = data 

    else:
        raise TypeError

    if filename:
        sf.write(filename, aud, samplerate=SR)


    byteio = io.BytesIO()
    wave.write(byteio, SR, aud)

    return byteio.read()