from Source.IO import data
from Source.Core.ChComponent.ChComponent import ChComponent


class rEnergy():
    def __init__(self, new_energy):
        self.value = 0.0
        self._zero = 0.0

class ChCompound(data):
    def __init__(self, file_location,  energy=0.0, name="New Substance"):
        super().__init__(file_location, name)
        self.components = []
        self.Energy = energy
        self.directory.mkdir(parents=True, exist_ok=True)
        self._zero = 0.0
        self.rBonds = []
        self.lBonds = []
        self.short_save.extend([ChComponent])
        self.save()


    def update(self):
        super().update()
        self.Energy = float(self.gui.Text)


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


    def setBound(self, other, boundPos):
        if boundPos == "r":
            self.rBonds.append(other)
            other.lBonds.append(self)
        else:
            self.lBonds.append(other)
            other.rBonds.append(self)


    def save(self):
        self.dont_save.append('rBonds')
        self.dont_save.append('lBonds')
        super().save()





