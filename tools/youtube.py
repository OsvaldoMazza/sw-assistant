import time
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
        print(f"+-- Opening Linux browser: {_browser} ...")
        url_complete = url + '?autoplay=1'
        print(f'URL COMPLETE: {url_complete}')
        subprocess_list.append(subprocess.Popen(['xdg-open', url_complete]))
    else:
        print(f"+-- Opening Windows browser: {_browser} ...")

    return "le dí play"

def kill_youtube():
    if _open_video_now:
        for proc in psutil.process_iter():
            if _browser in proc.name().lower():
                ("+-- closing subprocess ...")
                proc.kill()
    else:
        for subproc in subprocess_list:
            if subproc.pid != os.getpid():
                print("+-- closing subprocess ...")
                time.sleep(1)
                subproc.terminate()
        subprocess_list.clear()        

    return "apagado"
