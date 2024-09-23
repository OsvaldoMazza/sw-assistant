import config
from models.interpreting import Interpreting
from interaction.speaker import text_to_voice
from management.utils import get_lang_value

interpreting = Interpreting
greetings = get_lang_value('greetings')
wakeup = config.wakeup

def interpreter(text):
    text = remove_greetings(text.lower())

    if any(text.startswith(phrase) for phrase in wakeup): 
        remove_wakup(text)
        return interpreting
    elif text in get_lang_value('close'): close_program()
    else: do_nothing()

    interpreting.allowed_ia = False
    interpreting.quest_inside = False
    interpreting.text = text
    
    return interpreting
   
def do_nothing():
    pass

def close_program():
    text_to_voice(get_lang_value('goodbye'))
    print("+-- The assistant program finished by voice order ...")
    exit()

def remove_greetings(text):
    for phrase in greetings:
        if text.startswith(phrase) and len(text[len(phrase):].strip()) > 10:
            return text[len(phrase):].strip()
    
    return text

def remove_wakup(text):
    for phrase in wakeup:
        if text.startswith(phrase) and len(text[len(phrase):].strip()) > 10:
            interpreting.text = text[len(phrase):].strip()
            interpreting.allowed_ia = True
            interpreting.quest_inside = True

            return interpreting
        
    interpreting.allowed_ia = True
    interpreting.quest_inside = False
    ready_text = get_lang_value('ready')
    print(f"AI: {ready_text}")
    text_to_voice(ready_text)
        
    return interpreting