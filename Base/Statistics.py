import numpy as np
import os
import time

class Statistics:

    def __init__(self, outputFileName = 'results'):

        self.inputParams = {}

        self.resultsDirectory = "results/"

        self.filePath = self.resultsDirectory + outputFileName + '.csv'

        if not os.path.exists(self.resultsDirectory):
            os.makedirs(self.resultsDirectory)
            
    def changeFileName(self, name):
        self.filePath = self.resultsDirectory + name

    def resetFiles(self):

        pass


    def updateInputParams(self, inputParams):
        self.inputParams = inputParams

    def output(self, subjectNodeId, originalGraph, resultsArr, includeTitle = 'on_create', includeInputParams = True, writeMode = 'a+'):

        if ('on_create' == includeTitle):
            includeTitle = not os.path.isfile(self.filePath)

        resultsFile = open(self.filePath, writeMode)

        graphParams = originalGraph.getGraphParams(subjectNodeId)

        if (includeTitle):

            if (includeInputParams):
                for inputParamName in self.inputParams:
                    resultsFile.write(str(inputParamName) + ',')

            for graphParamName in graphParams:
                resultsFile.write(str(graphParamName) + ',')


            for resultName in resultsArr:
                resultsFile.write(str(resultName) + ',')
                
            resultsFile.write('\n')



        if (includeInputParams):
            for inputParamName in self.inputParams:
                resultsFile.write(str(self.inputParams[inputParamName]) + ',')

        for graphParamName in graphParams:
            resultsFile.write(str(graphParams[graphParamName]) + ',')



        for resultName in resultsArr:
            resultsFile.write(str(resultsArr[resultName]) + ',')

            
        resultsFile.write('\n')

        resultsFile.close()

