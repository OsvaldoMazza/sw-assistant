# coding=utf-8
import config
import handler.ai as ai
from datetime import datetime, timedelta

from interaction.listener import Listen
from interaction.speaker import text_to_voice
from management.utils import check_last_time_question, play_mp3_pygame
from management.interpreter import interpreter

_system_mp3 = config.system_sound
listen = Listen()
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

    if (check_last_time_question(time_until_question)):
        play_mp3_pygame(_system_mp3)
        print("+-- Enter AI Function ...")
        response = openai_handler.send_question(interpreting.text)
        text_to_voice(response)
        time_until_question = datetime.now()
