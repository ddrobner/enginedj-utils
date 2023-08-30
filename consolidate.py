import sqlite3
from pathlib import Path
import shutil
from os import chdir
from os.path import abspath, relpath


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


# set paths
ENGINE_DB_PATH = Path("/home/david/Downloads/m.db")
CONSOLIDATE_PATH = Path("/home/david/engine_consolidate")

chdir(ENGINE_DB_PATH.parent)

# open db connection
db_con = sqlite3.connect(ENGINE_DB_PATH)
cursor = db_con.cursor()
cursor.execute("SELECT id, path FROM Track ORDER BY id ASC;")

# load tracks into a format we can work with
tracks = []

for t in cursor.fetchall():
    tracks.append(Track(t[0], t[1]))

for t in tracks:
    # move track file here
    #print(f'UPDATE Track SET path = "{relpath(t.path, ENGINE_DB_PATH.parent)}" WHERE id = {t.id}')
    cursor.execute(f'UPDATE Track SET path = "{relpath(CONSOLIDATE_PATH / t.path.name, ENGINE_DB_PATH.parent)}" WHERE id = {t.id}')

db_con.commit()
cursor.execute("SELECT path FROM Track WHERE id = 420;")

db_con.close()