from Source.IO import data
from pathlib import Path
import numpy as np


class ChBound(data):

    def __init__(self, parent = None, rBound=None, lBound=None, mod="new",  gui=None):
        self.children = []
        self.short_save = []
        self.rBonds = rBound
        self.lBonds = lBound
        self.short_save.extend(["parent", "rBound", "lBound"])
        self.parent = parent
        self.hash_table = parent.hash_table
        self.gui = gui
        if mod == "new":
            self.hash_index = parent.hash_table.add_item(self)
            self.save()

    def add_gui(self, gui):
        self.gui = gui

    def convert_in_dictionary(self):

        result = dict()
        result = {
            "parent": self.parent.hash_index,
            "nodes": [child.convert_in_dictionary() for child in self.children],
            "rBonds": self.rBonds.hash_index,
            "lBonds": self.lBonds.hash_index,
            "gui": None}
        return result

    def get_hash(self):
        return str(self.parent.get_hash())

    @staticmethod
    def load(file_location, name):
        path = file_location / (name + ".json")

        obj = ChBound(file_location, name, mod="load")
        input_stream = data._load_json(path)
        obj.load_components(input_stream)
        return obj

    def save(self):
        pass


    def get_type_indeficator(self):
        return "ChBound"



class ChNode(data):

    def __init__(self, parent, gui=None, mod="new"):
        self.parent = parent
        self.hash_table = parent.hash_table
        self.short_save = []
        self.dont_save = []
        self.gui = gui
        if mod == "new":
            self.hash_index = parent.hash_table.add_item(self)
            self.save()

    def get_hash(self):
        return str(self.parent.get_hash())

    def add_gui(self, gui):
        self.gui = gui

    def convert_in_dictionary(self):
        result = dict()
        result = {"parent": self.parent.hash_index,
                  "gui": self.gui.convert_in_dictionary()}
        return result

    def save(self):
        pass


    def get_type_indeficator(self):
        return "ChNode"