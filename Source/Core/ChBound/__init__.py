from Source.IO import data
from pathlib import Path
import numpy as np


class ChBound(data):


    def __init__(self, hash_table, lBound=None, rBound=None, mod="new"):
        self.components = []
        self.rBonds = rBound
        self.lBonds = lBound
        self.dont_save.append("parent")
        self.short_save.extend()
        hash_table.add_item(self)
        self.hash_table = hash_table
        self.dont_save.append("hash_table")
        if mod == "new":
            self.save()

    def get_hash(self):
        pass


    @staticmethod
    def load(file_location, name):
        path = file_location / (name + ".json")
        obj = ChBound(file_location, name, mod="load")
        input_stream = data._load_json(path)
        obj.load_components(input_stream)
        return obj

