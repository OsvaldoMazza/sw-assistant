from datetime import datetime, timedelta
import json
import os

import pygame
import config

def check_last_time_question(time_until_question):
    diff = datetime.now() - time_until_question
    if (datetime.now() - time_until_question) < timedelta(seconds=config.attention_time):
        print("+-- Allowed to ask to OpenAi ...")
        return True
    
    return False

def get_tools():
    with open('tools/tools.json', 'r') as file:
        return json.load(file)

def get_lang_value(phrase):
    with open('languages.json', 'r') as file:
        phrases = json.load(file)
    
    return phrases[config.language][phrase]
    
def get_assistant_behavior():
    with open('assistant_behavior.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content += f"\n La fecha y la hora del día de hoy es {today}. Utilizarlo al momento de crear eventos de calendario"
    return content

def play_mp3_ffplay(file_name, velocity):
    os.system(f"ffplay -v 0 -nodisp -af 'atempo={velocity}' -autoexit {file_name}")

def play_mp3_pygame(file_name):
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play(loops=0)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(0) 
    pygame.quit()