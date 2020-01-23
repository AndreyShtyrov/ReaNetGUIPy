from Source.IO import data, hash_table
from Source.Core.ChComponent import ChComponent



class rEnergy():
    def __init__(self, new_energy):
        self.value = 0.0
        self._zero = 0.0

class ChCompound(data):
    def __init__(self, file_location, _hash_table, energy=0.0, name="New Substance", parent = None):
        super().__init__(file_location, name)
        self.components = []
        self.Energy = energy
        self.directory.mkdir(parents=True, exist_ok=True)
        self._zero = 0.0
        self.parent = parent
        self.rBonds = []
        self.lBonds = []
        self.dont_save.append("parent")
        self.short_save.extend([ChComponent])
        _hash_table.add_item(self)
        self.hash_table: hash_table = _hash_table
        self.dont_save.append("hash_table")
        self.save()


    def update(self):
        super().update()
        self.Energy = float(self.gui.Text.text)

    def get_hash(self):
        return str(self.directory)

    def get_left(self):
        for bounded in self.lBonds:
            yield bounded

    def get_right(self):
        for bounded in self.rBonds:
            yield bounded

    def calculate_Energy(self, previ):
        sum_Energy = 0
        for component in self.components:
            sum_Energy += component.Energy
        self.Energy = (sum_Energy - self._zero) *627.5


    def setBound(self, other):
        self.rBonds.append(other)
        other.lBonds.append(self)



    def save(self):
        self.dont_save.append('rBonds')
        self.dont_save.append('lBonds')
        super().save()





