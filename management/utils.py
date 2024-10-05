from datetime import datetime, timedelta
import json
import os

import arcade
import config

_is_windows = config.is_windows
_mp3_velocity= config.default_velocity_mp3

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

def play_mp3(file_name):
    if (_is_windows):
        play_sound_arcade(file_name)
    else:
        play_mp3_ffplay(file_name, _mp3_velocity)

def play_mp3_ffplay(file_name, velocity):
    os.system(f"ffplay -v 0 -nodisp -af 'atempo={velocity}' -autoexit {file_name}")

def play_sound_arcade(file_name, velocity = None):
    sound = arcade.load_sound(file_name)
    arcade.play_sound(sound)

def delete_mp3(filename):
    file_path =  filename.replace("/", "\\")
    if os.path.exists(file_path):
        os.remove(file_path)

def set_local_value(key, value, filename='values.json'):
    data = {}

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    data[key] = value

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_local_value(key, filename='values.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)

            return data.get(key, None)
    return None