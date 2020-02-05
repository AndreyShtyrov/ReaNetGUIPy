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

    def __init__(self, obj_hash ,obj_index, obj_type, parent_index):
        self.hash = obj_hash
        self.index = obj_index
        self.data_type = obj_type
        self.parent_index = parent_index

    def convert_in_dictionary(self):
        res = {"hash": str(self.hash),
               "index": self.index,
               "data_type": self.data_type,
               "parent_index": self.parent_index}
        return res

    @classmethod
    def load(cls, input_dict):
        return cls(input_dict["hash"],
                   input_dict["index"],
                   input_dict["data_type"],
                   input_dict["parent_index"])

    def get_hash(self):
        return self.hash

    def get_index(self):
        return self.index

    def get_type(self):
        return self.data_type

    def get_parent_index(self):
        return self.parent_index

    def get_name(self):
        path = Path(self.hash).name

    def update(self, obj_hash, parent_index=None):
        self.hash = str(obj_hash)
        if not parent_index:
            self.parent_index = parent_index


class hash_table():
    _hash_tables: [hash_data] = []
    _hash_links: list = []
    _init: bool
    _updating: bool

    def __init__(self, parent):
        self._init = True
        self._updating = False
        self._next_new_avail_index = -1
        self.add_item(parent)
        self._root_part_of_hash = parent.directory

    def get_next_avail_index(self):
        self._next_new_avail_index += 1
        return self._next_new_avail_index

    def get_by_hash(self, input_hash):
        if not self._updating:
            for i, chash_data in enumerate(self._hash_tables):
                if input_hash == chash_data.get_hash():
                    return self._hash_links[i]
        else:
            print(" Try later")

    def get_index_by_hash(self, input_hash):
        for chash_data in self._hash_tables:
            t_index = chash_data.get_index()
            if input_hash == t_index:
                return t_index

    def add_item(self, item):
        avail_index = self.get_next_avail_index()
        _hash_data =hash_data(item.get_hash(),
                              avail_index,
                              item.get_type_indeficator(),
                              self.get_index_by_id(item.parent))
        self._hash_tables.append(_hash_data)
        self._hash_links.append(item)
        return avail_index

    def get_by_index(self, index):
        for i, chash_data in enumerate(self._hash_tables):
            if index == chash_data.get_index():
                return self._hash_links[i]

    def is_loaded(self, index):
        if index < (len(self._hash_links) - 1):
            return True
        return False

    def update_hash(self):
        self._updating = True
        for i, chash_data in enumerate(self._hash_tables):
            chash_data.update(self._hash_links[i].get_hash(),
                       self._hash_links[i].parent)
        self._updating = False

    def next_hash(self):
        iter_hash = iter(self._hash_tables)
        _ = next(iter_hash)
        for _hash in iter_hash:
            yield _hash

    def get_index_by_id(self, obj):
        for index,  link in enumerate(self._hash_links):
            if link is obj:
                return self._hash_tables[index].get_index()

    def next_index(self):
        iter_index = iter(self._hash_tables)
        _ = next(iter_index)
        for chash_data in iter_index:
            yield chash_data.get_index()

    @staticmethod
    def load_from_list(parent, input_dict):
        obj = hash_table(parent)
        obj._init = False
        obj._hash_tables.extend(map(hash_data.load, input_dict["_hash_tables"]))
        obj._root_part_of_hash = input_dict["_root_part_of_hash"]
        obj._next_new_avail_index = input_dict["_next_new_avail_index"]
        return obj

    def convert_in_dictionary(self):
        result = dict()
        test = self._hash_tables[0]
        result.update({"_hash_tables": [x.convert_in_dictionary() for x in self._hash_tables]})
        result.update({"_root_part_of_hash": str(self._root_part_of_hash)})
        result.update({"_next_new_avail_index": self._next_new_avail_index})
        return result

    def del_by_hash(self, input_hash):
        index = self.get_index_by_hash(input_hash)
        self._hash_tables.remove(self._hash_tables[index])
        self._hash_links.remove(self._hash_links[index])




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
    children: []
    hash_index: int
    hash_table: hash_table


    def __init__(self, file_location: pathlib.Path, name="new", mod="new"):
        if mod == "new":
            self.Name = self._search_aval_name(file_location, name)
        else:
            self.Name = name
        self.directory = file_location / self.Name
        self.saveFileName = self.directory / (self.Name + ".json")
        self.short_save = []
        self.dont_save: list = ['dont_save', 'saveFileName', 'directory', 'short_save']



    def set_parent(self, parent):
        self.parent = parent
        self.update()

    def add_child(self, child):
        self.children.append(child)
        child.set_parent(parent=self)

    def find_in_children_by_index(self, index, input_dict) -> dict:
        children = input_dict["children"]
        for child in children:
            if child["index"] == index:
                return child


    def update(self):
        if hasattr(self, 'gui'):
            if hasattr(self.gui, "Name"):
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
                        if "." in t:
                            t = int(t.split(".")[0])
                        try:
                            t = int(t)
                        except ValueError:
                            t = value
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
            print(" try to save " + str(name))
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

    @staticmethod
    def convert_dict_in_values(converted_obj):
        if type(converted_obj) is dict:
            result = dict()
            for key, value in converted_obj.items():
                result.update({key: data.convert_dict_in_values(value)})
        elif type(converted_obj) is list:
            result = []
            for item in converted_obj:
                result.append(data.convert_dict_in_values(item))
        else:
            print(" You try convert unsupported data in value it may be error")
            result = converted_obj
        return result

    def load_components(self, input_dict: dict):
        for key, value in input_dict.items():
            if type(value) is list:
                value_list = []
                for item in value:
                    value_list.append(self.convert_dict_in_values(item))
                setattr(self, key, value_list)
            elif type(value) is dict:
                value_dict = dict()
                for key, item in value.items():
                    value_dict.update({key: self.convert_dict_in_values(item)})
                setattr(self, key, value_dict)
            else:
                setattr(self, key, value)



    @staticmethod
    def _load_json(file: pathlib.Path) -> Union[list, dict]:
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
        for name in self.short_save:
            if isinstance(name, str):
                if attr_name == name:
                    return True
        return False



    def createdir(self, directory=None):
        if bool(directory):
            self.directory.mkdir(parents=True, exist_ok=True)
        else:
            directory.mkdir(parents=True, exist_ok=True)


