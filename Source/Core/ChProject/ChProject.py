from Source.IO import data
from Source.Core.ChCompound.ChCompound import ChCompound
from pathlib import Path

class ChProject(data):

    def __init__(self, file_path, name="New Project"):
        super().__init__()
        self.Name = name
        self.directory = file_path / self.Name
        self.saveFileName = self.directory / (self.Name + ".json")
        self.compounds = []
        self.projects = []
        self.directory.mkdir(parents=True, exist_ok=True)
        self.short_save.extend([ChCompound])

    def add_new_compound(self, compound_name):
        self.compounds.append(ChCompound(self.directory/ compound_name, name=compound_name))

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


