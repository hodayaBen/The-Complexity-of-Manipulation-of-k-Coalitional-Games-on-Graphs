#!/usr/bin/env python3
# coding: utf-8
#main
import sys
sys.dont_write_bytecode = True
import math
import multiprocessing
import networkx as nx
import random
import time
sys.path.insert(1, './Base')

from Utils import Utils
from Graph import Graph
from GraphUtils import GraphUtils
from Statistics import Statistics
from ObjectiveNames import ObjectiveNames
from ManipulationProcessorReturnObject import ManipulationProcessorReturnObject
from ManipulationsProcessors import ManipulationsProcessors
from ManipulatorActions import ManipulatorActions
from AlgorithmsNames import AlgorithmsNames


visualiseGraphOnlyMode = False


# 
# Params block
# 

graphVisualizationEnabled = False

expParam_graphInputFileName = 'twitter_combined.txt'
# expParam_graphInputFileName = 'facebook_combined.txt'
expParam_maxNodesInGraph = 10
expParam_numOfFriends = 2
expParam_graphIndex = 1
expParam_randomSeed = -1

if (len(sys.argv) > 2):
    if ('twitter' == sys.argv[2]):
        expParam_graphInputFileName = 'twitter_combined.txt'
    else:
        expParam_graphInputFileName = 'facebook_combined.txt'

if (len(sys.argv) > 3):
    expParam_maxNodesInGraph = int(sys.argv[3])
    
if (len(sys.argv) > 4):
    expParam_numOfFriends = int(sys.argv[4])

if (len(sys.argv) > 5):
    expParam_graphIndex = int(sys.argv[5])
    
if (len(sys.argv) > 6):
    expParam_randomSeed = int(sys.argv[6])
    

if (expParam_randomSeed > 0):
    random.seed(expParam_randomSeed)


expParam_graphIsDirected = False

if ('twitter_combined.txt' == expParam_graphInputFileName):
    expParam_graphIsDirected = True

expParam_objectiveName = ObjectiveNames.MAX_UTIL



algorithmsToRunArr = [
        AlgorithmsNames.SOCIALLY,
        AlgorithmsNames.FPT, 
        AlgorithmsNames.BRUTE_FORCE,
    ]


expParam_singleAlgorithmToRun = ''

if (len(sys.argv) > 7):
    expParam_singleAlgorithmNameToRun = sys.argv[7]

    if ('brute_force' == expParam_singleAlgorithmNameToRun):
        algorithmsToRunArr = [AlgorithmsNames.BRUTE_FORCE]
        print('Running brute_force algorithm')

    if ('fpt' == expParam_singleAlgorithmNameToRun):
        algorithmsToRunArr = [AlgorithmsNames.FPT]
        print('Running fpt algorithm')

    if ('new_fpt3' == expParam_singleAlgorithmNameToRun):
        algorithmsToRunArr = [AlgorithmsNames.NEW_FPT3]
        print('Running fpt3 algorithm')

    if ('socially' == expParam_singleAlgorithmNameToRun):
        algorithmsToRunArr = [AlgorithmsNames.SOCIALLY]
        print('Running socially algorithm')

    
print(algorithmsToRunArr)



useOldCutAlgorithm = True

if (len(sys.argv) > 8):

    if ('randomAlgo' == sys.argv[8]):
        useOldCutAlgorithm = False

print('useOldCutAlgorithm: ' + str(useOldCutAlgorithm))



partitionsCount = 2

if (len(sys.argv) > 9):

    partitionsCount = int(sys.argv[9])

print('partitionsCount: ' + str(partitionsCount))





# 
# End of params block
# 


graphNX = GraphUtils.fetch_portion_of_graph(expParam_graphInputFileName, expParam_graphIsDirected, expParam_maxNodesInGraph, expParam_numOfFriends)
if not len(graphNX.nodes) == expParam_maxNodesInGraph:
    ddd


graphObj = Graph(isDirected = expParam_graphIsDirected, verbose = False, printErrors = True)
graphObj.loadFromOtherGraph(graphNX)



experimentUID = Utils.generateRandomString(20)

min_degrees = sorted(dict(graphNX.degree()).values())[:2]

if (expParam_graphIsDirected):

    if (useOldCutAlgorithm):
        mincuts = Utils.get_all_mincuts_d(graphNX, "all")
    else:
        mincuts = graphObj.getAllMinCuts(experimentUID, 'edges', False, partitionsCount)

else:
    if (useOldCutAlgorithm):
        mincuts = Utils.get_all_mincuts(graphNX, "all")
    else:
        mincuts = graphObj.getAllMinCuts(experimentUID, 'edges', False, partitionsCount)


if expParam_graphIsDirected:
    cut_nodes = set([tup[0] for cut in mincuts for tup in cut])
else:    
    cut_nodes = set([item for cut in mincuts for tup in cut for item in tup])

# Map the function to the list of nodes for parallel execution

inputs = []
for node in cut_nodes:
    inputs.append({'graphObj': graphNX, 'subjectNodeId': node, 'graphIsDirected': expParam_graphIsDirected})
    
random.shuffle(inputs)


# globalManipulationType = ManipulatorActions.REMOVE_EDGE_ONLY
globalManipulationType = ManipulatorActions.ADD_EDGE_ONLY



previuosTempGraphNx = None

additionalLogIdentifier = ''

if (len(sys.argv) > 1):
    additionalLogIdentifier = sys.argv[1]

stats = Statistics('results_10_' + additionalLogIdentifier)

filteredInputs = inputs

globalStartTime = time.time()

bf_result = False
fpt_result = False
last_nodes = []
last_edges = []
last_result = ""

for params in filteredInputs:

    subjectNodeId = params['subjectNodeId']

    
    if (visualiseGraphOnlyMode):
        
        graphObj.setNodeColor(subjectNodeId, 'red')

        graphObj.visualizeGraph('graphs/random_seed_'+str(expParam_randomSeed)+'_'+str(subjectNodeId)+'.png')
        
        continue

    
    for algorithmName in algorithmsToRunArr:
        was_exception = False
        
        foundManipulationType1Edges = []

        inputParams = {
                'graphInputFileName': expParam_graphInputFileName,
                'graphIsDirected': expParam_graphIsDirected,
                'numOfFriends': expParam_numOfFriends,
                'graphIndex': expParam_graphIndex,
                'expParam_randomSeed': expParam_randomSeed,
                'objectiveName': expParam_objectiveName,
                'algorithmName': algorithmName,
                'subjectNodeId': subjectNodeId,
                'mincutsCount': len(mincuts),
                'cutNodesCount': len(cut_nodes),
                'minDegrees': str(min_degrees).replace(', ', '|'),
            }

        stats.updateInputParams(inputParams)


        

        startTime = time.time()

        print('startTime')
        print(startTime)

        
        algorithmUID = Utils.generateRandomString(20)

        
        manipulationProcessorReturnObject = ManipulationProcessorReturnObject(experimentUID, algorithmUID, -1, -1, globalManipulationType)
        
        resultsStatsArr = manipulationProcessorReturnObject.prepareResultsLogDict()


        resultsStatsArr['experimentStage'] = 'start'
        resultsStatsArr['startTimestamp'] = startTime
        resultsStatsArr['finishTimestamp'] = 0
        resultsStatsArr['runTime'] = 0

        stats.output(subjectNodeId, graphObj, resultsStatsArr)



        
        manipulationProcessorReturnObject = ManipulationsProcessors.processManipulations(experimentUID, algorithmUID, algorithmName, params['graphObj'], graphObj, params['subjectNodeId'], params['graphIsDirected'], stats, globalManipulationType, useOldCutAlgorithm, partitionsCount)


        resultsStatsArr = manipulationProcessorReturnObject.prepareResultsLogDict()


        resultsStatsArr['startTimestamp'] = startTime
        resultsStatsArr['finishTimestamp'] = str(time.time())
        resultsStatsArr['runTime'] = (time.time() - startTime)

        
        stats.output(subjectNodeId, graphObj, resultsStatsArr)


        if (graphVisualizationEnabled):
            graphObj.setNodeColor(subjectNodeId, 'red')

            graphObj.visualizeGraph('graphs/'+str(expParam_graphIndex)+'_'+str(subjectNodeId)+'.png')
            

            if len(foundManipulationType1Edges) > 0:
                randomPostfix = random.randint(100000, 999999)

                subGraphObj = Graph(isDirected = expParam_graphIsDirected, verbose = False, printErrors = True)

                subGraphObj.loadFromOtherGraph(graphObj.getGraph())

                subGraphObj.setNodeColor(subjectNodeId, 'red')

                subGraphObj.visualizeGraph('graphs_examples/'+expParam_graphInputFileName+'/'+str(subjectNodeId)+'_'+str(randomPostfix)+'_before_manipulation.png')

                subGraphObj.addEdges(foundManipulationType1Edges)

                subGraphObj.visualizeGraph('graphs_examples/'+expParam_graphInputFileName+'/'+str(subjectNodeId)+'_'+str(randomPostfix)+'_after_manipulation.png')
            


print('Total run time:')
print(time.time() - globalStartTime)
print('----')
print('--end--')

