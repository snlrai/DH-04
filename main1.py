import streamlit as st
import tempfile
from moviepy.editor import VideoFileClip
import os
from IPython.display import Audio
from scipy.io import wavfile
import numpy as np
import subprocess

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

if st.button("submit"):
    subprocess.run(["python","main2.py"])