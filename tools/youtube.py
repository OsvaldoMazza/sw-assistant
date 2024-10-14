import pywhatkit as kit
import psutil
import webbrowser

def play_youtube(arguments):
    title = arguments.get('title')
    url = kit.playonyt(title,False,False)
    webbrowser.open(url, new=0)

    return "reproduciendose video"

def kill_youtube():
    for proc in psutil.process_iter():
        if "chrome" in proc.name().lower():
            proc.kill()

        if "chromium" in proc.name().lower():
            proc.kill()

        if "brave" in proc.name().lower():
            proc.kill()