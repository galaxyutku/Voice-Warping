import tkinter as tk
import customtkinter
import os
import pyaudio
import wave
import time
import threading
from functions import *
from recorder import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    path = None

    def __init__(self):
        super().__init__()


        # configure window
        self.title("Voice Warping Application")
        self.geometry(f"{1920}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((1, 2), weight=1)


        # create Save_button
        self.main_button_1 = customtkinter.CTkButton(self, border_width=2, text_color=("gray10", "#DCE4EE"),text="Save as",width=270,height=50, command=saveTo)
        self.main_button_1.grid(row=0, column=3, padx=(10, 338), pady=(0, 200))

        #General Frame

        self.General_frame = customtkinter.CTkFrame(self)
        self.General_frame.grid(row=0, column=0, padx=(40, 20), pady=(20, 200))


        # Warping Part
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.General_frame, dynamic_resizing=False,width=250,height=50,values=["Default", "Angry", "Sad", "Happy", "Fear", "Disgust"], command=self.changePreset)
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.Upload_Button = customtkinter.CTkButton(self.General_frame, border_width=2, text_color=("gray10", "#DCE4EE"),text="Upload",width=200, height=50, command=getAudio)
        self.Upload_Button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20),)
        self.Change_Button = customtkinter.CTkButton(self.General_frame, border_width=2,text_color=("gray10", "#DCE4EE"), text="Change", width=200, height=50, command=lambda: [changeAudio(isAllpass.get(), isComb.get(), isEcho.get(), isReverbed.get(), isChorus.get(), isFlanger.get(), isVibrato.get(), isTremolo.get(), isFade.get(), isFadeIn.get(), isFadeOut.get(), isTpl.get(), isEQ.get(), currentWNoise.get(), currentStrecth.get(), currentPitch.get(), currentIntensity.get(), currentHarmonic.get(), currentPercussive.get(), hz_32.get(), hz_63.get(), hz_125.get(), hz_250.get(), hz_500.get(), hz_1000.get(), hz_2000.get(), hz_4000.get(), hz_8000.get(), hz_16000.get())])
        self.Change_Button.grid(row=3, column=1, padx=(450, 0), pady=(20, 20))
        self.Play_Button = customtkinter.CTkButton(self.General_frame, border_width=2,text_color=("gray10", "#DCE4EE"), text="Play",width=200, height=50, command=play)
        self.Play_Button.grid(row=3, column=2, padx=(0, 0), pady=(20, 20))

        # Record Button
        self.recrodbutton_frame = customtkinter.CTkFrame(self)
        self.recrodbutton_frame.grid(row=0, column=3, padx=(50, 380), pady=(35,500))
        self.textbox = customtkinter.CTkLabel(self.recrodbutton_frame, text="Record",text_color="#fff",width=250,justify="left",anchor="w",font=("Arial", 25))
        self.textbox.grid(row=0, column=0, padx=(20,0),pady=(20,0),sticky="nsew")
        self.record_button_1 = customtkinter.CTkButton(master=self.recrodbutton_frame, border_width=2, text_color=("gray10", "#DCE4EE"), text="Save to", command=self.choosePath)
        self.record_button_1.grid(row=1, column=0, padx=(20, 100), pady=(20, 20), )
        self.record_button_2 = customtkinter.CTkButton(master=self.recrodbutton_frame, border_width=2, fg_color="#2fa572", text_color=("gray10", "#DCE4EE"), text="Record (Start/Stop)", command=self.click_handler)
        self.recording = False
        self.record_button_2.grid(row=2, column=0, padx=(20, 100), pady=(20, 20), )

        # create slider and progressbar frame
        currentWNoise = tk.DoubleVar()
        currentStrecth = tk.DoubleVar()
        currentPitch = tk.DoubleVar()
        currentIntensity = tk.DoubleVar()
        currentHarmonic = tk.DoubleVar()
        currentPercussive = tk.DoubleVar()
        self.Slider_frame_horizontal = customtkinter.CTkFrame(self.General_frame)
        self.Slider_frame_horizontal.grid(row=1, column=0,padx=(25,0), sticky="nsew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="White Noise", text_color="#fff", width=250, anchor="w", font=("Arial", 17))
        self.text.grid(row=0, column=0,padx=(10,0),pady=(10,0), sticky="nsew")
        self.slider = customtkinter.CTkSlider(self.Slider_frame_horizontal, orientation='horizontal', from_=0, to=0.05, variable=currentWNoise)
        self.slider.grid(row=1, column=0,  sticky="ew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Strecth", text_color="#fff", width=250, anchor="w", font=("Arial", 17))
        self.text.grid(row=2, column=0,padx=(10,0), sticky="nsew")
        self.slider_2 = customtkinter.CTkSlider(self.Slider_frame_horizontal, orientation='horizontal', from_=0.5, to=2, variable=currentStrecth)
        self.slider_2.set(1)
        self.slider_2.grid(row=3, column=0,  sticky="ew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Pitch", text_color="#fff", width=250,justify="left", anchor="w", font=("Arial", 17))
        self.text.grid(row=4, column=0,padx=(10,0), sticky="nsew")
        self.slider_3 = customtkinter.CTkSlider(self.Slider_frame_horizontal, orientation='horizontal', from_=-10, to=10, variable=currentPitch)
        self.slider_3.set(1)
        self.slider_3.grid(row=5, column=0, sticky="ew")

        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Intensity", text_color="#fff", width=250,justify="left", anchor="w", font=("Arial", 17))
        self.text.grid(row=6, column=0,padx=(10,0),pady=(10,0), sticky="nsew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Harmonic", text_color="#fff", width=250,justify="center", anchor="w", font=("Arial", 17))
        self.text.grid(row=7, column=0,padx=(10,0), sticky="nsew")
        self.slider_4 = customtkinter.CTkSlider(self.Slider_frame_horizontal, orientation='horizontal', from_=-10, to=10, variable=currentHarmonic)
        self.slider_4.set(1)
        self.slider_4.grid(row=8, column=0, sticky="ew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Percussive", text_color="#fff", width=250,justify="center", anchor="w", font=("Arial", 17))
        self.text.grid(row=9,column=0,padx=(10,0), sticky="nsew")
        self.slider_5 = customtkinter.CTkSlider(self.Slider_frame_horizontal, orientation='horizontal', from_=-10, to=10, variable=currentPercussive)
        self.slider_5.set(1)
        self.slider_5.grid(row=10, column=0, sticky="ew")

        # Equlizer eqSliders
        isEQ, hz_32, hz_63, hz_125, hz_250, hz_500, hz_1000, hz_2000, hz_4000, hz_8000, hz_16000 = tk.IntVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        self.Slider_frame_Equalizer = customtkinter.CTkFrame(self.General_frame)
        self.Slider_frame_Equalizer.grid(row=1, column=1, padx=(50,50))
        self.checkbox_Equalizer = customtkinter.CTkCheckBox(master=self.Slider_frame_Equalizer, text="Equalizer", font=("Arial", 25), variable=isEQ)
        self.checkbox_Equalizer.grid(row=0, column=0, pady=(20, 20), padx=(20,0), sticky="n")
        self.eqslider_1 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_32)
        self.eqslider_1.grid(row=1, column=0, padx=(0, 0), pady=(10, 10))
        self.eqslider_2 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_63)
        self.eqslider_2.grid(row=1, column=1, padx=(0, 60), pady=(10, 10))
        self.eqslider_3 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_125)
        self.eqslider_3.grid(row=1, column=2, padx=(0, 60), pady=(10, 10))
        self.eqslider_4 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_250)
        self.eqslider_4.grid(row=1, column=3, padx=(0, 60), pady=(10, 10))
        self.eqslider_5 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_500)
        self.eqslider_5.grid(row=1, column=4, padx=(0, 60), pady=(10, 10))
        self.eqslider_6 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_1000)
        self.eqslider_6.grid(row=1, column=5, padx=(0, 60), pady=(10, 10))
        self.eqslider_7 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_2000)
        self.eqslider_7.grid(row=1, column=6, padx=(0, 60), pady=(10, 10))
        self.eqslider_8 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_4000)
        self.eqslider_8.grid(row=1, column=7, padx=(0, 60), pady=(10, 10))
        self.eqslider_9 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_8000)
        self.eqslider_9.grid(row=1, column=8, padx=(0, 60), pady=(10, 10))
        self.eqslider_10 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical", from_=-20, to=20, variable=hz_16000)
        self.eqslider_10.grid(row=1, column=9, padx=(0, 60), pady=(10, 10))

        # create checkbox and switch frame
        isAllpass = tk.IntVar()
        isComb = tk.IntVar()
        isEcho = tk.IntVar()
        isReverbed = tk.IntVar()
        isChorus = tk.IntVar()
        isFlanger = tk.IntVar()
        isVibrato = tk.IntVar()
        isTremolo = tk.IntVar()
        isFade = tk.IntVar()
        isFadeIn = tk.IntVar()
        isFadeOut = tk.IntVar()
        isTpl = tk.IntVar()
        self.checkbox_slider_frame = customtkinter.CTkFrame(self.General_frame)
        self.checkbox_slider_frame.grid(row=1, column=2, padx=(0, 20))
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Allpass", variable=isAllpass)
        self.checkbox_1.grid(row=1, column=1, pady=(34, 15), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Comb", variable=isComb)
        self.checkbox_2.grid(row=1, column=0, pady=(34, 15), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Echo", variable=isEcho)
        self.checkbox_3.grid(row=2, column=0, pady=(0,15), padx=20, sticky="n")
        self.checkbox_4 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Reverbed", variable=isReverbed)
        self.checkbox_4.grid(row=2, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_5 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Chorus", variable=isChorus)
        self.checkbox_5.grid(row=3, column=0, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_6 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Flanger", variable=isFlanger)
        self.checkbox_6.grid(row=3, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_7 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Vibrato", variable=isVibrato)
        self.checkbox_7.grid(row=4, column=0, pady=(0,15), padx=20, sticky="n")
        self.checkbox_8 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Tremolo", variable=isTremolo)
        self.checkbox_8.grid(row=4, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_9 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Fade", variable=isFade)
        self.checkbox_9.grid(row=5, column=0, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_10 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Fade In", variable=isFadeIn)
        self.checkbox_10.grid(row=5, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_11 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Fade Out", variable=isFadeOut)
        self.checkbox_11.grid(row=6, column=0, pady=(0, 34), padx=20, sticky="n")
        self.checkbox_12 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="TPL", variable=isTpl)
        self.checkbox_12.grid(row=6, column=1, pady=(0, 34), padx=20, sticky="n")
        # set default values
        self.optionmenu_1.set("Default")
    
    def click_handler(self):
        if self.recording:
            self.recording = False
            self.record_button_2.configure(fg_color ="#2fa572")
        else:
            self.recording = True
            self.record_button_2.configure(fg_color ="#fe0000")
            threading.Thread(target=self.rec).start()
            
    def changePreset(self, preset):
        if preset == "Angry":
            self.slider_2.set(1.4)
            self.slider_3.set(-0.5)
            self.slider_4.set(1)
            self.slider_5.set(3)
            self.checkbox_Equalizer.select()
            self.eqslider_1.set(-10)
            self.eqslider_2.set(-10)
            self.eqslider_3.set(15)
            self.eqslider_4.set(10)
            self.eqslider_5.set(7)
            self.eqslider_6.set(5)
            self.eqslider_7.set(5)
            self.eqslider_8.set(10)
            self.eqslider_9.set(-8)
            self.eqslider_10.set(-8)
        if preset == "Sad":
            self.slider_2.set(0.8)
            self.slider_3.set(1.2)
            self.slider_4.set(2)
            self.slider_5.set(1)
            self.checkbox_Equalizer.select()
            self.eqslider_1.set(-20)
            self.eqslider_2.set(-10)
            self.eqslider_3.set(-10)
            self.eqslider_4.set(-5)
            self.eqslider_5.set(5)
            self.eqslider_6.set(5)
            self.eqslider_7.set(10)
            self.eqslider_8.set(5)
            self.eqslider_9.set(6)
            self.eqslider_10.set(-8)
        if preset == "Happy":
            self.slider_2.set(1.6)
            self.slider_3.set(0.7)
            self.slider_4.set(1)
            self.slider_5.set(4)
            self.checkbox_Equalizer.select()
            self.eqslider_1.set(-20)
            self.eqslider_2.set(-20)
            self.eqslider_3.set(-10)
            self.eqslider_4.set(-10)
            self.eqslider_5.set(5)
            self.eqslider_6.set(5)
            self.eqslider_7.set(10)
            self.eqslider_8.set(8)
            self.eqslider_9.set(9)
            self.eqslider_10.set(-8)
        if preset == "Fear":
            self.slider_2.set(0.94)
            self.slider_3.set(1)
            self.slider_4.set(1)
            self.slider_5.set(4)
            self.checkbox_Equalizer.select()
            self.eqslider_1.set(-10)
            self.eqslider_2.set(-10)
            self.eqslider_3.set(15)
            self.eqslider_4.set(10)
            self.eqslider_5.set(7)
            self.eqslider_6.set(5)
            self.eqslider_7.set(5)
            self.eqslider_8.set(10)
            self.eqslider_9.set(-8)
            self.eqslider_10.set(-8)
            self.checkbox_7.select()
        if preset == "Disgust":
            self.slider_2.set(1)
            self.slider_3.set(1.2)
            self.slider_4.set(1)
            self.slider_5.set(4)
            self.checkbox_Equalizer.select()
            self.eqslider_1.set(-20)
            self.eqslider_2.set(-10)
            self.eqslider_3.set(-10)
            self.eqslider_4.set(-5)
            self.eqslider_5.set(5)
            self.eqslider_6.set(5)
            self.eqslider_7.set(10)
            self.eqslider_8.set(5)
            self.eqslider_9.set(6)
            self.eqslider_10.set(-8)
            self.checkbox_7.select()
        if preset == "Default":
            self.slider.set(0)
            self.slider_2.set(1)
            self.slider_3.set(1)
            self.slider_4.set(1)
            self.slider_5.set(1)
            self.checkbox_Equalizer.deselect()
            self.eqslider_1.set(0)
            self.eqslider_2.set(0)
            self.eqslider_3.set(0)
            self.eqslider_4.set(0)
            self.eqslider_5.set(0)
            self.eqslider_6.set(0)
            self.eqslider_7.set(0)
            self.eqslider_8.set(0)
            self.eqslider_9.set(0)
            self.eqslider_10.set(0)
            self.checkbox_1.deselect()
            self.checkbox_2.deselect()
            self.checkbox_3.deselect()
            self.checkbox_4.deselect()
            self.checkbox_5.deselect()
            self.checkbox_6.deselect()
            self.checkbox_7.deselect()
            self.checkbox_8.deselect()
            self.checkbox_9.deselect()
            self.checkbox_10.deselect()
            self.checkbox_11.deselect()
            self.checkbox_12.deselect()

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
                    
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        exists = True
        i = 1
        while exists:
            if os.path.exists(self.path + f"/rec{i}.wav"):
                i+= 1
            else:
                exists = False
                sound_file = wave.open(self.path + f"/rec{i}.wav", "wb")
                sound_file.setnchannels(1)
                sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                sound_file.setframerate(44100)
                sound_file.writeframes(b"".join(frames))
                sound_file.close()
    
    def choosePath(self):
        self.path = filedialog.askdirectory()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()