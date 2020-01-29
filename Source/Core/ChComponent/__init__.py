from Source.IO import data
from pathlib import Path
import shutil


class ChComponent(data):

    def __init__(self, file_location, hash_table, name="New Component", mod="new", parent=None):
        super().__init__(file_location, name, mod)
        self._associated_file = None
        self.Energy = None
        self.parent = parent
        self.parser = None
        self.hash_table = hash_table
        self.short_save = ["parent"]
        self.dont_save.append("hash_table")
        if mod == "new":
            self.directory.mkdir(parents=True, exist_ok=True)
            self._sgeom: Path = self.directory / "scoord.xyz"
            if self._sgeom.is_file():
                with open(self._sgeom, "w") as input:
                    print("Please input geom here in xyz format with number of atom\n")
            self._geom: Path = self.directory / "coord.xyz"
            self.hash_index = hash_table.add_item(self)
            self.save()


    @staticmethod
    def load(file_location, name):
        path = file_location / (name + ".json")
        obj = ChComponent(file_location, name, mod="load")
        input_stream = data._load_json(path)
        obj.load_components(input_stream)
        return obj

    def get_type_indeficator(self):
        return "ChComponent"

    def get_hash(self):
        return str(self.directory)

    def set_energy(self, energy):
        self.Energy = energy

    def get_right(self):
        pass

    def get_left(self):
        pass

    def get_energy_from_file(self):
        if self.parser is not None:
            try:
                self.Energy = self.parser(self.directory/ "result.out")
            except:
                print("Parser raise a Error")
        else:
            print("Do not setup any parser")

    def set_parser(self):
        pass

    def get_geometry(self):
        if self._check_geom_file_is_not_empty(self._geom):
            pass
        elif self._check_geom_file_is_not_empty(self._sgeom):
            pass
        print("Geometry wasnot founded")

    def get_opt_log(self):
        pass


    def _check_geom_file_is_not_empty(self, file):
        with open(file, "r") as input:
            try:
                line = next(input)
                if "Please input geom here in xyz" in line:
                    return False
                else:
                    return True
            except:
                print(str(file) + "was corrupted")
                shutil.rmtree(str(file))

