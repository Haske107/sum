from moviepy.editor import *
import random

# BUILD CLIP CONTENT

for x in range(10):
    #   SET DURATION TO TEST CLIPS
    dur = random.randrange(2, 8)
    Title = TextClip("SECONDARY" + str(dur), color='white', size=(480, 640), bg_color="purple", fontsize=30)
    TitleClip = Title.set_duration(dur)
    TitleClip.write_videofile("secondary/Secondary-" + str(dur) + ".mp4", codec='libx264', fps=24)


# for Slot in range(50):
#     for Clip in range(5):
#         if Clip == 0:
#             bgColor = 'red'
#         elif Clip == 1:
#             bgColor = 'orange'
#         elif Clip == 2:
#             bgColor = 'yellow'
#         elif Clip == 3:
#             bgColor = 'green'
#         elif Clip == 4:
#             bgColor = 'blue'
#
#         # BUILD CLIP CONTENT
#         Title = TextClip('Slot Number: ' + str(Slot) + '  \n\n\n Sentiment:    ' + str(Clip - 2), color='white',
#                              size=(480, 640), bg_color=bgColor, fontsize=30)
#
#         #   SET RANDOM DURATION TO TEST CLIPS
#         TitleClip = Title.set_duration(random.randrange(5, 50)/10)
#
#         if Slot < 10:
#             TitleClip.write_videofile("Clip0" + str(Slot) +  str(Clip) + ".mp4", codec='libx264', fps=24)
#         else:
#             TitleClip.write_videofile("Clip" + str(Slot) +  str(Clip) + ".mp4", codec='libx264', fps=24)
#
