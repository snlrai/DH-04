import os

current_dir = os.getcwd(
transcription = "Samridhi is Dumb"
file_path = os.path.join(current_dir, "output.txt")

with open(file_path, "w") as file:
    file.write(transcription)

