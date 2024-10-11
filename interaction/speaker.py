from gtts import gTTS

import config
from management.utils import get_lang_value, play_mp3, delete_mp3

_mp3_name = config.default_name_mp3

def text_to_mp3(text, file_name):
    voice_language = get_lang_value('google_recognition_voice')
    tts = gTTS(text, tld = voice_language[0], lang= voice_language[1])
    tts.save(file_name)

def text_to_voice(text):
    text_to_mp3(text, _mp3_name)
    play_mp3(_mp3_name, wait = True, fast = True)
    delete_mp3(_mp3_name)
