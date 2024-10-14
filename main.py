# coding=utf-8
import config
import handler.ai as ai
from datetime import datetime, timedelta

from interaction.speech_recognition import Listen as Listen_sp
from interaction.vosk_detector import Listen as Listen_vosk
from interaction.speaker import text_to_voice
from management.utils import play_mp3
from management.interpreter import interpreter, check_to_ask_ai

_listener_library = config.listener_library
_system_mp3 = config.system_sound

listen = Listen_vosk if _listener_library == 'vosk' else Listen_sp
openai_handler = ai.Openai_handler() 
time_until_question = datetime.now() - timedelta(1)

while True:
    text = listen.get_audio_speech()
    interpreting = interpreter(text)

    if (interpreting.allowed_ia == True and interpreting.quest_inside == True):
        time_until_question = datetime.now()

    if (interpreting.allowed_ia == True and interpreting.quest_inside == False):
        text = listen.get_audio_speech()
        time_until_question = datetime.now()

    should_ask_ai, time_until_question = check_to_ask_ai(text, time_until_question)

    if (should_ask_ai):
        play_mp3(_system_mp3)
        print("+-- Enter AI Function ...")
        response = openai_handler.send_question(interpreting.text)
        text_to_voice(response)
        time_until_question = datetime.now()
