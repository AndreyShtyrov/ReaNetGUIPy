from Source.IO import data
from pathlib import Path
import shutil


class ChComponent(data):

    def __init__(self, file_location, name="New Component"):
        super().__init__(file_location, name)
        self._associated_file = None
        self.Energy = None
        self.parser = None
        self.directory.mkdir(parents=True, exist_ok=True)
        self._sgeom: Path = self.directory / "scoord.xyz"
        if self._sgeom.is_file():
            with open(self._sgeom, "w") as input:
                print("Please input geom here in xyz format with number of atom\n")
        self._geom: Path = self.directory / "coord.xyz"



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

