import pywhatkit as kit
import psutil

def play_youtube(arguments):
    title = arguments.get('title')
    kit.playonyt(title)

    print('+-- youtuve video playing ...')

    return "youtube playing."

def kill_youtube():
    for proc in psutil.process_iter():
        if "chrome" in proc.name().lower():
            proc.kill()

        if "chromium" in proc.name().lower():
            proc.kill()

        if "brave" in proc.name().lower():
            proc.kill()