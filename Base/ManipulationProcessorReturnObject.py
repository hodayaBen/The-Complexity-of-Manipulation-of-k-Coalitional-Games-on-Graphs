import time

class ManipulationProcessorReturnObject():

    def __init__(self, experimentUID, algorithmUID, LB, UB, manipulationActionType):

        self.experimentUID = experimentUID
        self.algorithmUID = algorithmUID

        self.LB = LB
        self.UB = UB
        self.manipulationActionType = manipulationActionType
        self.timeout = False
        self.manipulationFound = False
        self.isMidExperimentLog = True


        self.foundManipulationOutcome1Edges = []
        self.foundManipulationOutcome2Edges = []
        self.foundManipulationOutcome3Edges = []
        self.foundManipulationOutcome4Edges = []
        self.manipulationOutcome1 = '-1'
        self.manipulationOutcome2 = '-1'
        self.manipulationOutcome3 = '-1'
        self.manipulationOutcome4 = '-1'
        self.cutSetIndex = 0
        self.cutSetsCount = 0
        self.OPT_LB_LB = -1
        self.OPT_LB_UB = -1
        self.OPT_UB_LB = -1
        self.OPT_UB_UB = -1
        self.OPT_W_LB = -1
        self.OPT_W_UB = -1
        self.OPT_S_LB = -1
        self.OPT_S_UB = -1
        self.COUNTER_LB = -1
        self.COUNTER_UB = -1
        self.COUNTER_W = -1
        self.COUNTER_S = -1
        self.SEARCHTIMEMILISECONDS_LB = -1
        self.SEARCHTIMEMILISECONDS_UB = -1
        self.SEARCHTIMEMILISECONDS_W = -1
        self.SEARCHTIMEMILISECONDS_S = -1
        self.allOptionsPassRunTime = -1
        self.csize = -1
        self.asize = -1
        # self.csize_ON_GC = -1
        # self.asize_ON_GC = -1
        self.count_manipulation_checked = 0

    def update(self,
            foundManipulationOutcome1Edges,
            foundManipulationOutcome2Edges,
            foundManipulationOutcome3Edges,
            foundManipulationOutcome4Edges,
            manipulationOutcome1,
            manipulationOutcome2,
            manipulationOutcome3,
            manipulationOutcome4,
            cutSetIndex,
            cutSetsCount,
            OPT_LB_LB,
            OPT_LB_UB,
            OPT_UB_LB,
            OPT_UB_UB,
            OPT_W_LB,
            OPT_W_UB,
            OPT_S_LB,
            OPT_S_UB,
            COUNTER_LB,
            COUNTER_UB,
            COUNTER_W,
            COUNTER_S,
            searchTimeMiliseconds_lb,
            searchTimeMiliseconds_ub,
            searchTimeMiliseconds_w,
            searchTimeMiliseconds_s,
            allOptionsPassRunTime,
            csize,
            asize,
            # csize_ON_GC,
            # asize_ON_GC,
            count_manipulation_checked):

        self.foundManipulationOutcome1Edges = foundManipulationOutcome1Edges
        self.foundManipulationOutcome2Edges = foundManipulationOutcome2Edges
        self.foundManipulationOutcome3Edges = foundManipulationOutcome3Edges
        self.foundManipulationOutcome4Edges = foundManipulationOutcome4Edges
        self.manipulationOutcome1 = manipulationOutcome1
        self.manipulationOutcome2 = manipulationOutcome2
        self.manipulationOutcome3 = manipulationOutcome3
        self.manipulationOutcome4 = manipulationOutcome4
        self.cutSetIndex = cutSetIndex
        self.cutSetsCount = cutSetsCount
        self.OPT_LB_LB = OPT_LB_LB
        self.OPT_LB_UB = OPT_LB_UB
        self.OPT_UB_LB = OPT_UB_LB
        self.OPT_UB_UB = OPT_UB_UB
        self.OPT_W_LB = OPT_W_LB
        self.OPT_W_UB = OPT_W_UB
        self.OPT_S_LB = OPT_S_LB
        self.OPT_S_UB = OPT_S_UB
        self.COUNTER_LB = COUNTER_LB
        self.COUNTER_UB = COUNTER_UB
        self.COUNTER_W = COUNTER_W
        self.COUNTER_S = COUNTER_S
        self.SEARCHTIMEMILISECONDS_LB = searchTimeMiliseconds_lb
        self.SEARCHTIMEMILISECONDS_UB = searchTimeMiliseconds_ub
        self.SEARCHTIMEMILISECONDS_W = searchTimeMiliseconds_w
        self.SEARCHTIMEMILISECONDS_S = searchTimeMiliseconds_s
        self.allOptionsPassRunTime = allOptionsPassRunTime
        self.csize = csize
        self.asize = asize
        # self.csize_ON_GC = csize_ON_GC
        # self.asize_ON_GC = asize_ON_GC
        self.count_manipulation_checked = count_manipulation_checked


    def updateExperimentUID(self, experimentUID):
        self.experimentUID = experimentUID

    def updateAlgorithmUID(self, algorithmUID):
        self.algorithmUID = algorithmUID

    def updateRunTime(self, startRunTime):
        self.allOptionsPassRunTime = time.time() - startRunTime

    def setTimeout(self, timeout = True):
        self.timeout = timeout

    def isTimedOut(self):
        return self.timeout

    def setManipulationFound(self, manipulationFound = True):
        self.manipulationFound = manipulationFound

    def isManipulationFound(self):
        return self.manipulationFound

    def setIsMidExperimentLog(self, isMidExperimentLog = True):
        self.isMidExperimentLog = isMidExperimentLog

    def updateCountManipulationChecked(self, count_manipulation_checked):
        self.count_manipulation_checked = count_manipulation_checked


    def prepareResultsLogDict(self, printAllEvenWhenManipulationWasNotFound = False):
        
        resultsStatsArr = {}

        resultsStatsArr['experimentStage'] = '-'

        resultsStatsArr['experimentUID'] = self.experimentUID
        resultsStatsArr['algorithmUID'] = self.algorithmUID

        resultsStatsArr['LB'] = self.LB
        resultsStatsArr['UB'] = self.UB
        resultsStatsArr['manipulationActionType'] = self.manipulationActionType

        resultsStatsArr['manipulationFound'] = 0
        resultsStatsArr['foundManipulationOutcome1EdgesCount'] = '-'
        resultsStatsArr['foundManipulationOutcome1Edges'] = '-'
        resultsStatsArr['foundManipulationOutcome2EdgesCount'] = '-'
        resultsStatsArr['foundManipulationOutcome2Edges'] = '-'
        resultsStatsArr['foundManipulationOutcome3EdgesCount'] = '-'
        resultsStatsArr['foundManipulationOutcome3Edges'] = '-'
        resultsStatsArr['foundManipulationOutcome4EdgesCount'] = '-'
        resultsStatsArr['foundManipulationOutcome4Edges'] = '-'
        resultsStatsArr['manipulationOutcome1'] = -1
        resultsStatsArr['manipulationOutcome2'] = -1
        resultsStatsArr['manipulationOutcome3'] = -1
        resultsStatsArr['manipulationOutcome4'] = -1
        resultsStatsArr['OPT_LB_LB'] = -1
        resultsStatsArr['OPT_LB_UB'] = -1
        resultsStatsArr['OPT_UB_LB'] = -1
        resultsStatsArr['OPT_UB_UB'] = -1
        resultsStatsArr['OPT_W_LB'] = -1
        resultsStatsArr['OPT_W_UB'] = -1
        resultsStatsArr['OPT_S_LB'] = -1
        resultsStatsArr['OPT_S_UB'] = -1
        resultsStatsArr['COUNTER_LB'] = -1
        resultsStatsArr['COUNTER_UB'] = -1
        resultsStatsArr['COUNTER_W'] = -1
        resultsStatsArr['COUNTER_S'] = -1
        resultsStatsArr['SEARCHTIMEMILISECONDS_LB'] = -1
        resultsStatsArr['SEARCHTIMEMILISECONDS_UB'] = -1
        resultsStatsArr['SEARCHTIMEMILISECONDS_W'] = -1
        resultsStatsArr['SEARCHTIMEMILISECONDS_S'] = -1

        resultsStatsArr['csize'] = self.csize
        resultsStatsArr['asize'] = self.asize
        # resultsStatsArr['csize_ON_GC'] = self.csize_ON_GC
        # resultsStatsArr['asize_ON_GC'] = self.asize_ON_GC
        resultsStatsArr['cutSetIndex'] = self.cutSetIndex
        resultsStatsArr['cutSetsCount'] = self.cutSetsCount
        resultsStatsArr['count_manipulation_checked'] = self.count_manipulation_checked
        resultsStatsArr['allOptionsPassRunTime'] = self.allOptionsPassRunTime
        resultsStatsArr['timedOut'] = 0

        if (self.isTimedOut()):
            resultsStatsArr['timedOut'] = 1


        resultsStatsArr['experimentStage'] = 'middle' if self.isMidExperimentLog else 'end'

        if (not self.isTimedOut() and (printAllEvenWhenManipulationWasNotFound or self.isManipulationFound())):

            resultsStatsArr['manipulationFound'] = 1 if self.manipulationFound else 0
            # resultsStatsArr['manipulationOutcome'] = self.manipulationOutcome

            resultsStatsArr['foundManipulationOutcome1EdgesCount'] = len(self.foundManipulationOutcome1Edges)
            resultsStatsArr['foundManipulationOutcome1Edges'] = str(self.foundManipulationOutcome1Edges).replace('),)', '))').replace('), (', ')(').replace(', ', '-')
            resultsStatsArr['manipulationOutcome1'] = self.manipulationOutcome1

            resultsStatsArr['foundManipulationOutcome2EdgesCount'] = len(self.foundManipulationOutcome2Edges)
            resultsStatsArr['foundManipulationOutcome2Edges'] = str(self.foundManipulationOutcome2Edges).replace('),)', '))').replace('), (', ')(').replace(', ', '-')
            resultsStatsArr['manipulationOutcome2'] = self.manipulationOutcome2

            resultsStatsArr['foundManipulationOutcome3EdgesCount'] = len(self.foundManipulationOutcome3Edges)
            resultsStatsArr['foundManipulationOutcome3Edges'] = str(self.foundManipulationOutcome3Edges).replace('),)', '))').replace('), (', ')(').replace(', ', '-')
            resultsStatsArr['manipulationOutcome3'] = self.manipulationOutcome3

            resultsStatsArr['foundManipulationOutcome4EdgesCount'] = len(self.foundManipulationOutcome4Edges)
            resultsStatsArr['foundManipulationOutcome4Edges'] = str(self.foundManipulationOutcome4Edges).replace('),)', '))').replace('), (', ')(').replace(', ', '-')
            resultsStatsArr['manipulationOutcome4'] = self.manipulationOutcome4

            resultsStatsArr['OPT_LB_LB'] = self.OPT_LB_LB
            resultsStatsArr['OPT_LB_UB'] = self.OPT_LB_UB
            resultsStatsArr['OPT_UB_LB'] = self.OPT_UB_LB
            resultsStatsArr['OPT_UB_UB'] = self.OPT_UB_UB
            # resultsStatsArr['OPT_LB_S']  = self.OPT_LB_S
            # resultsStatsArr['OPT_UB_S']  = self.OPT_UB_S
            resultsStatsArr['OPT_W_LB'] = self.OPT_W_LB
            resultsStatsArr['OPT_W_UB'] = self.OPT_W_UB
            resultsStatsArr['OPT_S_LB'] = self.OPT_S_LB
            resultsStatsArr['OPT_S_UB'] = self.OPT_S_UB

            resultsStatsArr['COUNTER_LB'] = self.COUNTER_LB
            resultsStatsArr['COUNTER_UB'] = self.COUNTER_UB
            resultsStatsArr['COUNTER_W'] = self.COUNTER_W
            resultsStatsArr['COUNTER_S'] = self.COUNTER_S
            resultsStatsArr['SEARCHTIMEMILISECONDS_LB'] = self.SEARCHTIMEMILISECONDS_LB
            resultsStatsArr['SEARCHTIMEMILISECONDS_UB'] = self.SEARCHTIMEMILISECONDS_UB
            resultsStatsArr['SEARCHTIMEMILISECONDS_W'] = self.SEARCHTIMEMILISECONDS_W
            resultsStatsArr['SEARCHTIMEMILISECONDS_S'] = self.SEARCHTIMEMILISECONDS_S

        return resultsStatsArr

    def __str__(self):
        return '%s' % self.name