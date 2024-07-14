
import sys
from functools import partial

sys.path.insert(1, '../Base')

from Constants import Constants
from ManipulatorActions import ManipulatorActions
from ObjectiveNames import ObjectiveNames

class BasicEstimator():

    @staticmethod
    def rank(realGraph, newGraph, expParam_objectiveName, nodeId = Constants.SUBJECT_NODE_ID):
        graphRank = 0.0
        
        if (expParam_objectiveName == ObjectiveNames.MAX_UTIL):
            val,partiotion= newGraph.calculateWorstMinCut()
            if(Constants.SUBJECT_NODE_ID in partiotion[0]):
                par=partiotion[0]
            else:
                par= partiotion[1]
            for v in par:
                if(realGraph.isEdgeExists(Constants.SUBJECT_NODE_ID,v) or (not realGraph.isDirected() and realGraph.isEdgeExists(v, Constants.SUBJECT_NODE_ID))):
                    graphRank += 1

        
        if (expParam_objectiveName == ObjectiveNames.MAX_EGAL):
            # Do something...
            graphRank += 0.2 * realGraph.getNodesCount() * len(realGraph.getEdgesList())

        
        if (expParam_objectiveName == ObjectiveNames.AT_LEAST1):
            # Do something...
            graphRank -= 0.3 * realGraph.getNodesCount() * len(realGraph.getEdgesList())
            

        return graphRank

    @staticmethod
    def pairedRank(graphBefore, graphAfter, expParam_objectiveName, nodeId = Constants.SUBJECT_NODE_ID):
        graphBeforeRank = BasicEstimator.rank(graphBefore, graphBefore, expParam_objectiveName, nodeId)
        graphAfterRank = BasicEstimator.rank(graphBefore, graphAfter, expParam_objectiveName, nodeId)
        return [graphBeforeRank, graphAfterRank, graphAfterRank - graphBeforeRank]
