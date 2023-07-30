# Remove all .png files in the training folder
# and generate new ones from random tenor gifs
from os import listdir, remove
from glob import glob

for f in glob("*.png"):
    remove(f)

from gifpy import Gifpy
from os import getenv

tenor_token = getenv("GIF_TOKEN")
if not tenor_token:
    raise Exception("No gif token found")

gifpy = Gifpy(tenor_token, "en_US")

bad_gifs = [
    "https://media.discordapp.net/attachments/977197179477327903/1052649070587551824/Honeycam_.gif"
]
other_gifs = []


def get_gifs(query, limit=5):
    gifs = gifpy.search(query, limit=limit)
    for gif in gifs:
        other_gifs.append(gif.media.get_format("gif").url)


get_gifs("anime")
get_gifs("vrchat")
get_gifs("speech bubble")

# Download gifs to temp folder
import tempfile
import requests

other_temp_dir = tempfile.TemporaryDirectory()
for gif in other_gifs:
    r = requests.get(gif)
    with open(f"{other_temp_dir.name}/{gif.split('/')[-1]}", "wb") as f:
        f.write(r.content)

bad_temp_dir = tempfile.TemporaryDirectory()
for gif in bad_gifs:
    r = requests.get(gif)
    with open(f"{bad_temp_dir.name}/{gif.split('/')[-1]}", "wb") as f:
        f.write(r.content)

# Extract frames from gifs to training folder, with prefix
from sh import convert
from os import mkdir

mkdir("other")
mkdir("bad")

for gif in listdir(other_temp_dir.name):
    convert(
        f"{other_temp_dir.name}/{gif}", "-resize", "256x256", f"other/{gif}-%02d.png"
    )

for gif in listdir(bad_temp_dir.name):
    convert(f"{bad_temp_dir.name}/{gif}", "-resize", "256x256", f"bad/{gif}-%02d.png")

# Remove temp folders
other_temp_dir.cleanup()
bad_temp_dir.cleanup()
