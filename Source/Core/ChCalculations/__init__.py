from Source.IO import data
import os


class ChCalculations(data):


    def __init__(self, file_location ,step_name="step1"):
        self.Name: str = step_name
        self.status: bool = False
        self.input_creater = None
        self.parser = None
        self.directory = file_location / self.Name
        self.specifcation= ""
        self.add_information= ""
        self.saveFileName = self.directory / (self.Name + ".json")

        self.post_processing: []

    def decode_command(self):
        for command in self.post_processing:
            os.system(command)

    def push_in_next(self):
        self.decode_command()
        self.status = True

    def code_command(self):
        pass

    def generate_input(self):
        if bool(self.input_creater):
            pass
        else:
            print("Script for input creating is not choosen")

