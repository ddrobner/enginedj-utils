# a file to store the track class for future reuse

from pathlib import Path
from os.path import abspath

class Track:
    def __init__(self, track_id: int, track_path: Path, energy: int = 0):
        self._id = track_id
        self._path = Path(abspath(track_path))
        self._energy = energy

    @property
    def id(self):
        return self._id

    @property
    def path(self):
        return self._path

    @property
    def energy(self):
        return self._energy
    
    @id.setter
    def id(self, val: int):
        self._id = val 
    
    @path.setter
    def path(self, val: Path):
        self._path = Path(abspath(val))

    @energy.setter
    def energy(self, val: int):
        self._energy = val

    def __str__(self):
        return f"ID: {self.id} Path: {self.path}"