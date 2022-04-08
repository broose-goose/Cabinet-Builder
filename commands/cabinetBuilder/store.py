
from dataclasses import dataclass
from typing import Union

from ...lib.cabnietBuilder import data as cb_data

@dataclass
class Store:
    loadedFile: Union[cb_data.LoadedFile, None]
    def clear(self):
        self.loadedFile = None