
import sys
import copy
sys.path.insert(1, '../Base')

from Constants import Constants
from ManipulatorActions import ManipulatorActions
from ObjectiveNames import ObjectiveNames

class Algorithm3():

    def __init__(self):

        # Some algorithm state params, if needed
        pass

    def run(self, graphObj, subjectNodeAllowedAction = None, expParam_objectiveName = None):

        mMinus_NodeId = graphObj.getSubjectNodeId()

        n1GroupOfMMinus = graphObj.getN1GroupOfNode(mMinus_NodeId)

        if (len(n1GroupOfMMinus) > 0):
            if (graphObj.isVerbose()):
                print('row 2')

            return [None]
            # debug:
            # return None, None, 0

        graphNodesList = graphObj.getNodesList()

        maxV = -1
        minV = len(graphNodesList) + 1
        maxA_NodeId = mMinus_NodeId

        allNeighborsOfMMinus = graphObj.getNodeNeighbors(mMinus_NodeId)

        for a_NodeId in allNeighborsOfMMinus:

            aOnlyNeighborsGroup = graphObj.getN1GroupOfNode(a_NodeId)

            Va_Group = aOnlyNeighborsGroup + graphObj.getN1GroupOfNodePair(a_NodeId, mMinus_NodeId)

            N_of_mMinus_and_Va = Utils.subtractLists(Va_Group, aOnlyNeighborsGroup)


            sizeOf_N_of_mMinus_and_Va = len(N_of_mMinus_and_Va)

            if (sizeOf_N_of_mMinus_and_Va >= maxV and len(Va_Group) < len(Utils.subtractLists(graphNodesList, [mMinus_NodeId, a_NodeId]))):
                maxV = sizeOf_N_of_mMinus_and_Va
                maxA_NodeId = a_NodeId
            
            if (minV >= sizeOf_N_of_mMinus_and_Va):
                minV = sizeOf_N_of_mMinus_and_Va
        
        if (minV == maxV):
            return [None]
        

        output = []
        
        allNeighborsOfMMinusExceptMaxA = Utils.subtractLists(allNeighborsOfMMinus, [maxA_NodeId])

        for a in allNeighborsOfMMinusExceptMaxA:
            output.append((mMinus_NodeId, a))

        return output