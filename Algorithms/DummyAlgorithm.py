
import sys
import copy
sys.path.insert(1, '../Base')

from Constants import Constants
from ManipulatorActions import ManipulatorActions
from ObjectiveNames import ObjectiveNames

class DummyAlgorithm():

    def __init__(self):

        # Some algorithm state params, if needed
        pass

    def run(self, graph, subjectNodeAllowedAction, expParam_objectiveName):

        copyOfGraph = copy.deepcopy(graph)

        if (subjectNodeAllowedAction == ManipulatorActions.ADD_EDGE_ONLY):
            
            if (expParam_objectiveName == ObjectiveNames.MAX_UTIL):
                # Do something...
                pass

            copyOfGraph.addEdge(Constants.SUBJECT_NODE_ID, 3)

        if (subjectNodeAllowedAction == ManipulatorActions.REMOVE_EDGE_ONLY):
            
            if (expParam_objectiveName == ObjectiveNames.MAX_UTIL):
                # Do something...
                pass

            copyOfGraph.removeEdge(Constants.SUBJECT_NODE_ID, 1)
            
        if (subjectNodeAllowedAction == ManipulatorActions.ADD_OR_REMOVE_EDGE):

            if (expParam_objectiveName == ObjectiveNames.MAX_UTIL):
                # Do something...
                pass

            copyOfGraph.addEdge(Constants.SUBJECT_NODE_ID, 3)
            copyOfGraph.removeEdge(Constants.SUBJECT_NODE_ID, 1)

        return copyOfGraph