import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from glob import glob
import librosa
import librosa.display
import IPython.display as ipd
import soundfile as sf
from itertools import cycle
import scipy
from scipy import signal
import math
import audiomentations
import soundfile as sf
import pygame
import tkinter as tk
from tkinter import filedialog

import sys
sys.path.append('pafx-main')
from pafx.comb import Comb
from pafx.allpass import Allpass
from pafx.tapped_delay_line import TappedDelayLine
from pafx.reverb import Reverb, ReverbConfig
from pafx.equalizer import Equalizer
from pafx.echo import Echo
from pafx.chorus import Chorus
from pafx.flanger import Flanger
from pafx.vibrato import Vibrato
from pafx.tremolo import Tremolo
from pafx.fade import Fade, FadeIn, FadeOut

def noise(data, noise_factor):
    noise_amp = noise_factor*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data

def stretch(data, smpl_rate):
    return librosa.effects.time_stretch(data,rate=smpl_rate)

def shift(data):
    shift_range = int(np.random.uniform(low=-5, high = 5)*1000)
    return np.roll(data, shift_range)

def pitch(data, sampling_rate, pitch_factor):
    return librosa.effects.pitch_shift(data, sr=sampling_rate, n_steps=pitch_factor)

def intensity(data, percussive_rate, harmonic_rate):
    y_harmonic, y_percussive = librosa.effects.hpss(data)
    y_percussive_louder = np.multiply(y_percussive, percussive_rate)
    y_harmonic_louder = np.multiply(y_harmonic, harmonic_rate)
    y_total = y_harmonic_louder + y_percussive_louder
    return y_total

def test_allpass(data, sample_rate):
    x, fs  = data, sample_rate
    allpass = Allpass(100, 0.7)

    ya = np.zeros(len(x))
    # Start Processing
    for i in range(len(x)):
        ya[i] = allpass.process(x[i])

    #output_file = "audios/results/allpass.wav"
    ya = ya / max(np.abs(ya))
    #sf.write(output_file, ya, fs)
    return ya, fs

def test_comb(data, sample_rate):
    x, fs  = data, sample_rate
    comb = Comb(100, 0.9, 0)

    yc = np.zeros(len(x))
    # Start Processing
    for i in range(len(x)):
        yc[i] = comb.process(x[i])

    # Save Results
    #output_file = "audios/results/comb.wav"
    yc = yc / max(np.abs(yc))
    #sf.write(output_file, yc, fs)
    return yc, fs

def test_tpl(data, sample_rate):
    x, fs  = data, sample_rate

    tap_delays = [190,  949,  993,  1183, 1192, 1315,
                    2021, 2140, 2524, 2590, 2625, 2700,
                    3119, 3123, 3202, 3268, 3321, 3515]

    tap_gains = [.841, .504, .49,  .379, .38,  .346,
                    .289, .272, .192, .193, .217,  .181,
                    .18,  .181, .176, .142, .167, .134]

    tdl = TappedDelayLine(tap_delays, tap_gains)  

    yt = np.zeros(len(x))
    # Start Processing
    for i in range(len(x)):
        yt[i] = tdl.process(x[i])

    # Save Results
    #output_file = "audios/results/tpl.wav"
    yt = yt / max(np.abs(yt))
    #sf.write(output_file, yt, fs)
    return yt, fs

def test_eq(data, sample_rate, hz_32, hz_63, hz_125, hz_250, hz_500, hz_1000, hz_2000, hz_4000, hz_8000, hz_16000):
    x, fs  = data, sample_rate
    y = np.zeros(len(x))

    eq_gains = [hz_32, hz_63, hz_125, hz_250, hz_500, hz_1000, hz_2000, hz_4000, hz_8000, hz_16000]
    eq = Equalizer(eq_gains, fs)
    eq.dump()
    
    # Start Processing
    for i in range(len(x)):
        y[i] = eq.process(x[i])

    #output_file = "audios/results/eq.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_reverb(data, sample_rate):
    x, fs  = data, sample_rate

    config = ReverbConfig()
    config.room_scale = 70
    config.pre_delay = 50
    config.dry_gain = -5
    config.wet_gain = 5
    config.hf_damping = 30
    config.reverberance = 100
    config.stereo_width = 50
    config.er_gain = 0.2
    reverb = Reverb(config, fs)

    y = np.zeros(len(x))
    # Start Processing
    for i in range(len(x)):
        y[i] = reverb.process(x[i])

    #output_file = "audios/results/reverb.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_echo(data, sample_rate):
    x, fs  = data, sample_rate
    y = np.zeros(len(x))

    echo_gains = [0.5]
    echo_delays = [0.05]
    echo = Echo(fs, echo_delays, echo_gains, 0.5)
    # Start Processing
    for i in range(len(x)):
        y[i] = echo.process(x[i])

    #output_file = "audios/results/echo.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_chorus(data, sample_rate):
    x, fs  = data, sample_rate
    y = np.zeros(len(x))

    gains = [0.5]
    delays = [0.05]
    mod_widths = [0.005]
    mod_freqs = [2]
    dry_gain = 1
    chorus = Chorus(fs, delays, mod_freqs, mod_widths, gains, dry_gain)
    # Start Processing
    for i in range(len(x)):
        y[i] = chorus.process(x[i])

    #output_file = "audios/results/chorus.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_flanger(data, sample_rate):
    x, fs  = data, sample_rate
    y = np.zeros(len(x))

    delay = 0.01
    mod_width = 0.003
    mod_freq = 1
    flanger = Flanger(fs, delay, mod_width, mod_freq)
    # Start Processing
    for i in range(len(x)):
        y[i] = flanger.process(x[i])
    #output_file = "audios/results/flanger.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_vibrato(data, sample_rate):
    x, fs  = data, sample_rate
    mod_freq = 1.1
    mod_width = 0.008
    y = np.zeros(len(x))

    delay = 0.008
    vibrato = Vibrato(fs, delay, mod_width, mod_freq)
    # Start Processing
    for i in range(len(x)):
        y[i] = vibrato.process(x[i])
    
    #output_file = "audios/results/vibrato.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_tremolo(data, sample_rate):
    x, fs  = data, sample_rate
    mod_freq = 0.5
    mod_depth = 10
    y = np.zeros(len(x))
    
    tremolo = Tremolo(mod_freq, mod_depth, fs)
    # Start Processing
    for i in range(len(x)):
        y[i] = tremolo.process(x[i])

    #output_file = "audios/results/tremolo.wav"
    y = y / max(np.abs(y))
    #sf.write(output_file, y, fs)
    return y, sr

def test_fade(data, sample_rate):
    x, fs  = data, sample_rate
    y = np.zeros(len(x))

    in_length = 5
    out_start = 5
    out_length = 5
    fade = Fade(fs, in_length, out_start, out_length)
    # Start Processing
    for i in range(len(x)):
        y[i] = fade.process(x[i])
    y = y / max(np.abs(y))
    return y, sr

def test_fade_in(data, sample_rate):
    x, fs  = data, sample_rate
    y1 = np.zeros(len(x))

    in_length = 5
    fade_in = FadeIn(fs, in_length)
    # Start Processing
    for i in range(len(x)):
        y1[i] = fade_in.process(x[i])
    y1 = y1 / max(np.abs(y1))
    return y1, sr

def test_fade_out(data, sample_rate):
    x, fs  = data, sample_rate
    y2 = np.zeros(len(x))

    out_length = 5
    fade_out = FadeOut(fs, out_length)
    # Start Processing
    for i in range(len(x)):
        y2[i] = fade_out.process(x[i])
    y2 = y2 / max(np.abs(y2))
    return y2, sr

def getAudio():
    my_dir=filedialog.askopenfilename()
    global audio, sr
    audio, sr = librosa.load(my_dir)
    print(my_dir)

def saveTo():
    pygame.mixer.quit()
    dir=filedialog.askdirectory()
    sf.write(dir + "/output.wav", processed_data, Sampl_rate)

def changeAudio(isAllpass, isComb, isEcho, isReverbed, isChorus, isFlanger, isVibrato, isTremolo, isFade, isFadeIn, isFadeOut, isTpl, isEQ, currentWNoise, currentStrecth, currentPitch, currentIntensity, currentHarmonic, currentPercussive, hz_32, hz_63, hz_125, hz_250, hz_500, hz_1000, hz_2000, hz_4000, hz_8000, hz_16000):
    pygame.mixer.quit()
    WNoise_audio = noise(audio, currentWNoise)
    Strecth_audio = stretch(WNoise_audio, currentStrecth)
    Pitch_audio = pitch(Strecth_audio, sr, currentPitch)
    Intensity_audio = intensity(Pitch_audio, currentPercussive, currentHarmonic)
    sf.write("audios/results/processed.wav", Intensity_audio, sr)
    global processed_data, Sampl_rate
    processed_data, Sampl_rate = sf.read("audios/results/processed.wav")
    if isAllpass == 1:
        processed_data, Sampl_rate = test_allpass(processed_data, Sampl_rate)
    if isComb == 1:
        processed_data, Sampl_rate = test_comb(processed_data, Sampl_rate)
    if isTpl == 1:
        processed_data, Sampl_rate = test_tpl(processed_data, Sampl_rate)
    if isEcho == 1:
        processed_data, Sampl_rate = test_echo(processed_data, Sampl_rate)
    if isReverbed == 1:
        processed_data, Sampl_rate = test_reverb(processed_data, Sampl_rate)
    if isChorus == 1:
        processed_data, Sampl_rate = test_chorus(processed_data, Sampl_rate)
    if isFlanger == 1:
        processed_data, Sampl_rate = test_flanger(processed_data, Sampl_rate)
    if isVibrato == 1:
        processed_data, Sampl_rate = test_vibrato(processed_data, Sampl_rate)
    if isTremolo == 1:
        processed_data, Sampl_rate = test_tremolo(processed_data, Sampl_rate)
    if isFade == 1:
        processed_data, Sampl_rate = test_fade(processed_data, Sampl_rate)
    if isFadeIn == 1:
        processed_data, Sampl_rate = test_fade_in(processed_data, Sampl_rate)
    if isFadeOut == 1:
        processed_data, Sampl_rate = test_fade_out(processed_data, Sampl_rate)
    if isEQ == 1:
        processed_data, Sampl_rate = test_eq(processed_data, Sampl_rate, hz_32, hz_63, hz_125, hz_250, hz_500, hz_1000, hz_2000, hz_4000, hz_8000, hz_16000)
    sf.write("audios/results/LASTRESULTAUDIO.wav", processed_data, Sampl_rate)

def play():
    pygame.mixer.init()
    pygame.mixer_music.load("audios/results/LASTRESULTAUDIO.wav")
    pygame.mixer_music.play(loops=0)
