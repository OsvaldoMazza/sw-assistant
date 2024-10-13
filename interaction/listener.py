import config
import speech_recognition as sr

from management.utils import get_lang_value

_mic_number_position = config.mic_number_position
_mic_name = config.mic_name
_phrase_time_limit = config.phrase_time_limit

class Listen:
    __slots__ = ("mic", "recognizer", "audio") 
    def __init__(self):
        self.mic = sr.Microphone(device_index= self.set_microphone())
        self.recognizer = sr.Recognizer()

    def convert_audio_to_text(self):
        with self.mic as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source)
                self.audio = self.recognizer.listen(source, phrase_time_limit=_phrase_time_limit)

                with open(config.default_recognize_wav, "wb") as f:
                    f.write(self.audio.get_wav_data())

                return self.recognizer.recognize_google(self.audio, language= get_lang_value('google_recognition_listen'))
            except:
                return ""
    
    def get_audio_speech(self):
        print("+-- Say something ...")
        has_converted = False
        while has_converted == False:
            result = self.convert_audio_to_text()
            if result != "":
                has_converted = True
        print(f"+-- You said: {result} ...")

        return result
    
    def set_microphone(self):
        # if _mic_number_position: 
        #     return _mic_number_position
        
        return self.find_microphone()
        

    def find_microphone(self):
        mic_list = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mic_list):
            print(f'MIC KEY TO ANALYZE: {name}')
            if _mic_name in name.lower():
                print(f'found USB mic: {name}')
                return i
        return None