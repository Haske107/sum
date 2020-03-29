


from os import listdir
import os.path

import random
from random import randint
import uuid
import IPython.display as ipd
import librosa, librosa.display
from moviepy.editor import *
import math
import csv

FinalVisual = VideoFileClip('./renders/Limp1.mp4')

SONG_PATH = "./audio/SUMTRACK.mp3"



print("Audio time")
audio = AudioFileClip(SONG_PATH)


new_audioclip = CompositeAudioClip([audio])

FinalVisual.audio = new_audioclip
# print("Set audio")
# FinalAV = FinalVisual.set_audio(new_audioclip.set_duration(FinalVisual.duration))

# render video
FinalVisual.write_videofile("./renders/Limp2.mp4", codec='libx264', fps=24)