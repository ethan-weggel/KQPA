import os
import subprocess
import json
import re

class Parser:
    def __init__(self):
        '''
        init.json is the root file describing all sub workflows defined in KNIT
        '''

        self.__currentQuery = None

        self.__rootProjectDirectory = "../.."
        self.__targetFilename = "init.json"

        self.__initJSONPath = None
        self.__initJSONData = None
        self.__LLMJson = None

        self.findInitJSON()
        self.readInit()

    def getCurrentQuery(self):
        return self.__currentQuery
    
    def setCurrentQuery(self, query):
        self.__currentQuery = query

    def findInitJSON(self):
        for dirpath, _, filenames in os.walk(self.__rootProjectDirectory):
            if self.__targetFilename in filenames:
                self.__initJSONPath = os.path.join(dirpath, self.__targetFilename)
        return None

    def readInit(self):
        with open(self.__initJSONPath, 'r') as file:
            self.__initJSONData = json.load(file)
    
    def findApplicableModels(self):

        print("Finding applicable models for current query...")

        search_command = "You are a knowledgable classification assistant that is a part of a system called KATHERINE. Your job is to look at a target query, then iterate through \
                          json data. Read each description in the json data to see if the model is applicable to the current query. If the model's description suggests the model can be run on the query \
                          then add an entry to a json response for me. The key should be the model name, the value should be the path associated with the model. When finished, return \
                          to me the json object. As an example, if the target query is 'Good morning, can you give me a weather report and test the main interface.' then I expect \
                          {'model-#00000001': 'KNIT\\workflows\\models\\model1\\model-one-workflow-one.json', 'model-#00000002': 'KNIT\\workflows\\models\\model2\\model-two-workflow-two.json'}. \
                          Show me your thought process. Make sure you are adding the exact things you think should be in the json response. The description does NOT need to match the entire query to be included. Put your final json response as the very last thing you say every time. Here is the target query:"
        
        search_command += str(self.__currentQuery)
        search_command += '\n\n'
        search_command += str(self.__initJSONData)

        ollama_process = subprocess.Popen(['ollama', 'run', 'mistral-nemo'], 
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True,
                                encoding='utf-8', 
                                shell=False)
        
        ollama_process.stdin.write('\n\n')
        ollama_process.stdin.write(search_command)
        ollama_process.stdin.write('\n')
        ollama_process.stdin.flush()
        
        self.output, self.error = ollama_process.communicate()
        # print(self.output)

        ollama_process.stdin.close()
        ollama_process.stdout.close()
        ollama_process.stderr.close()
        ollama_process.terminate()

        output = self.extractJson()
        self.__LLMJson = output
       
    def extractJson(self):
        json_blobs = re.findall(r'\{.*?\}', self.output, re.DOTALL)
        return json_blobs[-1] if json_blobs else None
    
    def getLLMJson(self):
        return self.__LLMJson

