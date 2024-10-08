from parser import Parser
from actuator import Actuator

class KQPA:
    def __init__(self, query=None):
        self.__parser = Parser()
        self.__actuator = Actuator()
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
        self.__parser.findApplicableModels()
        response = self.__parser.getLLMJson()
        ## TODO: insert arranger file writing logic here
        self.__actuator.actuate(response)

kqpa = KQPA()
kqpa.setQuery("Give me a general report on the Headless Horseman using the RAG engine model.")
kqpa.runMain()

    