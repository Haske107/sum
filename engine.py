from os import listdir
import random
from random import randint
import uuid
import numpy, scipy, matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
from moviepy.editor import *
import math


# GLOBAL VARIABLES
CLIPS_RELATIVE_PATH = "./clips/"
SLUG_RELATIVE_PATH = "./slug/"
SECONDARY_RELATIVE_PATH = "./secondary/"
SONG_PATH = "./audio/limp.mp3"
OPEN_SLUGS = []


# OBJECTS
class Clip:
    def __init__(self, MPObj):
        self.MPObj = MPObj
        self.Slot = 0
        self.Duration = 0
        self.Sentiment = 0
        self.Path = ''


class Song:
    def __init__(self):
        self.Name = "Test Song"
        self.Duration = random.randrange(130, 360)


class RenderToken:
    def __init__(self):
        self.ID = uuid.uuid1()
        self.Chronology = random.randrange(2)
        self.Sentiment = random.randrange(5)


class Range:
    def __init__(self, token):
        temp_high = token.Sentiment + random.randrange(3)
        if temp_high > 5:
            temp_high = 5
        temp_low = token.Sentiment - random.randrange(3)
        if temp_low < 0:
            temp_low = 0
        if abs(temp_high - temp_low) < 2:
            if temp_high == 5:
                temp_low = temp_low - 2
            elif temp_low == 0:
                temp_high = temp_high + 2
            else:
                temp_high = temp_high + 1
                temp_low = temp_low - 1
        if temp_high < temp_low:
            temptemp = temp_high
            temp_high = temp_low
            temp_low = temptemp
        self.high = temp_high
        self.low = temp_low


# FUNCTIONS
def select_clips_for_all_slots(master_clips, sentiment_range):
    selected_clips = []
    for slot in master_clips:
        selected_clips.append(select_clip_for_slot(slot, random.randrange(sentiment_range.low, sentiment_range.high)))
    return selected_clips


def select_clip_for_slot(clips, target):
    return min(clips, key=lambda x: abs(int(x[6]) - target))


def categorize_clips_by_slot(clip_bin):
    slotted_array = []
    for Slot in range(50):
        temp_array = []
        for Clip in range(5):
            temp_array.append(clip_bin.pop())
        slotted_array.append(temp_array)
    return slotted_array


def clipify(clip_array):
    print("Clipify")
    initialized_clips = []
    for ClipName in clip_array:
        MPObject = VideoFileClip("./clips/" + ClipName)
        New_Clip = Clip(MPObject)
        initialized_clips.append(New_Clip)
    return initialized_clips


def add_slugs(clips):

    print("adding slugs")

    master_timeline = []
    current_duration = 0

    for clip in clips:

        master_timeline.append(clip)

        current_duration += clip.MPObj.duration

        time_to_next_beat = find_next_beat(current_duration)

        if time_to_next_beat >= .5:
            slug_duration = 6/24
        elif time_to_next_beat < 6/24:
            slug_duration = 10/24
        else:
            slug_duration = time_to_next_beat

        Slug = createSlug(slug_duration)

        master_timeline.append(Slug)

        current_duration += slug_duration

    return master_timeline


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def createSlug(duration):

        print("Creating Slug")
        # SET DURATION TO TEST CLIPS
        Title = TextClip('.', color='black', size=(480, 640), bg_color="black", fontsize=30)

        # truncate and also set to nearest frame
        formatted_duration = truncate(duration, 3)

        # set to truncated duration
        TitleClip = Title.set_duration(formatted_duration)

        # check if the slug already exists
        for slug in OPEN_SLUGS:
            if slug.Path == "slug/Slug-" + str(formatted_duration) + ".mp4":
                print("Found Slug")
                return slug

        # if it exists import from global -- else create and store
        TitleClip.write_videofile("slug/Slug-" + str(formatted_duration) + ".mp4", codec='libx264', fps=24)
        Slug = Clip(VideoFileClip("slug/Slug-" + str(formatted_duration) + ".mp4"))
        Slug.Duration = formatted_duration
        Slug.Sentiment = 0
        Slug.Slot = 0
        Slug.Path = "slug/Slug-" + str(formatted_duration) + ".mp4"
        OPEN_SLUGS.append(Slug)
        return Slug



def find_next_beat(time):
    x, sr = librosa.load(SONG_PATH)
    ipd.Audio(x, rate=sr)
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=85, units='time')
    target = 0
    temp = 10
    for x in beat_times:
        if x > time and x - time < temp:
            temp = x - time
            target = x

    return target - time


def initialize_clips(clips):
    initiliazed_clips = []
    for clip in clips:
        tempClip = Clip()
        tempClip.duration


def concatenate_video_clips(clips):
    stripped_array = []
    for clip in clips:
        stripped_array.append(clip.MPObj)
    return concatenate_videoclips(stripped_array)


def add_secondary(clips):
    # INITIALIZE AUDIO AND GET DURATION
    y, sr = librosa.load(SONG_PATH)
    ipd.Audio(y, rate=sr)
    song_length = librosa.core.get_duration(y=y, sr=sr)

    # GET TOTAL TIME LINE DURATION
    total_clip_duration = 0
    for clip in clips:
        total_clip_duration += clip.MPObj.duration

    # FIND DIFFERENCE BETWEEN TIME LINE AND SONG DURATION
    difference = song_length - total_clip_duration

    # PICK CLIPS LESS THAN DIFF
    selected_clips = []
    secondary_bin = [f for f in listdir(SECONDARY_RELATIVE_PATH) if not f.startswith('.')]
    time_left = difference
    while time_left > 14:  # CHOOSING 4 ARBITRARILY-ISH
        selected_clip = random.choice(secondary_bin)
        if int(selected_clip[len(selected_clip)-5: len(selected_clip)-4]) < time_left:
            mp_object = VideoFileClip("./secondary/" + selected_clip)
            selected_clips.append(Clip(mp_object))
            time_left = time_left - int(selected_clip[len(selected_clip)-5: len(selected_clip)-4])

    # ADD CLIPS RANDOMLY INTO ARRAY
    clips_plus_secondary = clips
    for x in selected_clips:
        clips_plus_secondary.insert(randint(0, len(clips_plus_secondary)), x)

    return clips_plus_secondary


# MAIN FUNCTION
# generate render token
Token = RenderToken()
Range = Range(Token)
Song = Song()

print("SENTIMENT TOKEN GENERATED: ", Token.Sentiment)

# gather clips and meta data (in this case metadata is encoded in filename)
UNSORTED_PRIMARY_CLIP_POOL = [f for f in listdir(CLIPS_RELATIVE_PATH) if not f.startswith('.')]

# sort clips in ascending order
PRIMARY_CLIP_POOL = sorted(UNSORTED_PRIMARY_CLIP_POOL, key=lambda x: x)

# slotted clips bin
SLOTTED_CLIPS_POOL = categorize_clips_by_slot(PRIMARY_CLIP_POOL)

# choose clips for each slot
CHOSEN_CLIPS_POOL = select_clips_for_all_slots(SLOTTED_CLIPS_POOL, Range)

# initialize into clip objects
INITIALIZED_CLIP_POOL = clipify(CHOSEN_CLIPS_POOL)

# check for room for secondary clips (add if necessary)
CLIPS_AND_SECONDARY = add_secondary(INITIALIZED_CLIP_POOL)

# add slugs
CLIPS_AND_SLUGS = add_slugs(CLIPS_AND_SECONDARY)

# concatenate videos
print("Concatenating")
FinalVisual = concatenate_video_clips(CLIPS_AND_SLUGS)

print("Audio time")
audio = AudioFileClip(SONG_PATH)

print("Set audio")
FinalAV = FinalVisual.set_audio(audio)

# render video
FinalAV.write_videofile("./renders/Limp.mp4", codec='libx264', fps=24)
print(Token.Chronology, Token.ID, Token.Sentiment)




