import sqlite3
import shutil
import argparse

from pathlib import Path
from sys import exit
from os import chdir
from os.path import abspath, relpath


# set up argument parsing
parser = argparse.ArgumentParser(
    prog="Engine DJ Consolidate", 
    description="Simple Script to Consolidate Engine DJ Library"
    )

parser.add_argument('engine_library_path', help="Path to Engine Library")
parser.add_argument('consolidate_path', help="The path to move your music files to")
parser.add_argument('--dry-run', action='store_true', help="Don't move any files or update database and print what would happen instead")

# load our arguments
args = parser.parse_args()

# set paths from args
ENGINE_LIBRARY_PATH = Path(args.engine_library_path)
CONSOLIDATE_PATH = Path(args.consolidate_path)

# and the dry run flag
DRY_RUN = bool(args.dry_run)

# class to nicely keep track of the relevant track information
class Track:
    def __init__(self, track_id: int, track_path: Path):
        self._id = track_id
        self._path = Path(abspath(track_path))

    @property
    def id(self):
        return self._id

    @property
    def path(self):
        return self._path
    
    @id.setter
    def id(self, val: int):
        self._id = val 
    
    @path.setter
    def path(self, val: Path):
        self._path = abspath(val) 

    def __str__(self):
        return f"ID: {self.id} Path: {self.path}"


if not DRY_RUN:
    print("ARE YOU SURE YOU WANT TO CONSOLIDATE YOUR LIBRARY?")
    print("THIS MEANS MOVING ALL OF YOUR MUSIC FILES INTO THE SAME FOLDER.")
    print("THIS SCRIPT COMES WITH NO GUARANTEES AND MAY BREAK YOUR LIBRARY")
    print("SO MAKE SURE YOU HAVE A BACKUP.")
    print("To continue, enter 'y'")
    confirmation = input()
    if confirmation != 'y':
        exit()

# chdir to engine db path to handle relpaths
chdir(ENGINE_LIBRARY_PATH)

# open db connection
db_con = sqlite3.connect(ENGINE_LIBRARY_PATH / "Database2/m.db")
cursor = db_con.cursor()
cursor.execute("SELECT id, path FROM Track ORDER BY id ASC;")

# load tracks into a format we can work with
tracks = []

for t in cursor.fetchall():
    tracks.append(Track(t[0], t[1]))

# actually move and update the engine database
for t in tracks:
    if not DRY_RUN:
        # move the tracks if we're not doing a dry run and update the database
        shutil.move(src=t.path, dst=(CONSOLIDATE_PATH / t.path.name))
        cursor.execute(f'UPDATE Track SET path = "{relpath(CONSOLIDATE_PATH / t.path.name, ENGINE_LIBRARY_PATH.parent)}" WHERE id = {t.id}')
    else:
        # print the source and final destinations if we are consolidating
        print(f"Would have moved {t.path} to {(CONSOLIDATE_PATH / t.path.name)}")


# save changes to the engine database
db_con.commit()
db_con.close()

print("All Done :)")