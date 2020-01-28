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

    def __init__(self, obj, obj_index, parent_index):
        path = Path(obj.directory)
        self.directory = parent_index
        self.name = path.name
        self.parent = path.parent
        self.type = str(type(obj))


    def load(self, input_dir):
        pass

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
    hash_index: int
    def __init__(self, file_location: pathlib.Path, name="new", mod="new"):
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

    def save(self, type_of_object: str):

        rdict = self._convert_in_dictionary(self.Name, self)
        if isinstance(rdict, list):
            rdict = dict({"type": type_of_object, "list_of_components": rdict})
        else:
            rdict.update({"type": type_of_object})
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


    def _convert_in_dictionary(self, name, convert_object) -> Union[list, dict]:
        result_dic = {}
        if self._check_type_saving(convert_object) \
                or self._check_attr_name_saving(name):
            return {name: convert_object.hash_index}
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
            if not isinstance(t_obj, str):
                if isinstance(obj, t_obj):
                    return True
        return False

    def _check_attr_name_saving(self, attr_name):
        for name in data.short_save:
            if isinstance(name, str):
                if attr_name == name:
                    return True
        return False



    def createdir(self, directory=None):
        if bool(directory):
            self.directory.mkdir(parents=True, exist_ok=True)
        else:
            directory.mkdir(parents=True, exist_ok=True)


class hash_table():
    _hash_tables: list = []
    _hash_links: list = []
    _init: bool
    _updating: bool
    _hash_index_table: list = []
    _next_new_avail_index: int = -1

    def __init__(self, parent):
        self._init = True
        self._updating = False
        self.add_item(parent)
        self._root_part_of_hash = parent.directory

    def get_next_avail_index(self):
        self._next_new_avail_index += 1
        return self._next_new_avail_index

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
                return self._hash_index_table[i]

    def add_item(self, item):
        self._hash_tables.append(item.get_hash())
        self._hash_links.append(item)
        avail_index = self.get_next_avail_index()
        self._hash_index_table.append(avail_index)
        return avail_index

    def get_by_index(self, index):
        for i, cindex in enumerate(self._hash_index_table):
            if cindex == index:
                return self._hash_links[i]

    def is_loaded(self, index):
        if index < (len(self._hash_links) - 1):
            return True
        return False

    def update_hash(self):
        self._updating = True
        temporary_hash = self._hash_links[0].directory
        if temporary_hash != self._root_part_of_hash:
            self._root_part_of_hash = temporary_hash
        for i in range(1, len(self._hash_links)):
            temporary_hash = self._hash_links[i].get_hash()
            if temporary_hash != self._hash_tables[i]:
                self._hash_tables[i] = temporary_hash
        self._update_index_table()
        self._updating = False

    def _update_index_table(self):
        new_list = [item.hash_index for item in self._hash_links]
        self._hash_index_table = new_list

    def next_hash(self):
        iter_hash = iter(self._hash_tables)
        _ = next(iter_hash)
        for _hash in iter_hash:
            yield _hash

    def get_index_by_id(self, obj):
        for index,  link in enumerate(self._hash_links):
            if link is obj:
                return index

    def next_index(self):
        iter_index = iter(self._hash_index_table)
        _ = next(iter_index)
        for _index in iter_index:
            yield _index



    @staticmethod
    def load_from_list(parent, input_dict):
        obj = hash_table(parent)
        obj._init = False
        obj.add_item(parent)
        obj._hash_tables.extend(input_dict["_hash_tables"])
        obj._root_part_of_hash = input_dict["_root_part_of_hash"]
        obj._next_new_avail_index = input_dict["_next_new_avail_index"]
        obj._hash_index_table.extend(input_dict["_hash_index_table"])
        return obj

    def convert_in_dictionary(self):
        result = dict()
        result.update({"_hash_tables": [str(x) for x in self._hash_tables]})
        result.update({"_root_part_of_hash": str(self._root_part_of_hash)})
        result.update({"_hash_index_table": self._hash_index_table})
        result.update({"_next_new_avail_index": self._next_new_avail_index})
        return result

    def del_by_hash(self, input_hash):
        index = self.get_index_by_hash(input_hash)
        self._hash_tables.remove(self._hash_tables[index])
        self._hash_links.remove(self._hash_links[index])


