import sys
import os

horsemanPath = os.path.dirname("C:\\Users\\Ethan\\Documents\\Katherine\\Katherine-Node-Interfacing-Tool\\KNIT\\app\\modules\\Knit_HEADLESS.py")
readerPath = os.path.dirname("C:\\Users\\Ethan\\Documents\\Katherine\\Katherine-Node-Interfacing-Tool\\KNIT\\app\\modules\\reader.py")
modelPath = os.path.dirname("C:\\Users\\Ethan\\Documents\\Katherine\\Katherine-Node-Interfacing-Tool\\KNIT\\app\\modules\\model.py")
dirPath = os.path.dirname("C:\\Users\\Ethan\\Documents\\Katherine\\Katherine-Node-Interfacing-Tool\\KNIT\\app\\modules\\")
sys.path.insert(0, horsemanPath)
sys.path.insert(0, readerPath)
sys.path.insert(0, modelPath)
sys.path.insert(0, dirPath)

import reader as rd # type: ignore
import model as md # type: ignore
import Knit_HEADLESS as hh # type: ignore

class Actuator:
    def __init__(self, path=None, args=None, query=None):
        self.__executablePath = path
        self.__args = args
        self.__query = query

        self.__headlessHorseman = None

    def actuate(self, parsedDict):
        for value in parsedDict.values():
            reader = rd.Reader(value)
            reader.readModel()
            model = md.Model(reader)
            model.loadZipFunctions()
            self.__horseman = hh.HeadlessHorseman(model)
            self.__horseman.run()

    def resetActuator(self, path=None, args=None, query=None):
        self.__executablePath = path
        self.__args = args
        self.__query = query


# act = Actuator()
# act.actuate({})
