import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        # configure window
        self.title("Voice Warping Application")
        self.geometry(f"{1650}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((1, 2), weight=1)


        # create Save_button
        self.main_button_1 = customtkinter.CTkButton(self, border_width=2, text_color=("gray10", "#DCE4EE"),text="Save as",width=270,height=50)
        self.main_button_1.grid(row=0, column=3, padx=(10, 338), pady=(0, 200))

        #General Frame

        self.General_frame = customtkinter.CTkFrame(self)
        self.General_frame.grid(row=0, column=0, padx=(40, 20), pady=(20, 200))


        # Warping Part
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.General_frame, dynamic_resizing=False,width=250,height=50,values=["Default", "Angry", "Sad", "Happy","Emotion 1","Emotion2"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.Upload_Button = customtkinter.CTkButton(self.General_frame, border_width=2, text_color=("gray10", "#DCE4EE"),text="Upload",width=200, height=50)
        self.Upload_Button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20),)
        self.Change_Button = customtkinter.CTkButton(self.General_frame, border_width=2,text_color=("gray10", "#DCE4EE"), text="Change", width=200, height=50)
        self.Change_Button.grid(row=3, column=1, padx=(450, 0), pady=(20, 20))
        self.Play_Button = customtkinter.CTkButton(self.General_frame, border_width=2,text_color=("gray10", "#DCE4EE"), text="Play",width=200, height=50, )
        self.Play_Button.grid(row=3, column=2, padx=(0, 0), pady=(20, 20))

        # Record Button
        self.recrodbutton_frame = customtkinter.CTkFrame(self)
        self.recrodbutton_frame.grid(row=0, column=3, padx=(50, 380), pady=(35,500))
        self.textbox = customtkinter.CTkLabel(self.recrodbutton_frame, text="Record",text_color="#fff",width=250,justify="left",anchor="w",font=("Arial", 25))
        self.textbox.grid(row=0, column=0, padx=(20,0),pady=(20,0),sticky="nsew")
        self.record_button_1 = customtkinter.CTkButton(master=self.recrodbutton_frame, border_width=2, text_color=("gray10", "#DCE4EE"), text="Save to")
        self.record_button_1.grid(row=1, column=0, padx=(20, 100), pady=(20, 20), )
        self.record_button_2 = customtkinter.CTkButton(master=self.recrodbutton_frame, border_width=2,text_color=("gray10", "#DCE4EE"), text="Record (Start/Stop)")
        self.record_button_2.grid(row=2, column=0, padx=(20, 100), pady=(20, 20), )

        # create slider and progressbar frame
        self.Slider_frame_horizontal = customtkinter.CTkFrame(self.General_frame)
        self.Slider_frame_horizontal.grid(row=1, column=0,padx=(25,0), sticky="nsew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="White Noise", text_color="#fff", width=250, anchor="w", font=("Arial", 17))
        self.text.grid(row=0, column=0,padx=(10,0),pady=(10,0), sticky="nsew")
        self.slider = customtkinter.CTkSlider(self.Slider_frame_horizontal)
        self.slider.grid(row=1, column=0,  sticky="ew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Strecth", text_color="#fff", width=250, anchor="w", font=("Arial", 17))
        self.text.grid(row=2, column=0,padx=(10,0), sticky="nsew")
        self.slider_2 = customtkinter.CTkSlider(self.Slider_frame_horizontal)
        self.slider_2.grid(row=3, column=0,  sticky="ew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Pitch", text_color="#fff", width=250,justify="left", anchor="w", font=("Arial", 17))
        self.text.grid(row=4, column=0,padx=(10,0), sticky="nsew")
        self.slider_3 = customtkinter.CTkSlider(self.Slider_frame_horizontal)
        self.slider_3.grid(row=5, column=0, sticky="ew")

        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Intensity", text_color="#fff", width=250,justify="left", anchor="w", font=("Arial", 17))
        self.text.grid(row=6, column=0,padx=(10,0),pady=(10,0), sticky="nsew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Harmonic", text_color="#fff", width=250,justify="center", anchor="w", font=("Arial", 17))
        self.text.grid(row=7, column=0,padx=(10,0), sticky="nsew")
        self.slider_4 = customtkinter.CTkSlider(self.Slider_frame_horizontal)
        self.slider_4.grid(row=8, column=0, sticky="ew")
        self.text = customtkinter.CTkLabel(self.Slider_frame_horizontal, text="Percussive", text_color="#fff", width=250,justify="center", anchor="w", font=("Arial", 17))
        self.text.grid(row=9,column=0,padx=(10,0), sticky="nsew")
        self.slider_4 = customtkinter.CTkSlider(self.Slider_frame_horizontal)
        self.slider_4.grid(row=10, column=0, sticky="ew")

        # Equlizer Sliders
        self.Slider_frame_Equalizer = customtkinter.CTkFrame(self.General_frame)
        self.Slider_frame_Equalizer.grid(row=1, column=1,padx=(50,50))
        self.checkbox_Equalizer = customtkinter.CTkCheckBox(master=self.Slider_frame_Equalizer, text="Equalizer", font=("Arial", 25))
        self.checkbox_Equalizer.grid(row=1, column=1, pady=(20, 20), padx=20, sticky="n")
        self.slider_1 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_1.grid(row=9, column=1, padx=(200, 10), pady=(10, 10))
        self.slider_2 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_2.grid(row=9, column=2, padx=(0, 10), pady=(10, 10))
        self.slider_3 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_3.grid(row=9, column=3, padx=(0, 10), pady=(10, 10))
        self.slider_4 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_4.grid(row=9, column=4, padx=(0, 10), pady=(10, 10))
        self.slider_5 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_5.grid(row=9, column=5, padx=(0, 10), pady=(10, 10))
        self.slider_6 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_6.grid(row=9, column=6, padx=(0, 10), pady=(10, 10))
        self.slider_7 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_7.grid(row=9, column=7, padx=(0, 10), pady=(10, 10))
        self.slider_8 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_8.grid(row=9, column=8, padx=(0, 10), pady=(10, 10))
        self.slider_9 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_9.grid(row=9, column=9, padx=(0, 10), pady=(10, 10))
        self.slider_9 = customtkinter.CTkSlider(self.Slider_frame_Equalizer, orientation="vertical")
        self.slider_9.grid(row=9, column=10, padx=(0, 10), pady=(10, 10))

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self.General_frame)
        self.checkbox_slider_frame.grid(row=1, column=2, padx=(0, 20))
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="allpass")
        self.checkbox_1.grid(row=1, column=1, pady=(34, 15), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="comb")
        self.checkbox_2.grid(row=1, column=0, pady=(34, 15), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="echo")
        self.checkbox_3.grid(row=2, column=0, pady=(0,15), padx=20, sticky="n")
        self.checkbox_4 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="reverbed")
        self.checkbox_4.grid(row=2, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_5 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="chorus")
        self.checkbox_5.grid(row=3, column=0, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_6 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="flanger")
        self.checkbox_6.grid(row=3, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_7 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="vibrato")
        self.checkbox_7.grid(row=4, column=0, pady=(0,15), padx=20, sticky="n")
        self.checkbox_8 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="tremolo")
        self.checkbox_8.grid(row=4, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_9 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="fade")
        self.checkbox_9.grid(row=5, column=0, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_10 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="fade in")
        self.checkbox_10.grid(row=5, column=1, pady=(0, 15), padx=20, sticky="n")
        self.checkbox_11 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="fade out")
        self.checkbox_11.grid(row=6, column=0, pady=(0, 34), padx=20, sticky="n")
        self.checkbox_12 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="tpl")
        self.checkbox_12.grid(row=6, column=1, pady=(0, 34), padx=20, sticky="n")


        # set default values
        self.checkbox_1.select()
        self.optionmenu_1.set("Default")




if __name__ == "__main__":
    app = App()
    app.mainloop()