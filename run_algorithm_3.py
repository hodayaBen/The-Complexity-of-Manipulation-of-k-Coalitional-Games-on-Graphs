#!/usr/bin/env python3
# coding: utf-8
import sys
sys.dont_write_bytecode = True
import subprocess
import time
import random
import copy
sys.path.insert(1, './Base')

from Constants import Constants
from Statistics import Statistics
from Utils import Utils
from Graph import Graph
from AlgorithmNames import AlgorithmNames
from ManipulatorActions import ManipulatorActions
from ObjectiveNames import ObjectiveNames

sys.path.insert(1, './Algorithms')


from Algorithm3 import Algorithm3

# from HuristicNotHarm import HuristicNotHarm
# from HuristicHarm import HuristicHarm
# from ManipulationHarm import ManipulationHarm
# from ManipulationNotHarm import ManipulationNotHarm
sys.path.insert(1, './Estimators')

from BasicEstimator import BasicEstimator


def __main__():

    graphObj = Graph(isDirected = False, verbose = False, printErrors = True)

    if (sys.argv[1] == 'twitter'):
        graphObj.loadGraphFromFile('./datasets/twitter_combined.txt')
    else:
        graphObj.loadGraphFromFile('./datasets/facebook_combined.txt')

    graphNodesList = list(graphObj.getNodesList())

    # print('runTime' + ',' + 'mNeighborsCount' + ',' + 'minV' + ',' + 'maxV')
    startTime = time.time()
    
    # while True:
    # # for nodeId in cut_nodes:
    #     mMinus_NodeId = random.choice(graphNodesList)

    outFile = open('results/algo3_whole_pass_facebook.csv', 'w+')

    algorithm3 = new Algorithm3()

    index = 0
    wholeLength = len(graphNodesList)
    for mMinus_NodeId in graphNodesList:

        index += 1
        print('processing node ' + str(index) + ' out of ' + str(wholeLength) + ' ; nodeId: ' + str(mMinus_NodeId))
        

        graphObj.setSubjectNodeId(mMinus_NodeId)


        result = algorithm3.run(graphObj)

        if (result[0] == None):
            continue
        
        if False:
            subGraphObj = Graph(isDirected = False, verbose = False, printErrors = True)

            subGraphObj.loadFromOtherGraph(graphObj.getSubGraphFromNodes(Utils.edgesToUniqueNodesList(result)))

            subGraphObj.setNodeColor(mMinus_NodeId, 'red')

            subGraphObj.visualizeGraph('before_manipulation.png')

            subGraphObj.removeEdges(result)

            subGraphObj.visualizeGraph('after_manipulation.png')
        
        runTime = time.time() - startTime

        outFile.write(str(runTime) + ',' + str(result[0]) + ',' + str(result[1]) + ',' + str(result[2]) + "\n")

        startTime = time.time()


    outFile.close()

__main__()