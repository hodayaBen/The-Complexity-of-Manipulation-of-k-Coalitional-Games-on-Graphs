import matplotlib.pyplot as plt
import random
import string
import itertools
# You also have to explicitly import the function for
# building the auxiliary digraph from the connectivity package
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from itertools import combinations, groupby
import networkx as nx
import sys
import subprocess
import copy
from Constants import Constants
from ObjectiveNames import ObjectiveNames
from Utils import Utils
sys.path.insert(1, './Estimators')
from BasicEstimator import BasicEstimator
from networkx.algorithms.connectivity import minimum_st_edge_cut

class Graph:

    def __init__(self, otherGraph = None, isSmallWorldNetwork = False, isDirected = True, nodesCount = 0, verbose = False, printErrors = False, isSNAP= False, isRandomGraph = False):

        self.graph_ = otherGraph

        self.subjectNodeId_ = None


        self.graphGroupedNodes_ = {}

        if (otherGraph != None):
            self.graphGroupedNodes_ = otherGraph.getGroupedNodes()


        self.nodesCount_ = nodesCount

        if (otherGraph != None):
            self.nodesCount_ = otherGraph.getNodesCount()


        self.isSmallWorldNetwork_ = isSmallWorldNetwork
        self.isSNAP_ = isSNAP
        self.isRandomGraph_ = isRandomGraph

        if (otherGraph != None):
            self.isSmallWorldNetwork_ = otherGraph.isSmallWorldNetwork()
            self.isSNAP_ = otherGraph.isSNAP()
            self.isRandomGraph_ = otherGraph.isRandomGraph()
        self.isDirected_ = isDirected

        if (otherGraph != None):
            self.isDirected_ = otherGraph.isDirected()


        self.verbose_ = verbose
        self.printErrors_ = printErrors

    def isVerbose(self):
        return self.verbose_

    def getSubGraphFromNodes(self, nodesList):
        return self.graph_.subgraph(nodesList)

    def setSubjectNodeId(self, subjectNodeId):
        self.subjectNodeId_ = subjectNodeId

    def getSubjectNodeId(self, nodesList):
        return self.subjectNodeId_

    def getEnlargedSubGraphFromNodes(self, nodesList):

        enlargedNodesSet = set()

        for nodeId in nodesList:
            enlargedNodesSet.add(nodeId)

            for nodeNeighborId in self.getNodeNeighbors(nodeId):
                enlargedNodesSet.add(nodeNeighborId)

        return self.graph_.subgraph(list(enlargedNodesSet))

    # def saveToFile(self, fileName):
    #     file1 = open(fileName, "w")
    #     file1.write(str(self.getNodesCount()))
    #     file1.write(" ")
    #     file1.write(str(len(self.getEdgesList())))
    #     #file1.write("\n")

    #     for v in sorted(self.getNodesList()):
    #         file1.write("\n")
    #         space = False
    #         for (u1, v1) in self.getEdgesFromNode(v):
    #             if space:
    #                 file1.write(' ')
    #             else:
    #                 space=True
    #             if u1 == v:
    #                 file1.write(str(int(v1)+1))
    #             else:
    #                 file1.write(str(int(u1)+1))

    #     file1.close()

    #     with open(fileName, 'r') as f:
    #         data = f.read()
    #         with open(fileName, 'w') as w:
    #             w.write(data[:-1])



    def getGraph(self):
        return self.graph_

    def getNodesCount(self):
        return self.nodesCount_

    def isSmallWorldNetwork(self):
        return self.isSmallWorldNetwork_

    def isSNAP(self):
        return self.isSNAP_

    def isRandomGraph(self):
        return self.isRandomGraph_

    def isDirected(self):
        return self.isDirected_

    def getGroupedNodes(self):
        return self.graphGroupedNodes_

    # 
    # Graph api methods:
    # 

    def isNodeExists(self, nodeId):
        return nodeId in self.graph_.nodes()


    def isEdgeExists(self, fromNodeId, toNodeId):
        if (self.isDirected_):
            return (fromNodeId, toNodeId) in self.graph_.edges()
        else:
            return (fromNodeId, toNodeId) in self.graph_.edges() or (toNodeId, fromNodeId) in self.graph_.edges()


    def getNodesList(self, includeData = False):
        return self.graph_.nodes(data = includeData)

    def getEdgesList(self, includeData = False):
        return self.graph_.edges(data = includeData)

    def getNodeDegree(self, nodeId):
        return len(self.getEdgesFromNode(nodeId))

    def getEdgesFromNode(self, nodeId):

        if (self.isDirected_):

            for innerNodeId, innerNodeEdges in groupby(self.graph_.edges(), key=lambda x: x[0]):
                if (nodeId == innerNodeId):
                    return list(innerNodeEdges)
        else:
            allEdgesOfNode = set()

            for innerNodeId, innerNodeEdges in groupby(self.graph_.edges(), key=lambda x: x[0]):
                if (nodeId == innerNodeId):
                    innerNodeEdgesList = list(innerNodeEdges)
                    allEdgesOfNode.update(innerNodeEdgesList)

            for innerNodeId, innerNodeEdges in groupby(self.graph_.edges(), key=lambda x: x[1]):
                if (nodeId == innerNodeId):
                    innerNodeEdgesList = Graph.reverseEdges(list(innerNodeEdges))
                    allEdgesOfNode.update(innerNodeEdgesList)
            
            return list(allEdgesOfNode)

        return []

    def getEdgesToNode(self, nodeId):

        if (self.isDirected_):

            allEdgesOfNode = set()
            
            for innerNodeId, innerNodeEdges in groupby(self.graph_.edges(), key=lambda x: x[1]):
                if (nodeId == innerNodeId):
                    innerNodeEdgesList = list(innerNodeEdges)
                    allEdgesOfNode.update(innerNodeEdgesList)

            return list(allEdgesOfNode)
        else:

            return self.getEdgesFromNode(nodeId)


    def addNode(self, nodeId, nodeColor = 1):
        
        if (None == self.graph_):

            if (self.printErrors_):
                print('Error: Trying to add node to non-existing graph')
                
            return False
        
        if (self.verbose_):
            print('Adding node ' + str(nodeId) + ' to graph')


        if (self.isNodeExists(nodeId)):

            if (self.verbose_):
                print('Node ' + str(nodeId) + ' already exists')

            return False

        self.nodesCount_+=1
        self.graph_.add_node(nodeId, color = nodeColor)

        return True


    def removeNode(self, nodeId):
        
        if (None == self.graph_):

            if (self.printErrors_):
                print('Error: Trying to remove node from non-existing graph')
                
            return False
        
        if (self.verbose_):
            print('Removing node ' + str(nodeId) + ' from graph')


        if (not self.isNodeExists(nodeId)):

            if (self.verbose_):
                print('Node ' + str(nodeId) + ' does not exists')

            return False


        self.graph_.remove_node(nodeId)

        return True


    def addEdge(self, fromNodeId, toNodeId, edgeWeight = 1.0, edgeColor = 'green'):
        
        if (None == self.graph_):

            if (self.printErrors_):
                print('Error: Trying to add edge to non-existing graph')
                
            return False
        
        if (self.verbose_):
            print('Adding edge ' + str((fromNodeId, toNodeId)) + ' to graph. Edge weight: ' + str(edgeWeight))


        if (self.isEdgeExists(fromNodeId, toNodeId)):

            if (self.verbose_):
                print('Edge ' + str((fromNodeId, toNodeId)) + ' already exists')

            return False


        if (not self.isNodeExists(fromNodeId)):
            self.addNode(fromNodeId, 'lightblue')

            if (self.verbose_):
                print('Creating node on new edge request: New node id: ' + str(fromNodeId))
        if (not self.isNodeExists(toNodeId)):
            self.addNode(toNodeId, 'lightblue')

            if (self.verbose_):
                print('Creating node on new edge request: New node id: ' + str(toNodeId))

        self.graph_.add_edge(fromNodeId, toNodeId, weight=edgeWeight, color=edgeColor)

        return True


    def addEdges(self, edgesList):

        for edge in edgesList:
            self.addEdge(edge[0], edge[1])

    def removeEdges(self, edgesList):

        for edge in edgesList:
            self.removeEdge(edge[0], edge[1])

    def removeEdge(self, fromNodeId, toNodeId):
        
        if (None == self.graph_):

            if (self.printErrors_):
                print('Error: Trying to remove edge from non-existing graph')
                
            return False
        
        if (self.verbose_):
            print('Removing edge ' + str((fromNodeId, toNodeId)) + ' from graph')


        if (not self.isEdgeExists(fromNodeId, toNodeId)):

            if (self.verbose_):
                print('Edge ' + str((fromNodeId, toNodeId)) + ' does not exist')

            return False

        self.graph_.remove_edge(fromNodeId, toNodeId)

        return True

    def getConnectedComponents(self):
        return nx.connected_components(self.graph_)


    def printGraph(self, destinationPath):

        with open(destinationPath, "a+") as f:

            print('----', file=f)
            print(self.graph_, file=f)
            print('Nodes:', file=f)
            print(self.graph_.nodes(), file=f)

            print('--', file=f)
            print('Edges:', file=f)

            if (len(self.graph_.edges()) == 0):
                print('None', file=f)

            for innerNodeId, innerNodeEdges in groupby(self.graph_.edges(), key=lambda x: x[0]):
                
                print(str(innerNodeId) + ' : ' + str(list(innerNodeEdges)), file=f)
            print('----', file=f)

    def getGraphParams(self, subjectNodeId):

        paramsArr = {}

        paramsArr['nodesCount'] = len(self.graph_.nodes())
        paramsArr['edgesCount'] = len(self.graph_.edges())
        edgesFromSubjectNode = self.getEdgesFromNode(subjectNodeId)
        
        # paramsArr['edgesCountFromM'] = len(edgesFromSubjectNode)
        paramsArr['edgesCountFromM'] = self.getNodeNeighborsCount(subjectNodeId)
        # paramsArr['groupsCount'] = len(self.graphGroupedNodes_)
        
        for firstGroupUniqueId in self.graphGroupedNodes_:
            paramsArr['group_'+firstGroupUniqueId+'_length'] = len(self.graphGroupedNodes_[firstGroupUniqueId])

        return paramsArr


    def visualizeGraph(self, fileName = 'graph.png', figureX = 20, figureY = 20):

        plt.figure(figsize=(figureX, figureY))

        nodesPositions = nx.spring_layout(self.graph_, seed = 100)

        graphNodes = self.getNodesList(True)
        nodesColorsMap = [data['color'] for u,data in graphNodes]

        graphEdges = self.getEdgesList(True)
        
        edgesColors = [data['color'] for u,v,data in graphEdges]
        edgesWeights = [data['weight'] for u,v,data in graphEdges]

        nx.draw(self.graph_, pos = nodesPositions, with_labels=True,cmap=plt.cm.Set1, node_color=nodesColorsMap, node_size=500, edge_color=edgesColors, width=edgesWeights, linewidths=1)

        # plt.show()
        plt.savefig(fileName)

        
    def addSubjectNodeAsRandomNode(self):

        graphNodes = self.getNodesList(True)

        nodesCount = len(graphNodes)
    
        if (nodesCount <= 0):
            nodesCount = 1

        randomNodeIndex = random.randint(0, nodesCount - 1)

        #self.addNode(self.getSubjectNodeId(), 'red')
        #self.nodesCount_-=1
        #mapping = {randomNodeIndex: self.getSubjectNodeId()}
        #self.graph_ = nx.relabel_nodes(self.graph_, mapping)
        self.setSubjectNodeId(randomNodeIndex)
        self.colorAllEdgesConnectedToNode(self.getSubjectNodeId(), 'green')

    def addSubjectNode(self, subjectNodeEdgeProbabilityToMembersInHisGroup, subjectNodeEdgeProbabilityFromMembersInHisGroup, subjectNodeEdgeProbabilityToMembersInOtherHroups, subjectNodeEdgeProbabilityFromMembersInOtherHroups):

        self.addNode(self.getSubjectNodeId(), 1)


        selectedGroupId = random.choice(list(self.graphGroupedNodes_.keys()))

        for selectedGroupNodeId in self.graphGroupedNodes_[selectedGroupId]:
            
            if (self.isDirected_):

                if random.random() < subjectNodeEdgeProbabilityToMembersInHisGroup:
                    self.connectSubjectNodeTo(selectedGroupNodeId)
                    
            if random.random() < subjectNodeEdgeProbabilityFromMembersInHisGroup:
                self.connectNodeToSubjectNode(selectedGroupNodeId)


        for groupId in self.graphGroupedNodes_:

            # Skipping the selected group
            if (selectedGroupId == groupId):
                continue

            for otherGroupNodeId in self.graphGroupedNodes_[groupId]:
                
                if (self.isDirected_):

                    if random.random() < subjectNodeEdgeProbabilityToMembersInOtherHroups:
                        self.connectSubjectNodeTo(otherGroupNodeId)
                        
                if random.random() < subjectNodeEdgeProbabilityFromMembersInOtherHroups:
                    self.connectNodeToSubjectNode(otherGroupNodeId)


    def connectSubjectNodeTo(self, destNodeId):
        return self.addEdge(self.getSubjectNodeId(), destNodeId)

    def connectNodeToSubjectNode(self, sourceNodeId):
        return self.addEdge(sourceNodeId, self.getSubjectNodeId())

    def loadFromOtherGraph(self, otherGraphObj):

        if (self.isDirected_):
            self.graph_ = nx.DiGraph()
        else:
            self.graph_ = nx.Graph()

        for innerFromeNodeId, innerToNodeId, edgeParams in otherGraphObj.edges(data = True):

            weight = 1.0
            
            if ('weight' in edgeParams):
                weight = edgeParams['weight']

            color = 'lightblue'
            
            if ('color' in edgeParams):
                color = edgeParams['color']

            self.addEdge(innerFromeNodeId, innerToNodeId, weight, color)

            if (not self.isDirected_):
                self.addEdge(innerToNodeId, innerFromeNodeId, weight, color)

    def loadGraphFromFile(self, graphFilePath):

        if (self.isDirected_):
            self.graph_ = nx.DiGraph()
        else:
            self.graph_ = nx.Graph()


        with open(graphFilePath, "r") as f:
            for line in f:
            
                sp = line.split(" ")

                self.addEdge(int(sp[0]), int(sp[1]), 1.0, 'lightblue')

                if (not self.isDirected_):
                    self.addEdge(int(sp[1]), int(sp[0]), 1.0, 'lightblue')
            
    """
    Generates a random group, enforcing that the resulting group is conneted
    """
    def generateRandomGroup(self, minNodesCount = 2, maxNodesCount = 10, edgeProbability = 0.01):
        #groupUniqueIdentifier = ''
        print("generateRandomGroup")
        base = self.getNodesCount()
#        print(groupUniqueIdentifier, minNodesCount, maxNodesCount, edgeProbability)
        if (minNodesCount < 0):

            if (self.printErrors_):
                print('minNodesCount' + str(minNodesCount))
                print('Error: minNodesCount must be greater than zero. Setting minNodesCount = 1')
                
            minNodesCount = 1

        if (maxNodesCount < minNodesCount):

            if (self.printErrors_):
                print('minNodesCount' + str(minNodesCount))
                print('maxNodesCount' + str(maxNodesCount))
                print('Error: maxNodesCount must be greater or equal to minNodesCount. Setting maxNodesCount = ' + str(minNodesCount))
                
            maxNodesCount = minNodesCount

                
        groupNodesCount = random.randint(minNodesCount, maxNodesCount)
        self.nodesCount_ += groupNodesCount

        if (self.verbose_):
            print('Generating random group. Nodes count: ' + str(groupNodesCount))


        if edgeProbability <= 0:
            return self.graph_
            
        # if edgeProbability >= 1:
        #     return nx.complete_graph(groupNodesCount, create_using = self.graph_)
            

        nodesNamesList = []

        for nodeIndex in range(groupNodesCount):
            nodeName = base + nodeIndex

            self.graph_.add_node(nodeName, color = (abs(hash(str(base))) % (10 ** 4)))

            nodesNamesList.append(nodeName)

        edges = combinations(nodesNamesList, 2)

        self.graphGroupedNodes_[str(base)] = nodesNamesList


        for _, node_edges in groupby(edges, key=lambda x: x[0]):

            node_edges = list(node_edges)

            random_edge = random.choice(node_edges)


            if (not self.isDirected_):
                self.graph_.add_edge(random_edge[0], random_edge[1], weight = 1.0, color='lightblue')
            else:
                if random.random() > 0.5:
                    self.graph_.add_edge(random_edge[1], random_edge[0], weight = 1.0, color='lightblue')
                else:
                    self.graph_.add_edge(random_edge[0], random_edge[1], weight = 1.0, color='lightblue')


            for e in node_edges:
                if random.random() < edgeProbability:
                    self.graph_.add_edge(e[0], e[1], weight = 1.0, color='lightblue')


    def getUniqueGroupId(self, groupNumber, jumpStep):

        lettersList = list(string.ascii_uppercase)

        allIdsList = []

        for i in range(len(lettersList)):
            for j in range(len(lettersList)):
                allIdsList.append(lettersList[i] + lettersList[j])

        return allIdsList[(jumpStep + groupNumber) % len(allIdsList)]
           
    def colorAllNodes(self, color):

        for node in self.graph_.nodes(True):
            node[1]['color'] = color
            
    def colorAllEdges(self, color):

        graphEdges = self.getEdgesList(True)

        for edge in graphEdges:
            edge[2]['color'] = color
            
    def colorAllEdgesConnectedToNode(self, nodeId, color):
            
        edgesFromNode = self.getEdgesFromNode(nodeId)
        edgesToNode = self.getEdgesToNode(nodeId)

        for edge in edgesFromNode:            
            self.setEdgeColor(edge[0], edge[1], color)

        for edge in edgesToNode:
            self.setEdgeColor(edge[0], edge[1], color)
            
            
    def addWeightToAllEdges(self, weight):

        graphEdges = self.getEdgesList(True)

        for edge in graphEdges:
            edge[2]['weight'] = weight
            
    def generateSmallWorldNetwork(self, n, m, p, t):

        self.graph_ = nx.connected_watts_strogatz_graph(n, m, p, t)

        self.nodesCount_ = len(self.graph_.nodes())

        self.colorAllNodes('lightblue')

        self.colorAllEdges('lightblue')

        self.addWeightToAllEdges(1.0)

    def generateRandom(self, connectedGroupsCount = 1, minNodesCountInSingleGroup = 2, maxNodesCountInSingleGroup = 10, edgeProbabilityInSingleGroup = 0.01, edgeProbabilityBetweenGroups = 0.01):
        print("generateRandom")
        print(connectedGroupsCount, minNodesCountInSingleGroup, maxNodesCountInSingleGroup, edgeProbabilityInSingleGroup, edgeProbabilityBetweenGroups)
        if (self.isDirected_):
            self.graph_ = nx.DiGraph()
        else:
            self.graph_ = nx.Graph()

        # 
        # Generating groups
        # 
        for connectedGroupIndex in range(connectedGroupsCount):

            groupUniqueId = self.getUniqueGroupId(connectedGroupIndex, connectedGroupIndex * 26)

            self.generateRandomGroup(minNodesCountInSingleGroup, maxNodesCountInSingleGroup, edgeProbabilityInSingleGroup)

            if (self.verbose_):
                print('---')
                print('Group ' + groupUniqueId + ' created')
            
        # 
        # Connecting different groups
        # 
        for firstGroupUniqueId in self.graphGroupedNodes_:

            for secondGroupUniqueId in self.graphGroupedNodes_:

                if (firstGroupUniqueId == secondGroupUniqueId):
                    continue

                for firstGroupNodeId in self.graphGroupedNodes_[firstGroupUniqueId]:
                    for secondGroupNodeId in self.graphGroupedNodes_[secondGroupUniqueId]:
                            
                        if random.random() < edgeProbabilityBetweenGroups:
                            self.graph_.add_edge(firstGroupNodeId, secondGroupNodeId, weight = 1.0, color='black')


        if (self.verbose_):
            print('---')
            print('Random graph generated:')
            self.printGraph()
            print('---')


    def calculateMinCut(self):

        if (self.isDirected_):

            print('Not implemented for directed. See for more details:')
            print('https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.stoerwagner.stoer_wagner.html#networkx.algorithms.connectivity.stoerwagner.stoer_wagner')

            return
        component = list(self.getConnectedComponents())
        if(len(component) >1):
            return[0,component]
        if(self.graph_.number_of_nodes() <2):
            return[0,[self.graph_.nodes,[]]]
        cut_value, partition = nx.stoer_wagner(self.graph_)
        
        return [cut_value, partition]

    def calculateMinSTCut(self, s,t):
        copyOfGraph = copy.deepcopy(self)
        if (copyOfGraph.isDirected_):
            print('Not implemented for directed. See for more details:')
            print('https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.stoerwagner.stoer_wagner.html#networkx.algorithms.connectivity.stoerwagner.stoer_wagner')
            return
        edges = nx.connectivity.cuts.minimum_st_edge_cut(copyOfGraph.graph_, s,t)
        return edges

    def calculateBestMinCut(self):
        copyOfGraph = copy.deepcopy(self)
        for u,v in copyOfGraph.getEdgesList():
             if(u == self.getSubjectNodeId() or (not copyOfGraph.isDirected()) and v == self.getSubjectNodeId()):
                #graph[e[0]][e[1]]['weight'] = 1-(1/graph.nodesCount_)
                copyOfGraph.setEdgeWeight(u,v,1+(1/copyOfGraph.nodesCount_))
        return copyOfGraph.calculateMinCut()

    def calculateWorstMinCut(self):
        copyOfGraph = copy.deepcopy(self)
        for u,v in copyOfGraph.getEdgesList():
             if(u == self.getSubjectNodeId() or (not copyOfGraph.isDirected()) and v == self.getSubjectNodeId()):
                #graph[e[0]][e[1]]['weight'] = 1-(1/graph.nodesCount_)
                copyOfGraph.setEdgeWeight(u,v,1-(1/copyOfGraph.nodesCount_))
        return copyOfGraph.calculateMinCut()

    def calculateWorstSTMinCut(self,s,t):
        copyOfGraph = copy.deepcopy(self)
        for u,v in copyOfGraph.getEdgesList():
             if(u == self.getSubjectNodeId() or (not copyOfGraph.isDirected()) and v == self.getSubjectNodeId()):
                #graph[e[0]][e[1]]['weight'] = 1-(1/graph.nodesCount_)
                copyOfGraph.setEdgeWeight(u,v,1-(1/copyOfGraph.nodesCount_))
        return copyOfGraph.calculateMinSTCut(s,t)


    def rankOfWorstMinCut(self):
        copyOfGraph = copy.deepcopy(self)
        for u,v in copyOfGraph.getEdgesList():
             if(u == self.getSubjectNodeId() or (not copyOfGraph.isDirected()) and v == self.getSubjectNodeId()):
                #graph[e[0]][e[1]]['weight'] = 1-(1/graph.nodesCount_)
                copyOfGraph.setEdgeWeight(u,v,1-(1/copyOfGraph.nodesCount_))
        return  BasicEstimator.rank(copyOfGraph, copyOfGraph, ObjectiveNames.MAX_UTIL, self.getSubjectNodeId())
    @staticmethod
    def reverseEdges(edgesList):
        output = []

        for edge in edgesList:
            output.append(edge[::-1])
        
        return output


    # @staticmethod
    # def getGraphDescriptionFromXml(xmlObject):

    #     emptyGraphDescription = Graph.toArray(Graph(''))

    #     return BaseManager.getObjectDescriptionFromXml(xmlObject, emptyGraphDescription)


    def getEdgeWeight(self, fromNodeId, toNodeId):

        for innerFromeNodeId, innerToNodeId, edgeParams in self.graph_.edges(data=True):

            if (innerFromeNodeId == fromNodeId and innerToNodeId == toNodeId):
                return edgeParams['weight']

        return 1.0

    def setEdgeWeight(self, fromNodeId, toNodeId, newEdgeWeight):

        for innerFromeNodeId, innerToNodeId, edgeParams in self.graph_.edges(data=True):

            if (innerFromeNodeId == fromNodeId and innerToNodeId == toNodeId):
                edgeParams['weight'] = newEdgeWeight

                return True

        return False

    def setEdgeColor(self, fromNodeId, toNodeId, newEdgeColor):

        for innerFromeNodeId, innerToNodeId, edgeParams in self.graph_.edges(data=True):

            if (innerFromeNodeId == fromNodeId and innerToNodeId == toNodeId):
                edgeParams['color'] = newEdgeColor

                return True

        return False

    def setNodeColor(self, nodeId, newColor):

        for innerFromeNodeId, nodeParams in self.graph_.nodes(data=True):

            if (innerFromeNodeId == nodeId):
                nodeParams['color'] = newColor

                return True

        return False

    def addEdgesToGroup(self, par1, par2):
        
        if(self.getSubjectNodeId() in par1):
            par=par1
        else:
            par= par2
            
        for v in par:
            if(not(self.isEdgeExists(self.getSubjectNodeId(),v) or (not self.isDirected() and self.isEdgeExists(v, self.getSubjectNodeId())))):
                self.addEdge(self.getSubjectNodeId(),v)

    def removeEdgesfromSecGroup(self, par1, par2):

        if(self.getSubjectNodeId() in par1):
            par=par2
        else:
            par= par1

        for v in par:
            if(self.isEdgeExists(self.getSubjectNodeId(),v) or (not self.isDirected() and self.isEdgeExists(v, self.getSubjectNodeId()))):
                self.removeEdge(self.getSubjectNodeId(),v)

    def addAndRemoveEdges(self, par1,par2):
        self.addEdgesToGroup(par1,par2)
        self.removeEdgesfromSecGroup(par1,par2)

    def getN1GroupOfNode(self, targetNodeId):

        return self.getN1GroupOfNodePair(targetNodeId, targetNodeId)

    def getN1GroupOfNodePair(self, firstTargetNodeId, secondTargetNodeId):

        targetNodeNeighbors = self.getNodeNeighbors(firstTargetNodeId)

        output = []

        for firstTargetNodeNeighborId in targetNodeNeighbors:

            neighborsOfFirstTargetNeighbor = self.getNodeNeighbors(firstTargetNodeNeighborId)

            if (secondTargetNodeId in neighborsOfFirstTargetNeighbor):

                if (firstTargetNodeId != secondTargetNodeId):

                    if (len(neighborsOfFirstTargetNeighbor) == 2):
                        output.append(firstTargetNodeNeighborId)
                else:

                    if (len(neighborsOfFirstTargetNeighbor) == 1):
                        output.append(firstTargetNodeNeighborId)

        return output

    def getNodeNeighborsCount(self, nodeId):
        return len(self.getNodeNeighbors(nodeId))

    def getNodeNeighbors(self, nodeId):
        return list(self.graph_.neighbors(nodeId))

    def get_all_mincuts_directed(self):

        g = self.graph_

        self_loops = list(nx.selfloop_edges(g))
        g.remove_edges_from(self_loops)

        input_path = "temp"
        number_to_node = Utils.directed_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "t.out"]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(output.stdout)
        print(output.stderr)
        print(cpp_command)

        so = output.stdout
        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        G = nx.read_graphml("t.out")
        swgroups = []
        cuts = []
        for edge in G.edges():
            node1 = edge[0]
            node2 = edge[1]
            weight = G.edges[edge]['weight']

            if weight == cut_size:
                temp = G.copy()
                temp.remove_edge(edge[0], edge[1])
                a1, a2 = nx.connected_components(temp)

                c1lst = []
                c2lst = []
                for node1 in a1:
                    if 'containedVertices' in G.nodes[node1] and G.nodes[node1]['containedVertices'] != "" :
                        c1lst.append(G.nodes[node1]['containedVertices'])
                for node2 in a2:
                    if 'containedVertices' in G.nodes[node2] and G.nodes[node2]['containedVertices'] != "" :
                        c2lst.append(G.nodes[node2]['containedVertices'])
                c1 = ",".join(c1lst)
                c2 = ",".join(c2lst)
                try:
                    cc1 = [] if c1 == "" else [number_to_node[int(k)] for k in c1.split(",")]
                    cc2 = [] if c2 == "" else [number_to_node[int(k)] for k in c2.split(",")]

                except Exception as e:
                    with open("errors.log", "a") as f:
                        print(c1, file=f)
                        print(c2, file=f)
                    raise e

                cut = list(nx.edge_boundary(g, cc1, cc2))
                if len(cut) == 2:
                    print(weight, cut_size, cc1, cc2)
                    print(cut)

                cuts.append(cut)

            elif weight < cut_size:
                print(weight, cut_size)
                swgroups.append((edge[0], edge[1]))

        for comb in itertools.combinations(swgroups, 2):  # a cut in G contains one tree edge or two cycle edges.
            temp = G.copy()
            temp.remove_edge(comb[0][0], comb[0][1])
            temp.remove_edge(comb[1][0], comb[1][1])

            components = list(nx.connected_components(temp))
            if len(components) <2:
                continue
            a1 = components[0]
            a2 = components[1]
            c1 = ",".join([G.nodes[node1]['containedVertices'] for node1 in a1])
            c2 = ",".join([G.nodes[node2]['containedVertices'] for node2 in a2])
            c1 = c1.replace(",,", ",").strip(",")
            c2 = c2.replace(",,", ",").strip(",")
            cc1 = [number_to_node[int(k)] for k in c1.split(",")]
            cc2 = [number_to_node[int(k)] for k in c2.split(",")]
            cut1 = list(nx.edge_boundary(g, cc1, cc2))
            cut2 = list(nx.edge_boundary(g, cc2, cc1))
            cut = cut1 + cut2

            cuts.append(cut)

        return cuts


    def get_all_mincuts_undirected(self):

        g = self.graph_

        input_path = "temp"
        number_to_node = Utils.undirected_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "t.out"]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout
        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        G = nx.read_graphml("t.out")
        swgroups = []
        cuts = []
        for edge in G.edges():

            weight = G.edges[edge]['weight']

            if weight == cut_size:
                temp = G.copy()
                temp.remove_edge(edge[0], edge[1])
                a1, a2 = nx.connected_components(temp)

                c1lst = []
                c2lst = []
                for node1 in a1:
                    if 'containedVertices' in G.nodes[node1] and G.nodes[node1]['containedVertices'] != "" :
                        c1lst.append(G.nodes[node1]['containedVertices'])
                for node2 in a2:
                    if 'containedVertices' in G.nodes[node2] and G.nodes[node2]['containedVertices'] != "" :
                        c2lst.append(G.nodes[node2]['containedVertices'])

                c1 = ",".join(c1lst)
                c2 = ",".join(c2lst)

                cc1 = [] if c1 == "" else [number_to_node[int(k)] for k in c1.split(",")]
                cc2 = [] if c2 == "" else [number_to_node[int(k)] for k in c2.split(",")]
                cuts.append((cc1, cc2))

            elif weight < cut_size:
                swgroups.append((edge[0],edge[1]))

        for comb in itertools.combinations(swgroups, 2):  # a cut in G contains one tree edge of two cycle edges.
            temp = G.copy()
            temp.remove_edge(comb[0][0], comb[0][1])
            temp.remove_edge(comb[1][0], comb[1][1])
            components = list(nx.connected_components(temp))
            if len(components)<2:
                continue

            a1 = components[0]
            a2 = components[1]

            c1 = ",".join([G.nodes[node1]['containedVertices'] for node1 in a1])
            c2 = ",".join([G.nodes[node2]['containedVertices'] for node2 in a2])
            cc1 = [number_to_node[int(k)] for k in c1.split(",")]
            cc2 = [number_to_node[int(k)] for k in c2.split(",")]
            cuts.append((cc1, cc2))

        return cuts


    def saveToFile(self, destinationPath):

        nextNodeIndex = 1
        nodesMap = {}
        nodesReverseMap = {}

        fileHandler = open(destinationPath, "w+")
        
        fileHandler.write('p edge ')
        fileHandler.write(str(len(self.graph_.nodes())))
        fileHandler.write(' ')
        fileHandler.write(str(len(self.graph_.edges())))
        fileHandler.write("\n")

        for innerNodeId, innerNodeEdges in groupby(self.graph_.edges(), key=lambda x: x[0]):
            
            for edge in list(innerNodeEdges):

                if (edge[0] not in nodesMap):
                    nodesMap[edge[0]] = nextNodeIndex
                    nodesReverseMap[nextNodeIndex] = edge[0]
                    nextNodeIndex += 1

                mappedLeftNodeId = nodesMap[edge[0]]


                if (edge[1] not in nodesMap):
                    nodesMap[edge[1]] = nextNodeIndex
                    nodesReverseMap[nextNodeIndex] = edge[1]
                    nextNodeIndex += 1

                mappedRightNodeId = nodesMap[edge[1]]


                # left -> right (e right left === e tail head)
                fileHandler.write('e ' + str(mappedRightNodeId) + ' ' + str(mappedLeftNodeId))
                fileHandler.write("\n")

        fileHandler.close()

        return nodesReverseMap


    def getAllMinCuts(self, filePrefix, outputFormat = 'edges', returnOnlyMinimalCut = False, numberOfPartitions = 2):

        tempFilePath = './graphs/' + str(filePrefix) + '_' + Utils.generateRandomString(7)

        nodesMap = self.saveToFile(tempFilePath)

        isDirectedGraphParam = 'false'

        if (self.isDirected()):
            isDirectedGraphParam = 'true'


        cpp_command = ["./executables/karger", tempFilePath, isDirectedGraphParam, str(numberOfPartitions), outputFormat]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        executableOutput = output.stdout

        
        cutsList = []

        if ('edges' == outputFormat):

            cutsStrings = executableOutput.split('&')
    
            for cutString in cutsStrings:

                if ("\n" == cutString):
                    continue

                partitionsStrings = cutString.split('|')

                cutPartitions = []

                for partitionStr in partitionsStrings:

                    if ('' == partitionStr or "\n" == partitionStr):
                        continue

                    nodesStrs = partitionStr.split(',')

                    if (len(nodesStrs) < 2):
                        continue

                    cutPartitions.append(
                            (nodesMap[int(nodesStrs[0]) + 1], nodesMap[int(nodesStrs[1]) + 1])
                        )


                if (len(cutPartitions) < 1):
                    continue

                cutsList.append(cutPartitions)
        else:
        
            cutsStrings = executableOutput.split('&')
    
            for cutString in cutsStrings:

                if ("\n" == cutString):
                    continue

                partitionsStrings = cutString.split(',;')

                cutPartitions = []
        
                for partitionStr in partitionsStrings:

                    if ('' == partitionStr):
                        continue

                    nodesStrs = partitionStr.split(',')

                    partitionNodes = []
                    for nodeInt in nodesStrs:
                        partitionNodes.append(nodesMap[int(nodeInt) + 1])

                    cutPartitions.append(partitionNodes)


                if (len(cutPartitions) < 1):
                    continue

                cutsList.append(cutPartitions)

        if (returnOnlyMinimalCut and len(cutsList) > 0):
            return cutsList[0]

        return cutsList
