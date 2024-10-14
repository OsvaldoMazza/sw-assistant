import os
from dotenv import load_dotenv

load_dotenv()

## System
connection_type = "openai" # azure | openai
wake_up_every_place = True  # True | False  fwake up ia in any place of the phrase
system_sound = "assets/system.mp3"

## Language
language = "spanish"  # Select from languages.json

## OpenaAI
chat_model = "gpt-3.5-turbo"
enable_tools = True
max_tokens = 4096
max_response_tokens = 500

## Azure
azure_api_version = "2024-02-01"

## Hardware
mic_number_position = 0 # set the microphone position number if you know
mic_name = "usb"          # set the microphone name if you don't know the position

## Voice Recognition
wakeup = [
            "southie",
            "ramona",
            "shazam",
            "ramón"
        ]
attention_time = 7
phrase_time_limit = 5 

## Voice Assistant
default_name_mp3 = "temp/voice_temp.mp3"
default_recognize_wav = "temp/recognize.wav"
default_velocity_mp3 = 1.6


