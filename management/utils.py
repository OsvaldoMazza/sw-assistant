from datetime import datetime
import json
import os
import subprocess

import config

_mp3_velocity= config.default_velocity_mp3


def get_tools():
    with open('tools/tools.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def get_lang_value(phrase):
    with open('languages.json', 'r', encoding='utf-8') as file:
        phrases = json.load(file)
    
    return phrases[config.language][phrase]
    
def get_assistant_behavior():
    with open('assistant_behavior.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content += f"\n La fecha y la hora del día de hoy es {today}. Utilizarlo al momento de crear eventos de calendario"
    return content

def play_mp3(file_name, wait = False, fast = False):
    play_mp3_ffplay(file_name, wait, fast)

def play_mp3_ffplay(file_name, wait, fast):
    speed = _mp3_velocity if fast else 1
    command = [
    "ffplay",
    "-v", "0",
    "-nodisp",
    "-af", f"atempo={_mp3_velocity}",
    "-autoexit",
    file_name
    ]

    if wait:
        subprocess.run(command)
    else:
        subprocess.Popen(command)

def delete_mp3(filename):
    file_path =  filename.replace("/", "\\")
    if os.path.exists(file_path):
        os.remove(file_path)

def set_local_value(key, value, filename='values.json'):
    data = {}

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    data[key] = value

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_local_value(key, filename='values.json', ):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

            return data.get(key, None)
    return None