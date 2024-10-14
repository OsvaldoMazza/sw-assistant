import os
import subprocess
import pywhatkit as kit
import psutil

import config

_operate_system = config.operate_system
_open_video_now = True if _operate_system != 'linux' else False
_browser = config.browser

subprocess_list = []

def play_youtube(arguments):
    title = arguments.get('title')
    url = kit.playonyt(title,False,_open_video_now)
    if not _open_video_now: 
        print(f"+-- Opening Linux browser: {_browser}")
        subprocess_list.append(subprocess.Popen([_browser, f"{url}?autoplay=1"]))
    else:
        print(f"+-- Opening Windows browser: {_browser} ")

    return "le dí play"

def kill_youtube():
    print(f"+-- Closing browser: {_browser}...")
    for subproc in subprocess_list:
        subproc.terminate()
