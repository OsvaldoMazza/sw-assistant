import os
from dotenv import load_dotenv

load_dotenv()

###############################################################################
### System ###
# AI Type [azure | openai]
connection_type = os.getenv("connection_type") or "openai"

# Wakeup in any place of the phrase [True | False]
wake_up_every_place =  os.getenv("wake_up_every_place") or True

# Operate System running in program [windows | linux]
operate_system = os.getenv("operate_system") or "linux"

# Browser to open searchs in Linux ex: "chromium" 
browser =  os.getenv("browser") or "chrome"

# Language from language.json
language =  os.getenv("language") or "spanish"

###############################################################################
### OpenaAI Configuration ####
# Chat Model ex:"gpt-3.5-turbo"
chat_model = "gpt-3.5-turbo"

# Enable Functiol Tools [True | False]
enable_tools = True

# Max Tokens ex: 4096
max_tokens = 4096

#Max Tokens response: ex 500
max_response_tokens = 500

###############################################################################
### Azure ###
# Azure API version template ex: "2024-02-01"
azure_api_version = "2024-02-01"

###############################################################################
### Hardware ###
# Mic position in list of Hardware
mic_number_position = 0

# Mic name in the list of Hardware. Put "" mic_number_position to enable by Mic name.
mic_name = "usb" 

###############################################################################
### Voice Recognition ###
# Name of IA to wake up
wakeup = [
            "ramona",
            "ramón",
            "gallega",
        ]

# Time to be awake without using the wakup word and continue the chat.
attention_time = 15

# Phrase time limit
phrase_time_limit = 5

# librery to listener [vosk | speech_recognition ]
listener_library = 'vosk'

# Vosk Folder
vosk_folder = "./vosk-model"

###############################################################################
### Miscelaneus ###
# Place of Sound File Sound
system_sound = "assets/system.mp3"

# MP3 temporally name
default_name_mp3 = "temp/voice_temp.mp3"

# WAV temporally name
default_recognize_wav = "temp/recognize.wav"

# Velocity speech IA
default_velocity_mp3 = 1.6

###############################################################################

