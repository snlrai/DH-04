import streamlit as st
import tempfile
from moviepy.editor import VideoFileClip
import os
from IPython.display import Audio
from scipy.io import wavfile
import numpy as np
import subprocess

import os

from IPython.display import Audio
from scipy.io import wavfile
import numpy as np
import streamlit as st

import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

st.title("DORITOS")

current_dir = os.getcwd()


def video_to_audio(video_file):
    video_temp_path = os.path.join(current_dir, "temp_video.mp4")
    with open(video_temp_path, "wb") as f:
        f.write(video_file.read())

    video_clip = VideoFileClip(video_temp_path)
    audio_clip = video_clip.audio

    audio_temp_path = os.path.join(current_dir, "temp_audio.wav")
    audio_clip.write_audiofile(audio_temp_path)

    # os.remove(video_temp_path)
    return audio_temp_path


video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
if video_file is not None:
    # Convert video to audio
    st.write("Converting video to audio...")
    audio_file_path = video_to_audio(video_file)

    # Display the extracted audio file
    st.audio(audio_file_path)

current_dir = os.getcwd()
file_name = os.path.join(current_dir, 'temp_audio.wav')
data = wavfile.read(file_name)
framerate = data[0]
sounddata = data[1]
time = np.arange(0, len(sounddata)) / framerate
# st.write('Sample rate:', framerate, 'Hz')
# st.write('Total time:', len(sounddata) / framerate, 's')

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
input_audio, _ = librosa.load(file_name,
                              sr=16000)
input_values = tokenizer(input_audio, return_tensors="pt").input_values
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = tokenizer.batch_decode(predicted_ids)[0]

st.write(transcription)
file_path = os.path.join(current_dir, "output.txt")

with open(file_path, "w") as file:
    file.write(transcription)