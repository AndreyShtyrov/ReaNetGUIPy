from Source.Core.ChProject import ChProject
from Source.IO import hash_data
from Source.IO import data
from Source.Core.ChCompound import ChCompound
from Source.Core.ChCalculations import ChCalculations
from Source.Core.ChComponent import ChComponent
from pathlib import Path
from Source.Core.ChBound import ChBound, ChNode

from Source.update import MainWidget
from Source.CanvasSubstance.Molecule import MolFrame
from Source.Bounding.Bound import Bound, Node


class ProjectObserver():

    def __init__(self, file_path, file_name):
        pass



class Loader():

    def __init__(self, file_path: Path, file_name: str, main_window):
        self.project,\
        self.hash_table = ChProject.load(file_path, file_name.split(".")[0])
        self.main_window = main_window
        self.rebase = False
        self.new_root = file_path
        if Path(self.hash_table._root_part_of_hash) == self.new_root:
            self.rebase = True


    def load_type_of_data(self):
        pass


    def chouse_constructor(self, obj_type):
        if obj_type == "ChCompound":
            return ChCompound
        elif obj_type == "ChBound":
            return ChBound
        elif obj_type == "ChCalculations":
            return ChCalculations
        elif obj_type == "Bound":
            return Bound
        elif obj_type == "ChComponent":
            return ChComponent
        elif obj_type == "MolFrame":
            return MolFrame
        elif obj_type == "Node":
            return Node
        elif obj_type == "ChNode":
            return ChNode

    def chouse_Frame_type(self, obj_type):
        if obj_type == "ChCompound":
            return MolFrame
        elif obj_type == "ChBound":
            return Bound
        elif obj_type == "ChNode":
            return Node

    def load(self):
        old_path = Path(self.hash_table._root_part_of_hash)
        for chash_data in self.hash_table.next_hash():
            if self.rebase:
                nhash = Path(chash_data.get_hash()).relative_to(old_path)
                nhash = self.new_root / nhash
                chash_data.update(nhash)
            input_dir = Path(chash_data.get_hash())
            obj = self.chouse_constructor(chash_data.get_type()).load(input_dir, chash_data.get_name())
            parent = self.hash_table.get_by_index(chash_data.get_parent_index)
            parent.new_child(obj)
            frame_class = self.chouse_Frame_type(obj.get_type_indeficator())
            gui = frame_class.load_Frame(obj.gui, obj)
            self.hash_table.get_by_index(obj.parent).addwiget(gui)



