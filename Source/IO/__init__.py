import json
import pathlib
from typing import Union
from pathlib import Path
import numpy as np
import shutil
import hashlib

import os
import time
import zipfile



def get_dir_tree(curr_path: pathlib.Path):
    for file in curr_path.iterdir():
        if file.is_dir():
            yield from get_dir_tree(file)
        elif file.is_file():
            yield file
    return


def treatment_exception(error: Exception):
    if error is PermissionError:
        return False


def make_dir_forced(curr_dir: pathlib.Path)-> None:
    if curr_dir.parent.is_dir():
        make_dir_forced(curr_dir.parent)
    else:
        curr_dir.mkdir()


def get_dir_tree_list(curr_path: pathlib.Path):
    result = []
    for file in get_dir_tree(curr_path):
        result.append(file)
    return result


def search_file_with_template_in_name(curr_path: pathlib.Path, template: str) -> Union[pathlib.Path, bool]:
    try:
        return _search_file_with_template_in_name(curr_path, template)
    except PermissionError:
        return False


def _search_file_with_template_in_name(curr_path: pathlib.Path, template: str) -> Union[pathlib.Path, bool]:
    main_dir = pathlib.Path.home()
    for file in curr_path.iterdir():
        if file.is_file():
            if template in file.name:
                return file
    if main_dir != curr_path:
        if curr_path.parent.is_dir():
            return search_file_with_template_in_name(curr_path.parent, template)
    return False

class data():

    def __init__(self, file_location: pathlib.Path, name="new"):
        self.Name = self._search_aval_name(file_location, name)
        self.directory = file_location / self.Name
        self.saveFileName = self.directory / (self.Name + ".json")

        self.short_save = []
        self.dont_save: list = ['dont_save', 'saveFileName', 'directory', 'short_save']



    def update(self):
        if hasattr(self, 'gui'):
            self.Name = self.gui.Name


    def add_gui(self, gui):
        self.gui = gui

    @staticmethod
    def convert_ndarray(array: np.ndarray):
        return array.tolist()

    @staticmethod
    def conver_to_json(instance):
        if type(instance) is pathlib.Path:
            try:
                return str(instance)
            except TypeError:
                pass
        try:
            json.dumps(instance)
            return instance
        except:
            return str(instance)

    def save(self):
        rdict = self._convert_in_dictionary(self.Name, self)
        self._save_json(self.saveFileName, rdict)

    def rename(self, name):
        if self.Name != name:
            new_directory = self.directory.parent / name
            shutil.move(str(self.directory), str(new_directory), copy_function=shutil.copytree)
            new_saveFileName = new_directory / (name + ".json")
            self.directory = new_directory
            self.saveFileName = self.directory / (self.Name + ".json")
            shutil.move(str(self.saveFileName), str(new_saveFileName))
            self.saveFileName = new_saveFileName
            self.Name = name
            self.save()


    def assotiate_with_file(self, file_str):
        file = Path(file_str)
        if file.is_file():
            if file.parent is not self.directory:
                shutil.copy(str(file), str(self.directory/ "result.out"))
            elif file.parent is self.directory and file.name != "result.out":
                shutil.move(str(file), str(self.directory/ "result.out"))
            else:
                print("The file was not founded")
                raise IOError

    def exclude_attr_from_saving(self, name):
        if name in self.dont_save:
            self.dont_save
            return False
        return True

    def _search_aval_name(self, file_location, name):
        value = -1
        for component in file_location.iterdir():
            if name in component.name:
                if name == component.name:
                    value = 0
                else:
                    t = int(component.name.split(name)[-1])
                    if t > value:
                        value = t
        acc = value + 1
        if acc != 0:
            return name + str(acc)
        else:
            return name


    def _convert_in_dictionary(self, name, convert_object):
        result_dic = {}
        if self._check_type_saving(convert_object):
            return {name: str(convert_object.directory.relative_to(self.directory))}

        if hasattr(convert_object, 'convert_in_dictionary'):
            return {name: convert_object.convert_in_dictionary()}
        elif hasattr(convert_object, '__dict__'):
            for key, value in convert_object.__dict__.items():
                if not callable(value):
                    if self.exclude_attr_from_saving(key):
                        result_dic.update(self._convert_in_dictionary(key, value))
        elif issubclass(type(convert_object), np.ndarray):
            t_value = self.convert_ndarray(convert_object)
            result_dic.update({name: t_value})
        elif issubclass(type(convert_object), list):
            t_value = []
            for item in convert_object:
                t_value.append(self._convert_in_dictionary(str(type(item).__name__), item))
            result_dic.update({name: t_value})
        else:
            if name is not "save_name":
                result_dic.update({name: self.conver_to_json(convert_object)})

        return result_dic

    def _load_json(self, file: pathlib.Path)->  Union[list, dict]:
        return json.load(open(file, "r"))

    def _save_json(self, file: pathlib.Path, data: dict):
        js_data = json.dumps(data, indent=2)
        file.write_text(js_data)

    def _check_type_saving(self, obj):
        for t_obj in self.short_save:
            if isinstance(obj, t_obj):
                return True
        return False

    def createdir(self, directory=None):
        if bool(directory):
            self.directory.mkdir(parents=True, exist_ok=True)
        else:
            directory.mkdir(parents=True, exist_ok=True)