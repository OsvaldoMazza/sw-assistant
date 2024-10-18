
import subprocess
import time
import pyautogui

import config
from management.utils import play_mp3

_operate_system = config.operate_system
_system_mp3 = config.system_sound

def control_volume(order):
    play_mp3(_system_mp3)
    if order == 'up':
        for i in range(10): 
            pyautogui.press('volumeup')
            time.sleep(0.1)
    elif order == 'down':
        for i in range(7): 
            pyautogui.press('volumedown')
            time.sleep(0.1)
    elif order == 'mute':
        pyautogui.hotkey('volumemute')
    if order == 'max':
        for i in range(50): 
            pyautogui.press('volumeup')
       
    