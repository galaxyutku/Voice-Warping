import os
import pyaudio
import wave
import time
import threading
import tkinter as tk
import tkinter as tk
from tkinter import filedialog


class VoiceRec:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.button = tk.Button(text="🎤", font= ("Arial", 120, "bold"),
                                command =self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.rec).start()
            
            
    def rec(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                            input=True, frames_per_buffer=1024)
        
        frames = []
        
        start = time.time()        
        
        while self.recording:
            data = stream.read(1024)
            frames.append(data)
            
            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60 
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
                    
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        exists = True
        i = 1
        while exists:
            if os.path.exists(path + f"/rec{i}.wav"):
                i+= 1
            else:
                exists = False
                    
                sound_file = wave.open(path + f"/rec{i}.wav", "wb")
                sound_file.setnchannels(1)
                sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                sound_file.setframerate(44100)
                sound_file.writeframes(b"".join(frames))
                sound_file.close()

def choosePath():
    global path
    path = filedialog.askdirectory()