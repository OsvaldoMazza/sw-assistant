from datetime import datetime, timedelta
import json
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