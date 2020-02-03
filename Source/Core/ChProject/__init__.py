from Source.IO import data, hash_table
from Source.Core.ChCompound import ChCompound
from Source.Core.ChBound import ChBound
from Source.Core.ChCalculations import ChCalculations
from pathlib import Path


class ChProject(data):

    def __init__(self, file_path, gui, name="New Project", mod="new"):
        super().__init__(file_path, name=name, mod=mod)
        self.children = []
        self.general_method: [ChCalculations] = []
        self.directory.mkdir(parents=True, exist_ok=True)
        self.short_save.extend([ChCompound])
        self.parent = 0
        self._is_updating = False
        if mod == "new":
            self.hash_table = hash_table(self)
            self.hash_index = 0
            self.save()


    def get_hash(self):
        return self.directory


    def update(self, *kvargs):
        print(" update all tree of project")
        if not self._is_updating:
            self._is_updating = True
            for compound in self.children:
                compound.update()
            self.hash_table.update_hash()
            self.save()
            self._is_updating = False

    def add_child(self, child):
        self.children.append(child)
        child.set_parent(self)
        child.update()

    def new_child(self, compound_name="New Substance"):
        chc = ChCompound(self.directory, name=compound_name, parent=self, _hash_table=self.hash_table)
        self.children.append(chc)
        return chc

    @classmethod
    def load(cls, file_path, name):
        path = file_path / (name + ".json")
        input_stream = data._load_json(path)
        list_for_hash = input_stream.pop("hash_table")
        obj = ChProject(file_path, name, mod="load")
        obj.load_components(input_stream)
        _hash_table = hash_table.load_from_list(obj, list_for_hash)
        return obj, _hash_table

    def save(self):
        for compound in self.children:
            compound.save()
        super().save("ChProject")


    def get_type_indeficator(self):
        return "ChProject"

if __name__ == '__main__':
    proj_dir = Path.cwd()
    nameproject = "new1"
    chproject = ChProject(proj_dir, nameproject)
    chproject.new_child("tN2H2")
    chproject.save()


