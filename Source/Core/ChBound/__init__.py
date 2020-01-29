from Source.IO import data
from pathlib import Path
import numpy as np


class ChBound(data):

    def __init__(self, hash_table, lBound=None, rBound=None, mod="new", parent = None):
        self.children = []
        self.rBonds = rBound
        self.lBonds = lBound
        self.short_save.extend("parent", "rBound", "lBound")
        self.parent = parent
        self.directory = lBound.diretory
        self.saveFileName = lBound.saveFileName
        hash_table.add_item(self)
        self.hash_index = self.hash_table = hash_table
        self.dont_save.append("hash_table")
        if mod == "new":
            self.save()

    def get_hash(self):
        return "Bound: " + str(self.rBonds.get_hash() + str(self.lBonds.get_hash()))

    @staticmethod
    def load(file_location, name):
        path = file_location / (name + ".json")
        obj = ChBound(file_location, name, mod="load")
        input_stream = data._load_json(path)
        obj.load_components(input_stream)
        return obj

    def save(self):
        super().save("ChBound")


    def get_type_indeficator(self):
        return "ChBound"



class ChNode(data):

    def __init__(self, gui, parent):
        self.parent = parent
        self.gui = gui

    def _convert_in_dictionary(self):
        result = dict()
        result = {"gui": self.gui.load}
        return result

    def save(self):
        super().save("ChNode")

    def get_type_indeficator(self):
        return "ChNode"