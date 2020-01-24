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


class hash_data():

    def __init__(self, input_hash):
        path = Path(input_hash)
        self.directory = path.parent.absolute()
        self.name = path.name
        self.parent = path.parent.name

    def get_name(self):
        return self.name

    def get_dir(self):
        return self.directory

    def get_parent(self):
        return self.parent


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

    def __init__(self, file_location: pathlib.Path, mod="new", name="new"):
        if mod == "new":
            self.Name = self._search_aval_name(file_location, name)
        else:
            self.Name = name
        self.directory = file_location / self.Name
        self.saveFileName = self.directory / (self.Name + ".json")

        self.short_save = []
        self.dont_save: list = ['dont_save', 'saveFileName', 'directory', 'short_save']



    def update(self):
        if hasattr(self, 'gui'):
            new_name = self.gui.Name.text
            if self.Name != new_name:
                self.rename(new_name)



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

    @staticmethod
    def _search_aval_name(file_location: Union[str, Path], name):
        value = -1
        if type(file_location) is str:
            file_location = Path(file_location)
        for component in file_location.iterdir():
            if name in component.name:
                if name == component.name:
                    value = 0
                else:
                    try:
                        t = int(component.name.split(name)[-1])
                    except ValueError:
                        t = component.name.split(name)[-1]
                        t = int(t.split(".")[0])
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

    def read_dict_by_child_name(self, child_name: str):
        path = self.directory / self.Name / (child_name + ".json")
        return self._load_json(path)

    def load_components(self, input_dict: dict):
        for key, vaule in input_dict.items():
            setattr(self, vaule, key)


    @staticmethod
    def _load_json(file: pathlib.Path)->  Union[list, dict]:
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

class hash_table():
    _hash_tables: list
    _hash_links: list
    _init: bool
    _updating: bool

    def __init__(self, parent):
        self._hash_links = parent
        self._hash_tables = parent.get_hash()
        self._init = True
        self._updating = False
        self._root_part_of_hash = parent.directory

    def get_by_hash(self, input_hash):
        if not self._updating:
            for i in range(len(self._hash_tables)):
                if input_hash == self._hash_tables[i]:
                    return self._hash_links[i]
        else:
            print(" Try later")

    def get_index_by_hash(self, input_hash):
        for i in range(len(self._hash_tables)):
            if input_hash == self._hash_tables[i]:
                return i

    def add_item(self, item):
        self._hash_tables.append(item.get_hash())
        self._hash_links.append(item)

    def update_hash(self):
        self._updating = True
        temporary_hash = self._hash_links[0].directory
        if temporary_hash != self._root_part_of_hash:
            self._root_part_of_hash = temporary_hash
        for i in range(1, len(self._hash_links)):
            temporary_hash = self._hash_tables[i].get_hash()
            if temporary_hash != self._hash_links[i].get_hash():
                self._hash_tables[i] = temporary_hash
        self._updating = False

    def next_hash(self):
        for _hash in self._hash_tables:
            yield _hash

    def get_index_by_id(self, obj):
        for index,  link in enumerate(self._hash_links):
            if link is obj:
                return index


    @staticmethod
    def load_from_list(parent, input_list):
        obj = hash_table(parent)
        obj._init = False
        obj._hash_tables.extend(input_list)
        return obj

    def convert_in_dictionary(self):
        result = dict()
        result.update({"_hash_tables": self._hash_tables})
        result.update({"_root_part_of_hash": self._root_part_of_hash})
        return result

    def del_by_hash(self, input_hash):
        index = self.get_index_by_hash(input_hash)
        self._hash_tables.remove(self._hash_tables[index])
        self._hash_links.remove(self._hash_links[index])

    @staticmethod
    def load_project(path_to_file, file_name):
        pass




