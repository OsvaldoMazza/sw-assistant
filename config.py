import os
from dotenv import load_dotenv

load_dotenv()

# System
api_key = os.getenv("apikey")
is_windows = os.getenv("windows", True)

# Language
language = "spanish"  # Select from languages.json

# OpenaAI
chat_model = "gpt-3.5-turbo"
enable_tools = True

# Hardware
mic_number_position = 0

# Voice Recognition
wakeup = [
            "southie",
            "ramona",
            "shazam"
        ]
attention_time = 30
phrase_time_limit = 5 

# Voice Assistant
default_name_mp3 = "temp/voice_temp"
default_velocity_mp3 = 1.5


