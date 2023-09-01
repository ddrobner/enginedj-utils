import sqlite3
import shutil
import argparse

from pathlib import Path
from os import chdir
from os.path import abspath, relpath


parser = argparse.ArgumentParser(
    prog="Engine DJ Consolidate", 
    description="Simple Script to Consolidate Engine DJ Library"
    )

parser.add_argument('engine_database_path', help="Path to Engine DJ's m.db")
parser.add_argument('consolidate_path', help="The path to move your music files to")
parser.add_argument('--dry-run', action='store_true', help="Don't move any files or update database and print what would happen instead")

args = parser.parse_args()

# set paths from args
ENGINE_DB_PATH = Path(args.engine_database_path)
CONSOLIDATE_PATH = Path(args.consolidate_path)
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


chdir(ENGINE_DB_PATH.parent)

# open db connection
db_con = sqlite3.connect(ENGINE_DB_PATH)
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
        cursor.execute(f'UPDATE Track SET path = "{relpath(CONSOLIDATE_PATH / t.path.name, ENGINE_DB_PATH.parent)}" WHERE id = {t.id}')
    else:
        # print the source and final destinations if we are consolidating
        print(f"Moving {t.path} to {(CONSOLIDATE_PATH / t.path.name)}")


# save changes to the engine database
db_con.commit()
db_con.close()