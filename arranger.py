import json
import os
class Arranger:
    def __init__(self, jsonData=None, query=None):
        self.__modelPaths = []
        self.__jsonData = jsonData
        self.__query = query

    def arrangeModel(self, jsonData=None, query=None):
        if jsonData != None:
            self.__jsonData = jsonData
        if query != None:
            self.__query = query

        self.__modelPaths.append(*(self.__jsonData.values()))
        
        for path in self.__modelPaths:
            for dirpath, _, filenames in os.walk(".."):
                if path in filenames:
                    print(path)
                    workflowPath = os.path.join(dirpath, path)
                    with open(workflowPath, "r") as file:
                        data = json.load(file)

                        for key, value in data.items():
                            if key.isdigit(): 
                                value["data"].append(self.__query) 

                    with open(path, "w") as file:
                        json.dump(data, file, indent=2)


