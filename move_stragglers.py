### Script to move music files which aren't in your engine library to a new folder

import sqlite3
import shutil
import glob
import argparse

from pathlib import Path
from os.path import abspath
# set up argument parsing
parser = argparse.ArgumentParser(
    prog="Engine DJ Consolidate", 
    description="Simple Script to Consolidate Engine DJ Library"
    )

parser.add_argument('engine_library_path', help="Path to Engine Library")
parser.add_argument('music_path', help="Path to Music Folder")
parser.add_argument('move_path', help="The path to move your music files to")

# load our arguments
args = parser.parse_args()

# set paths from args
ENGINE_LIBRARY_PATH = Path(args.engine_library_path)
MOVE_PATH = Path(args.move_path)
MUSIC_PATH = Path(args.music_path)

# listing all supported filetypes by engine DJ so we don't move around random files
music_file_extensions = ["AAC", "M4A", "AIF", "AIFF", "ALAC", "FLAC", "MP3", "MP4", ".OGG", ".WAV"]

# open the db con, read tracknames and close
db_con = sqlite3.connect(ENGINE_LIBRARY_PATH / "Database2/m.db")
cursor = db_con.cursor()
cursor.execute("SELECT filename FROM Track ORDER BY id ASC;")

TRACK_FNAMES = [x[0] for x in cursor.fetchall()]
print(len(TRACK_FNAMES))

db_con.close()


# now we recursively iterate over the music path
for f in glob.iglob("*", root_dir=Path(MUSIC_PATH), recursive=True):
    # get the extension
    extension = f.split(".")[-1].upper()
    if (f not in TRACK_FNAMES) and (extension in music_file_extensions):
        # and if it's not in the list of filenames, we move it
        shutil.move(abspath(str(MUSIC_PATH / Path(f))), abspath(str(MOVE_PATH / Path(f))))