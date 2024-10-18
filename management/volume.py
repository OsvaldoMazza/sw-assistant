
import subprocess
import time
import pyautogui

import config
from management.utils import play_mp3

_operate_system = config.operate_system
_system_mp3 = config.system_sound

def control_volume(order):
    play_mp3(_system_mp3)
    if _operate_system == 'linux':
            linux_volume(order)
    else:
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
    

def linux_volume(order):
    vol = get_master_volume()
    if order == 'up':
        vol =+ 20
    if order == 'down':
        vol =- 20
    if order == 'mute':
         vol = 0
    if order == 'max':
        vol = 100
    set_master_volume(vol)

def get_master_volume():
	proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
	amixer_stdout = proc.communicate()[0].split('\n')[4]
	proc.wait()
	find_start = amixer_stdout.find('[') + 1
	find_end = amixer_stdout.find('%]', find_start)
	return float(amixer_stdout[find_start:find_end])

def set_master_volume(volume):
	val = volume
	val = float(int(val))
	proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
	proc.wait()
   
    