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
        self._hash_table = ChProject.load(file_path, file_name)




    def load(self):
        iter_hashs = iter(self._hash_table)
        _ = next(iter_hashs)
        for _hash in iter_hashs:
            hdata = hash_data(_hash)
            inp_dir = hdata.get_dir()
            name = hdata.get_name()
            parent = hdata.get_parent()
            



