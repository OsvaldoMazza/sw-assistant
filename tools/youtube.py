import pywhatkit as kit
import psutil
import webbrowser

import config

_operate_system = config.operate_system
_should_get_url = True if _operate_system != 'linux' else False

def play_youtube(arguments):
    title = arguments.get('title')
    url = kit.playonyt(title,False,_should_get_url)
    if _should_get_url: 
        webbrowser.open(url, new=0)

    return "reproduciendose video"

def kill_youtube():
    browsers = ["chrome", "chromium", "brave", "firefox", "edge"]
    
    for proc in psutil.process_iter():
        for browser in browsers:
            if browser in proc.name().lower():
                proc.kill()