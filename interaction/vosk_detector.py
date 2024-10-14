import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

_vosk_folder = "./vosk-full"

class Listen:
    __slots__ = ("model", "p", "rec") 
    def __init__(self):
        self.model = Model(os.path.abspath(_vosk_folder))
        self.rec = KaldiRecognizer(self.model, 16000)
        
    def get_audio_speech(self):
        self.p = pyaudio.PyAudio()
        stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()
        text = None
        print('+-- Say Something ...')
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break

            if self.rec.AcceptWaveform(data):
                result = self.rec.Result()
                text = json.loads(result)["text"]
                
                if text.strip():
                    print(f"+-- Text recognized: {text} ...")
                    break

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        return text
