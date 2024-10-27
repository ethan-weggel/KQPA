from parser import Parser
from actuator import Actuator
from arranger import Arranger
import sys

class KQPA:
    def __init__(self, query=None):
        self.__parser = Parser()
        self.__actuator = Actuator()
        self.__arranger = Arranger()
        self.__query = query

    def getQuery(self):
        return self.__query
    
    def setQuery(self, query):
        self.__query = query

    def reset(self, path=None, args=None, query=None):
        self.__actuator.resetActuator(path=path, args=args, query=query)

    def getModels(self):
        return self.__parser.getLLMJson()
    
    def parse(self, query):
        self.__parser.setCurrentQuery(query)
        self.__parser.findApplicableModels()

    def actuate(self):
        self.__actuator.actuate(self.__parser.getLLMJson())

    def runMain(self, query=""):
        if query == "":
            query = self.__query
        self.__parser.setCurrentQuery(query)
        print("Query set.")
        self.__parser.findApplicableModels()
        print("Models found and returned.")
        response = self.__parser.getLLMJson()
        print(response)
        print("Models parsed.")
        self.__arranger.arrangeModel(response, query)
        print("Model arranged.")
        self.__actuator.actuate(response)


def main(args):
    kqpa = KQPA()
    kqpa.runMain(' '.join(args[1:]))

if __name__ == "__main__":
    main(sys.argv)

    