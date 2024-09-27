import config
import speech_recognition as sr

from management.utils import get_lang_value

class Listen:
    __slots__ = ("mic", "recognizer", "audio") 
    def __init__(self):
        self.mic = sr.Microphone(device_index= config.mic_number_position)
        self.recognizer = sr.Recognizer()

    def convert_audio_to_text(self):
        with self.mic as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source)
                self.audio = self.recognizer.listen(source, phrase_time_limit=config.phrase_time_limit)

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