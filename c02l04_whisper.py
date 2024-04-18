from ai_devs import get_task, get_token, send_task
from openai import OpenAI
import os
import requests

token = get_token("whisper")
task = get_task(token, True)

file_url = task["msg"].split(" ")[6]

print(file_url)

# Download the audio file from the URL
response = requests.get(file_url)
audio_data = response.content

# Save the audio file temporarily (optional: handle this in memory if possible)
with open("temp_audio.wav", "wb") as audio_file:
    audio_file.write(audio_data)

# Transcribe the downloaded audio file
client = OpenAI()
transcription_response = client.audio.transcriptions.create(
    model="whisper-1",
    file=open("temp_audio.wav", "rb"),
)

# Print the transcription
print(transcription_response.text)

# Optionally remove the temporary file if you don't need it anymore
os.remove("temp_audio.wav")


send_task(token, transcription_response.text)
