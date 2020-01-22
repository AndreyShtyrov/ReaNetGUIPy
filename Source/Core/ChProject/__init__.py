from Source.IO import data
from Source.Core.ChCompound import ChCompound
from Source.Core.ChCalculations import ChCalculations
from pathlib import Path


class ChProject(data):

    def __init__(self, file_path, name="New Project"):
        super().__init__(file_path, name)
        self.compounds = []
        self.general_method: [ChCalculations] = []
        self.directory.mkdir(parents=True, exist_ok=True)
        self.short_save.extend([ChCompound])
        self.calculations = []
        self._is_updating = False


    def update(self, *kvargs):
        print(" update all tree of project")
        if not self._is_updating:
            self._is_updating = True
            for compound in self.compounds:
                compound.update()
            for calc in self.calculations:
                calc.update()
            self.save()
            self._is_updating = False

    def add_new_compound(self, compound_name="New Substance"):
        chc = ChCompound(self.directory, name=compound_name, parent=self)
        self.compounds.append(chc)
        return chc

    def save(self):
        for compound in self.compounds:
            compound.save()
        super().save()

if __name__ == '__main__':
    proj_dir = Path.cwd()
    nameproject = "new1"
    chproject = ChProject(proj_dir, nameproject)
    chproject.add_new_compound("tN2H2")
    chproject.save()


