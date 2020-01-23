from Source.IO import data
from pathlib import Path
import numpy as np


class ChBound(data):


    def __init__(self, hash_table, lBound, rBound):
        self.components = []
        self.rBonds = rBound
        self.lBonds = lBound
        self.dont_save.append("parent")
        self.short_save.extend()
        hash_table.add_item(self)
        self.hash_table = hash_table
        self.dont_save.append("hash_table")
        self.save()

    def get_hash(self):
        pass

