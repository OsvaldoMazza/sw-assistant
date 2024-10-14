import os
import pywhatkit as kit
import psutil

import config

_operate_system = config.operate_system
_open_video_now = True if _operate_system != 'linux' else False
_browser = config.browser

def play_youtube(arguments):
    title = arguments.get('title')
    url = kit.playonyt(title,False,_open_video_now)
    if not _open_video_now: 
        print(f"+-- Opening Linux browser: {_browser}")
        os.system(f"{_browser} {url}")
    else:
        print(f"+-- Opening Windows browser: {_browser} ")

    return "le dí play"

def kill_youtube():
    print(f"+-- Closing browser: {_browser}...")
    for proc in psutil.process_iter():
        if _browser in proc.name().lower():
            proc.kill()