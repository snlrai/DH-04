import streamlit as st
import tempfile
from moviepy.editor import VideoFileClip
import os
from pydub import AudioSegment

# Title of the Streamlit app
st.title("DORITOS")


# Function to convert video to audio
def video_to_audio(video_file):
    # Create a temporary file to store the video
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    # Extract audio using moviepy
    video_clip = VideoFileClip(tfile.name)
    audio_clip = video_clip.audio

    # Save the audio to a temporary file (MP3 format)
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    audio_clip.write_audiofile(audio_file.name)

    # Close and delete the temporary video file
    tfile.close()
    os.remove(tfile.name)

    return audio_file.name


# Function to convert MP3 to WAV
def mp3_to_wav(mp3_file, wav_file):
    """
    Converts an MP3 audio file to WAV format.

    Parameters:
    - mp3_file (str): Path to the input MP3 file.
    - wav_file (str): Path to save the output WAV file.
    """
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file)

    # Export the audio to WAV format
    audio.export(wav_file, format="wav")


# File uploader to accept video files
video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

# File uploader to accept audio files
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

# Check if video file is uploaded
if video_file is not None:
    # Convert video to audio
    st.write("Converting video to audio...")
    audio_file_path = video_to_audio(video_file)

    # Display the extracted audio file
    st.audio(audio_file_path)

# Check if audio file is uploaded
elif audio_file is not None:
    # Display the uploaded audio file
    st.audio(audio_file)

# Button to trigger MP3 to WAV conversion
if st.button("Convert MP3 to WAV") and audio_file is not None:
    # Get current working directory
    current_dir = os.getcwd()

    # Define output WAV file path in the current directory
    output_wav_file = os.path.join(current_dir, "converted_audio.wav")

    # Call mp3_to_wav function with uploaded audio file and output WAV file path
    mp3_to_wav(audio_file.name, output_wav_file)

    # Display confirmation message
    st.write(f"MP3 file converted to WAV. Download [converted WAV file]({output_wav_file})")
