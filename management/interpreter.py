from datetime import datetime, timedelta
import config
from models.interpreting import Interpreting
from interaction.speaker import text_to_voice
from management.utils import get_lang_value, play_mp3
from tools.tuya_home import switch_device
from management.volume import control_volume
from tools.youtube import kill_youtube

_attention_time = config.attention_time
_system_mp3 = config.system_sound
_wakeup = config.wakeup
_is_wakup_every_place = config.wake_up_every_place
_greetings = get_lang_value('greetings')

interpreting = Interpreting

def interpreter(text):
    text = remove_greetings(text.lower())
    if _is_wakup_every_place and any(phrase in text for phrase in _wakeup):
        remove_wakup(text)
        return interpreting
    elif any(text.startswith(phrase) for phrase in _wakeup): 
        remove_wakup(text)
        return interpreting
    elif text in get_lang_value('light_house'): 
        light_house()
        return interpreting('False', False,False)

    elif text in get_lang_value('volume_up'): 
        control_volume('up')
        return interpreting('False', False,False)
    elif text in get_lang_value('volume_down'): 
        control_volume('down')
        return interpreting('False', False,False)
    elif text in get_lang_value('silent'): 
        control_volume('mute')
        return interpreting('False', False,False)
    elif text in get_lang_value('loud'): 
        control_volume('max')
        return interpreting('False', False,False)
    
    elif text in get_lang_value('emergency_silence'):
        emergency_silent()
        return interpreting('False', False,False)
    
    elif text in get_lang_value('close'): close_program()
    else: do_nothing()

    interpreting.allowed_ia = False
    interpreting.quest_inside = False
    interpreting.text = text
    
    return interpreting
   
def do_nothing():
    pass

def light_house():
    play_mp3(_system_mp3)
    switch_device()

def emergency_silent():
    control_volume('mute') 
    kill_youtube()

def close_program():
    text_to_voice(get_lang_value('goodbye'))
    print("+-- The assistant program finished by voice order ...")
    exit()

def remove_greetings(text):
    for phrase in _greetings:
        if text.startswith(phrase) and len(text[len(phrase):].strip()) > 10:

            return text[len(phrase):].strip()
    
    return text

def remove_wakup(text):
    for phrase in _wakeup:
        if phrase in text and len(text.replace(phrase,'')) > 10:
            interpreting.text = text.replace(phrase,'')
            interpreting.allowed_ia = True
            interpreting.quest_inside = True

            return interpreting
        
    interpreting.allowed_ia = True
    interpreting.quest_inside = False
    ready_text = get_lang_value('ready')
    print(f"+-- AI: {ready_text} ...")
    text_to_voice(ready_text)
        
    return interpreting

def check_to_ask_ai(text, time_until_question):
    should_ask_ai = False
    if not check_stop_talking(text) and check_last_time_question(time_until_question):
        should_ask_ai = True
    else:
        time_until_question = datetime.now() - timedelta(1)
    
    return should_ask_ai, time_until_question
   

def check_last_time_question(time_until_question):
    if (datetime.now() - time_until_question) < timedelta(seconds= _attention_time):
        print("+-- Allowed to ask to OpenAi ...")
        return True
    
    return False

def check_stop_talking(text):
    for phrase in get_lang_value('stop_talking'):
        if text.lower() == phrase.lower():

            return True
    
    return False