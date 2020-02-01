from Source.IO import data, hash_table
from Source.Core.ChComponent import ChComponent



class rEnergy():
    def __init__(self, new_energy):
        self.value = 0.0
        self._zero = 0.0

class ChCompound(data):
    def __init__(self, file_location, _hash_table, energy=0.0, name="New Substance", parent=None, mod="new"):
        super().__init__(file_location, name, mod)
        self.children = []
        self.Energy = energy
        self.directory.mkdir(parents=True, exist_ok=True)
        self.parent = parent
        self.rBonds = []
        self.lBonds = []
        self.hash_index = None
        self.short_save.extend([ChComponent, "parent"])
        self.dont_save.append("hash_table")
        self.dont_save.append('rBonds')
        self.dont_save.append('lBonds')
        self.hash_table: hash_table = _hash_table
        if mod == "new":
            self.hash_index = _hash_table.add_item(self)
            self.save()


    def update(self):
        super().update()
        self.Energy = float(self.gui.Text.text)

    def get_hash(self):
        return str(self.directory)

    @staticmethod
    def load(file_location, name):
        path = file_location / (name + ".json")
        obj = ChCompound(file_location, name, mod="load")
        input_stream = data._load_json(path)
        obj.load_components(input_stream)
        return obj




    def setBound(self, other):
        self.rBonds.append(other)
        other.lBonds.append(self)

    def get_type_indeficator(self):
        return "ChCompound"

    def save(self):
        super().save("ChCompound")





