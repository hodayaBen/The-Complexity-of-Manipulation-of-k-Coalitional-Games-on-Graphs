# import networkx as nx
import itertools
import time

from Timeout import Timeout
from multiprocessing import TimeoutError
from Utils import Utils
from Graph import Graph
from AlgorithmsNames import AlgorithmsNames
from ManipulationOutcome import ManipulationOutcome
from ManipulatorActions import ManipulatorActions
from ManipulationProcessorReturnObject import ManipulationProcessorReturnObject

GLOBAL_TIMEOUT_SECONDS = 60 * 60
# GLOBAL_TIMEOUT_SECONDS = 5 * 60
# GLOBAL_TIMEOUT_SECONDS = 10

class ManipulationsProcessors:

    @staticmethod
    def processManipulations(experimentUID, algorithmUID, algorithmName, graphObj, customGraphObj, subjectNodeId, graphIsDirected, outputStats, manipulationActionType = ManipulatorActions.REMOVE_EDGE_ONLY, useOldCutAlgorithm = True, partitionsCount = 2):

        # 
        # Init
        # 
        csize = -1
        asize = -1
        # csize_ON_GC = -1
        # asize_ON_GC = -1

        foundManipulationOutcome1Edges = []
        foundManipulationOutcome2Edges = []
        foundManipulationOutcome3Edges = []
        foundManipulationOutcome4Edges = []
        foundManipulationOutcome1 = -1
        foundManipulationOutcome2 = -1
        foundManipulationOutcome3 = -1
        foundManipulationOutcome4 = -1
        allOptionsPassStartTime = -1
        count_manipulation_checked = 0


        # 
        # Prepare
        # 

        subjectNodeNeighbors = list(graphObj.neighbors(subjectNodeId))

        customGraphObjCopy = Graph(isDirected = graphIsDirected)
        customGraphObjCopy.loadFromOtherGraph(graphObj)

        if graphIsDirected:
            mn, mx, _ = Utils.cut_value_d(customGraphObjCopy, graphObj, subjectNodeId, subjectNodeNeighbors, useOldCutAlgorithm, partitionsCount)
        else:
            mn, mx, _ = Utils.cut_value(customGraphObjCopy, graphObj, subjectNodeId, subjectNodeNeighbors, useOldCutAlgorithm, partitionsCount)


        print(algorithmName)
        
        if (AlgorithmsNames.SOCIALLY == algorithmName):

            if graphIsDirected:
                # manipulation_sets, manipulation_sets_temp = itertools.tee(Utils.get_all_mincuts_d(graphObj, subjectNodeId))
                if (useOldCutAlgorithm):
                    manipulation_sets = (Utils.get_all_mincuts_d(graphObj, subjectNodeId))
                else:
                    manipulation_sets = customGraphObj.getAllMinCuts(experimentUID, 'edges', False, partitionsCount)
            else:
                # manipulation_sets, manipulation_sets_temp = itertools.tee(Utils.get_all_mincuts(graphObj, subjectNodeId))
                if (useOldCutAlgorithm):
                    manipulation_sets = (Utils.get_all_mincuts(graphObj, subjectNodeId))
                else:
                    manipulation_sets = customGraphObj.getAllMinCuts(experimentUID, 'edges', False, partitionsCount)


        elif (AlgorithmsNames.FPT == algorithmName or AlgorithmsNames.NEW_FPT3 == algorithmName):
            graphObjCopy = graphObj.copy()

            #add all edges from M 
            for nodeId in graphObj.nodes():
                if nodeId != subjectNodeId and (subjectNodeId, nodeId) not in graphObj.edges():
                    graphObjCopy.add_edge(subjectNodeId, nodeId)

            customGraphObjCopy = Graph(isDirected = customGraphObj.isDirected())
            customGraphObjCopy.loadFromOtherGraph(graphObjCopy)

            if graphIsDirected:

                if (useOldCutAlgorithm):
                    asize = Utils.get_cutsize_d(graphObjCopy, subjectNodeId)
                    csize = Utils.get_cutsize_d(graphObj, subjectNodeId)
                else:

                    minCut = customGraphObjCopy.getAllMinCuts(experimentUID, 'edges', True, partitionsCount)
                    asize = len(minCut)

                    minCut = customGraphObj.getAllMinCuts(experimentUID, 'edges', True, partitionsCount)
                    csize = len(minCut)
            else:

                if (useOldCutAlgorithm):
                    asize = Utils.get_cutsize(graphObjCopy, subjectNodeId)
                    csize = Utils.get_cutsize(graphObj, subjectNodeId)
                else:

                    minCut = customGraphObjCopy.getAllMinCuts(experimentUID, 'edges', True, partitionsCount)
                    asize = len(minCut)

                    minCut = customGraphObj.getAllMinCuts(experimentUID, 'edges', True, partitionsCount)
                    csize = len(minCut)



            if ManipulatorActions.REMOVE_EDGE_ONLY == manipulationActionType:
                # manipulation_sets, manipulation_sets_temp = itertools.tee(Utils.get_subsets_m_plus(graphObj.edges(), (2 * csize)))
                manipulation_sets = (Utils.get_subsets_m_plus(graphObj.edges(), (2 * csize), csize))
                
            elif ManipulatorActions.ADD_EDGE_ONLY == manipulationActionType:
                # manipulation_sets, manipulation_sets_temp = itertools.tee(Utils.get_subsets_m_plus(graphObj.edges(), asize))
                manipulation_sets = (Utils.get_subsets_m_plus(graphObj.edges(), asize, csize))
            else:
                not_implemented
                
                
        elif (AlgorithmsNames.BRUTE_FORCE == algorithmName):

            graphObjCopy = graphObj.copy()

            limit = -10
            
            if ManipulatorActions.REMOVE_EDGE_ONLY == manipulationActionType:
                limit = len(list(graphObj.edges(subjectNodeId))) - mn -1

            # manipulation_sets, manipulation_sets_temp = itertools.tee(Utils.get_set_all_manipulation(graphObjCopy, subjectNodeId, manipulationActionType, limit)) #1 - add,2-add, 3 - remove
            manipulation_sets = (Utils.get_set_all_manipulation(graphObjCopy, subjectNodeId, manipulationActionType, limit)) #1 - add,2-add, 3 - remove
            


        # 
        # Start
        # 


        output = ManipulationProcessorReturnObject(experimentUID, algorithmUID, mn, mx, manipulationActionType)

        output.setIsMidExperimentLog(True)

        try:
            with Timeout(seconds = GLOBAL_TIMEOUT_SECONDS):

                allOptionsPassStartTime = time.time()
                
                mna = mn
                mxa = mx
                mnb = mn
                mxb = mx
                mnc = mn
                mxc = mx
                mnd = mn
                mxd = mx

                counter    = 0
                counter_lb = 0
                counter_ub = 0
                counter_w  = 0
                counter_s  = 0

                searchTimeMiliseconds_lb = -1
                searchTimeMiliseconds_ub = -1
                searchTimeMiliseconds_w = -1
                searchTimeMiliseconds_s = -1

                shouldWriteMidExperimentStatistics = False

                len_of_manipulation_sets = 0

                for cutSet in manipulation_sets:

                    len_of_manipulation_sets += 1

                    # if (len_of_manipulation_sets > 40000000):
                    #     raise TimeoutError()
                    #     break


                    counter += 1

                    if (AlgorithmsNames.BRUTE_FORCE != algorithmName):
                        functionReturnValue = Utils.innerp(customGraphObj, graphObj, subjectNodeId, subjectNodeNeighbors, mn, cutSet, graphIsDirected, manipulationActionType, useOldCutAlgorithm, partitionsCount)

                        if functionReturnValue[0] != -2:
                            count_manipulation_checked += 1
                    else:
                        functionReturnValue = Utils.lb_ub_for_gm(customGraphObj, graphObj, subjectNodeId, subjectNodeNeighbors, cutSet, graphIsDirected, manipulationActionType, useOldCutAlgorithm, partitionsCount)

                            
                    if functionReturnValue[0] == -1:
                        continue
                        
                    if functionReturnValue[0] == -2:
                        continue


                    mn1 = functionReturnValue[0]
                    mx1 = functionReturnValue[1]

                    if mn1 > mna:
                        mna = mn1
                        mxa = mx1
                        foundManipulationOutcome1Edges = functionReturnValue[2]

                        foundManipulationOutcome1 = ManipulationOutcome.LB_IMPROVMENT #1
                        
                        if counter_lb == 0:
                            counter_lb = counter
                            searchTimeMiliseconds_lb = time.time() - allOptionsPassStartTime
                            shouldWriteMidExperimentStatistics = True


                                                    
                    if mx1 > mxb:
                        mnb = mn1
                        mxb = mx1
                        foundManipulationOutcome2Edges = functionReturnValue[2]

                        foundManipulationOutcome2 = ManipulationOutcome.UB_IMPROVMENT #2
                        
                        if counter_ub == 0:
                            counter_ub = counter 
                            searchTimeMiliseconds_ub = time.time() - allOptionsPassStartTime
                            shouldWriteMidExperimentStatistics = True
                        
                                                    
                    if (mn1 > mnc and mx1 > mxc):# or (mn1 >= mnc and mx1 > mxc):
                        mnc = mn1
                        mxc = mx1
                        foundManipulationOutcome3Edges = functionReturnValue[2]

                        foundManipulationOutcome3 = ManipulationOutcome.WEAK_IMPROVMENT #3
                        
                        if counter_w == 0:
                            counter_w = counter
                            searchTimeMiliseconds_w = time.time() - allOptionsPassStartTime
                            shouldWriteMidExperimentStatistics = True
                        

                    if (mn1 > mxd):
                        mnd = mn1
                        mxd = mx1
                        foundManipulationOutcome4Edges = functionReturnValue[2]

                        foundManipulationOutcome4 = ManipulationOutcome.STRICT_IMPROVMENT #4

                        if counter_s == 0:
                            counter_s = counter
                            searchTimeMiliseconds_s = time.time() - allOptionsPassStartTime
                            shouldWriteMidExperimentStatistics = True



                    if (shouldWriteMidExperimentStatistics):

                        if (AlgorithmsNames.BRUTE_FORCE == algorithmName):
                            count_manipulation_checked = len_of_manipulation_sets

                        output.update(
                                foundManipulationOutcome1Edges = foundManipulationOutcome1Edges,
                                foundManipulationOutcome2Edges = foundManipulationOutcome2Edges,
                                foundManipulationOutcome3Edges = foundManipulationOutcome3Edges,
                                foundManipulationOutcome4Edges = foundManipulationOutcome4Edges,
                                manipulationOutcome1 = foundManipulationOutcome1,
                                manipulationOutcome2 = foundManipulationOutcome2,
                                manipulationOutcome3 = foundManipulationOutcome3,
                                manipulationOutcome4 = foundManipulationOutcome4,
                                cutSetIndex = counter,
                                cutSetsCount = len_of_manipulation_sets,
                                OPT_LB_LB = mna,
                                OPT_LB_UB = mxa,
                                OPT_UB_LB = mnb,
                                OPT_UB_UB = mxb,
                                OPT_W_LB = mnc,
                                OPT_W_UB = mxc,
                                OPT_S_LB = mnd,
                                OPT_S_UB = mxd,
                                COUNTER_LB = counter_lb,
                                COUNTER_UB = counter_ub,
                                COUNTER_W = counter_w,
                                COUNTER_S = counter_s,
                                searchTimeMiliseconds_lb = searchTimeMiliseconds_lb,
                                searchTimeMiliseconds_ub = searchTimeMiliseconds_ub,
                                searchTimeMiliseconds_w = searchTimeMiliseconds_w,
                                searchTimeMiliseconds_s = searchTimeMiliseconds_s,
                                allOptionsPassRunTime = time.time() - allOptionsPassStartTime,
                                csize = csize,
                                asize = asize,
                                # csize_ON_GC = csize_ON_GC,
                                # asize_ON_GC = asize_ON_GC,
                                count_manipulation_checked = count_manipulation_checked,
                        )
                        
                        if (shouldWriteMidExperimentStatistics or counter < len_of_manipulation_sets):
                            resultsStatsArr = output.prepareResultsLogDict()

                            resultsStatsArr['startTimestamp'] = allOptionsPassStartTime
                            resultsStatsArr['finishTimestamp'] = str(time.time())
                            resultsStatsArr['runTime'] = (time.time() - allOptionsPassStartTime)

                            outputStats.output(subjectNodeId, customGraphObj, resultsStatsArr)

                        shouldWriteMidExperimentStatistics = False



            if (AlgorithmsNames.BRUTE_FORCE == algorithmName):
                count_manipulation_checked = len_of_manipulation_sets

            output.update(
                    foundManipulationOutcome1Edges = foundManipulationOutcome1Edges,
                    foundManipulationOutcome2Edges = foundManipulationOutcome2Edges,
                    foundManipulationOutcome3Edges = foundManipulationOutcome3Edges,
                    foundManipulationOutcome4Edges = foundManipulationOutcome4Edges,
                    manipulationOutcome1 = foundManipulationOutcome1,
                    manipulationOutcome2 = foundManipulationOutcome2,
                    manipulationOutcome3 = foundManipulationOutcome3,
                    manipulationOutcome4 = foundManipulationOutcome4,
                    cutSetIndex = counter,
                    cutSetsCount = len_of_manipulation_sets,
                    OPT_LB_LB = mna,
                    OPT_LB_UB = mxa,
                    OPT_UB_LB = mnb,
                    OPT_UB_UB = mxb,
                    OPT_W_LB = mnc,
                    OPT_W_UB = mxc,
                    OPT_S_LB = mnd,
                    OPT_S_UB = mxd,
                    COUNTER_LB = counter_lb,
                    COUNTER_UB = counter_ub,
                    COUNTER_W = counter_w,
                    COUNTER_S = counter_s,
                    searchTimeMiliseconds_lb = searchTimeMiliseconds_lb,
                    searchTimeMiliseconds_ub = searchTimeMiliseconds_ub,
                    searchTimeMiliseconds_w = searchTimeMiliseconds_w,
                    searchTimeMiliseconds_s = searchTimeMiliseconds_s,
                    allOptionsPassRunTime = time.time() - allOptionsPassStartTime,
                    csize = csize,
                    asize = asize,
                    # csize_ON_GC = csize_ON_GC,
                    # asize_ON_GC = asize_ON_GC,
                    count_manipulation_checked = count_manipulation_checked,
            )
            

            output.setIsMidExperimentLog(False)

            if mn < mna or mx < mxb:
                
                output.setManipulationFound(True)
                return output

            output.setManipulationFound(False)
            return output

        except TimeoutError:

            print('timeout occured - writing to the log')

            output.updateRunTime(allOptionsPassStartTime)

            # output.updateCountManipulationChecked(Utils.count_iter_items(manipulation_sets_temp))
            output.updateCountManipulationChecked(len_of_manipulation_sets)

            output.setIsMidExperimentLog(False)

            output.setTimeout(True)
            output.setManipulationFound(False)
            
            return output
        

        except Exception as e:
            print('in general exception')
            print(e)

