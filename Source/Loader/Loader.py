from Source.Core.ChProject import ChProject
from Source.IO import hash_data
from Source.Core.ChCompound import ChCompound
from Source.Core.ChCalculations import ChCalculations
from Source.Core.ChBound import ChBound
from Source.Core.ChComponent import ChComponent

from Source.update import MainWidget
from Source.CanvasSubstance.Molecule import MolFrame
from Source.Bounding.Bound import Bound


class ProjectObserver():

    def __init__(self, file_path, file_name):
        pass



class Loader():

    def __init__(self, file_path, file_name, main_window):
        self.project,\
        self.hash_table = ChProject.load(file_path, file_name)
        self.main_window = main_window

    def load_type_of_data(self):
        pass



    def load(self):
        for obj_index in self.hash_table.next_index():
            self.hash_table.get_by_index(obj_index).get_hash()








