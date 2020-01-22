from Source.IO import data
from pathlib import Path
import numpy as np


class ChBound(data):


    def __init__(self, lBound, rBound):

        self.components = []
        self.rBonds = rBound
        self.lBonds = lBound
        self.dont_save.append("parent")
        self.short_save.extend()
        self.save()

