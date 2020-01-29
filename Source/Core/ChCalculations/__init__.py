from Source.IO import data
import os


class ChCalculations(data):


    def __init__(self, file_location, hash_table, name="step1", mod="new", parent=None):
        super().__init__(file_location, name, mod)
        self.status: bool = False
        self.input_creater = None
        self.parser = None
        self.specification = ""
        self.add_information = ""
        self.parent = parent
        self.directory.mkdir(parents=True, exist_ok=True)
        self.post_processing = []
        self.next_step = [ChCalculations, "parent"]
        self.post_processing: []
        self.hash_table = hash_table
        self.dont_save.append("hash_table")
        if mod == "new":
            self.hash_index = hash_table.add_item(self)
            self.save("ChCalculations")

    def get_hash(self):
        return str(self.directory)

    def get_type_indeficator(self):
        return "ChCalculations"

    def update(self):
        super().update()
        self.specification = self.gui.Text

    def decode_command(self):
        for command in self.post_processing:
            os.system(command)

    @staticmethod
    def load(file_location, name):
        path = file_location / (name + ".json")
        obj = ChCalculations(file_location, name, mod="load")
        input_stream = data._load_json(path)
        obj.load_components(input_stream)
        return obj

    def push_in_next(self):
        self.decode_command()
        self.status = True

    def code_command(self):
        pass

    def add_next_step(self, other):
        self.next_step.append(other)

    def generate_input(self):
        if bool(self.input_creater):
            pass
        else:
            print("Script for input creating is not choosen")

