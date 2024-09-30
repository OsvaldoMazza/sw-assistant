import os
from gtts import gTTS

import config
from management.utils import get_lang_value
from management.utils import play_mp3_pygame, play_mp3_ffplay

mp3_name = config.default_name_mp3
mp3_velocity= config.default_velocity_mp3

def text_to_mp3(text, file_name):
    voice_language = get_lang_value('google_recognition_voice')
    tts = gTTS(text, tld = voice_language[0], lang= voice_language[1])
    tts.save(file_name)

def text_to_voice(text):
    text_to_mp3(text, mp3_name)
    if (config.is_windows):
        play_mp3_pygame(mp3_name)
    else:
        play_mp3_ffplay(mp3_name, mp3_velocity)

    delete_mp3(mp3_name)

def delete_mp3(filename):
    file_path =  filename.replace("/", "\\")
    if os.path.exists(file_path):
        os.remove(file_path)
