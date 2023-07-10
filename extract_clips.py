import sys
import pandas as pd
from subprocess import call

PREFIX="~/data/projects/PInSoRo/freeplay_sandbox/data/"
OUT="./"

clips = pd.read_csv("ClipTimeStamps.csv")

# ffmpeg -i env_camera_skel.mkv -ss 00:00:30 -t 30 -an env_camera_skel_clip.mp4
for idx, clip in clips.iterrows():
    name = "clip_%02d.mp4" % clip["id"]
    name_skel = "clip_skel_%02d.mp4" % clip["id"]
    cmd = "ffmpeg -n -i " + PREFIX+ clip["clip"] + "/videos/env_camera_raw.mkv -ss " + clip["start"] + " -t 30 -an " + OUT + name
    cmd = "ffmpeg -n -i " + PREFIX+ clip["clip"] + "/videos/env_camera_skel.mkv -ss " + clip["start"] + " -t 30 -an " + OUT + name_skel
    call(cmd, shell=True)

print("<html><body>")

for idx, clip in clips.iterrows():
    name = "clip_%02d.mp4" % clip["id"]
    name_skel = "clip_skel_%02d.mp4" % clip["id"]
    print("""<h2>%s</h2><p><video width="960" height="540" controls>
  <source src="%s" type="video/mp4">
</video><video width="960" height="540" controls>
  <source src="%s" type="video/mp4">
</video></p>""" % (name, name, name_skel))

print("</body></html>")


