from ManipulatorActions import ManipulatorActions

import os
import sys
import subprocess
import itertools
import math
import networkx as nx
from collections import deque
import random
import string
import copy

class Utils:

    @staticmethod
    def generateRandomString(length):
        
        return ''.join(random.choice(string.ascii_letters) for i in range(length))

    @staticmethod
    def combinations(n, k):
        return sum(math.comb(n, r) for r in range(1, k + 1))

    @staticmethod
    def count_iter_items(iterable):
        """
        Consume an iterable not reading it into memory; return the number of items.
        """
        counter = itertools.count()
        deque(zip(iterable, counter), maxlen=0)  # (consume at C speed)
        return next(counter)

    # @staticmethod
    # def get_subsets_m_plus_set_size_only(edges, csize, min_cut_size):

    #     edges_count = graphObj.edges()
    #     csize
    #     min_cut_size
    #     for r in range(min_cut_size, csize + 1):

    @staticmethod
    def get_subsets_m_plus(edges, csize, min_cut_size):
        edges = sorted(list(edges))
        sample = (itertools.chain.from_iterable(itertools.combinations(edges, r) for r in range(min_cut_size, csize + 1)))

        # sample = iter([[(136137625,282193031), (136137625,15187983), (136137625,90046723), (136137625,76027335), (136137625,167947361), (136137625,54475994), (169112757,136137625)]])

        return sample

    @staticmethod
    def subtractLists(x, y):
        return list(set(x) - set(y))

    @staticmethod
    def edgesToUniqueNodesList(edgesList):

        nodesList = set()

        for edge in edgesList:
            nodesList.add(edge[0])
            nodesList.add(edge[1])
            
        return list(nodesList)

    @staticmethod
    def undirected_to_metis(g, path):
        node_to_number = {}
        nodes = sorted(list(g.nodes()))
        for i, node in enumerate(nodes, start=0):
            node_to_number[node] = i + 1

        with open(path, "w") as f:
            print("{} {}".format(len(g.nodes()), len(g.edges())), file=f)
            nodes = list(g.nodes())
            nodes.sort()
            n = 0

            for node in nodes:
                neighbors = []
                for neighbor in g.neighbors(node):
                    neighbors.append(node_to_number[neighbor])
                neighbors = sorted(neighbors)
                st = ""
                for neighbor in neighbors:
                    st = st + str(neighbor) + " "
                    n += 1
                st = st.strip()
                print(st, file=f)

        with open(path + "_mapping", "w") as f:
            number_to_node = {}
            for k, v in node_to_number.items():
                number_to_node[v - 1] = k
                print("{},{}".format(v, k), file=f)
        return number_to_node

    @staticmethod
    def directed_to_metis(g, path):
        self_loops = list(nx.selfloop_edges(g))
        g.remove_edges_from(self_loops)

        gu = nx.Graph((edge[0], edge[1], {'weight': 1 + int(g.has_edge(edge[1], edge[0]))}) for edge in g.edges())

        node_to_number = {}
        nodes = sorted(list(g.nodes()))
        for i, node in enumerate(nodes, start=0):
            node_to_number[node] = i + 1
        with open(path, "w") as f:
            print("{} {} 1".format(len(gu.nodes()), len(gu.edges())), file=f) #add edge weights
            nodes = list(gu.nodes())
            nodes.sort()
            n = 0
            cnt = 0
            cnt2 = 0

            for node in nodes:
                neighbors = []
                weights = []
                for neighbor in gu.neighbors(node):
                    cnt2 += 1
                    neighbors.append(node_to_number[neighbor])
                    weights.append(gu[node][neighbor])
                cnt += len(neighbors)

                neighbors = sorted(zip(neighbors, weights), key=lambda x: x[0])
                st = ""
                for neighbor in neighbors:
                    neighborj = " ".join([str(neighbor[0]),str(int(neighbor[1]['weight']))])
                    st = st + str(neighborj) + " "
                    n += 1
                st = st.strip()
                print(st, file=f)
        with open(path + "_mapping", "w") as f:
            number_to_node = {}
            for k, v in node_to_number.items():
                number_to_node[v - 1] = k
                print("{},{}".format(v, k), file=f)
        return number_to_node

    @staticmethod
    def metis_to_undirected(path):
        number_to_node = {}
        node_to_number = {}
        with open(path + "_mapping", "r") as f:
            for l in f:
                sp = l.split(",")
                num = sp[0].strip()
                val = sp[1].strip()

                try:
                    val = int(val)
                except:
                    pass
                try:
                    num = int(num)
                except:
                    pass
                #            print(num, val)
                number_to_node[num] = val
                node_to_number[val] = num

        g = nx.Graph()
        with open(path, "r") as f:
            first = True
            for lid, line in enumerate(f):
                if lid == 0:
                    continue
                else:
                    lid = number_to_node[int(lid)]  # removing one since the first line contains different data
                    g.add_node(lid)
                    #                print(line, flush=True)
                    for item in line.split(" "):
                        #                    print("item: " , item)
                        item = number_to_node[int(item)]
                        g.add_edge(lid, item)

        return g, node_to_number

    @staticmethod
    def get_all_mincuts(g,m):
        # input_path = "/tmp/temp"
        input_path = "/tmp/temp_{}".format(m)
        number_to_node = Utils.undirected_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "/tmp/t_{}.out".format(m)]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout

        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        G = nx.read_graphml("/tmp/t_{}.out".format(m))
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

                cuts.append(cut)

            elif weight < cut_size:
                swgroups.append((edge[0], edge[1]))

        for comb in itertools.combinations(swgroups, 2):  # a cut in G contains one tree edge or two cycle edges.
            temp = G.copy()
            temp.remove_edge(comb[0][0], comb[0][1])
            temp.remove_edge(comb[1][0], comb[1][1])

            components = list(nx.connected_components(temp))
            if len(components) < 2:
                continue
            a1 = components[0]
            a2 = components[1]
            c1 = ",".join([G.nodes[node1]['containedVertices'] for node1 in a1])
            c2 = ",".join([G.nodes[node2]['containedVertices'] for node2 in a2])
            c1 = c1.replace(",,", ",").strip(",")
            c2 = c2.replace(",,", ",").strip(",")
            cc1 = [number_to_node[int(k)] for k in c1.split(",")]
            cc2 = [number_to_node[int(k)] for k in c2.split(",")]
            cut = list(nx.edge_boundary(g, cc1, cc2))
            cuts.append(cut)

        return cuts

    @staticmethod
    def apply_respect_manipulation(g, manipulatorNodeId, components, manipulatorActionType, outputManipulations):

        graphCopy = g.copy()

        localManipulationsDict = {}
        
        graphCopyEdgesList = graphCopy.edges()

            
        for component in components:
        
            manipulatorFoundInThisComponent = False

            if (manipulatorNodeId in component):
                manipulatorFoundInThisComponent = True

            for nodeId in component:

                if nodeId == manipulatorNodeId:
                    continue


                if (manipulatorFoundInThisComponent):

                    if (manipulatorActionType in {ManipulatorActions.ADD_EDGE_ONLY, ManipulatorActions.ADD_OR_REMOVE_EDGE}):

                        if (str(manipulatorNodeId) + str(nodeId) not in localManipulationsDict):
                        
                            graphCopy.add_edge(manipulatorNodeId, nodeId)
                            outputManipulations.append((manipulatorNodeId, nodeId))

                            # Used for filtering
                            localManipulationsDict[str(manipulatorNodeId) + str(nodeId)] = True
                else:

                    if (manipulatorActionType in {ManipulatorActions.ADD_OR_REMOVE_EDGE, ManipulatorActions.REMOVE_EDGE_ONLY}):

                        if ((manipulatorNodeId, nodeId) in graphCopyEdgesList):

                            graphCopy.remove_edge(manipulatorNodeId, nodeId)
                            outputManipulations.append((manipulatorNodeId, nodeId))

                            del graphCopyEdgesList[(manipulatorNodeId, nodeId)]

        return graphCopy


    @staticmethod
    def getManipulatorNeighborsInComponent(components, manipulatorNodeId, manipulatorNeighbors):

        mNeighborsCountInComponent = 0

        for component in components:
        
            if (manipulatorNodeId in component):

                for nodeId in component:

                    if (manipulatorNodeId == nodeId):
                        continue

                    if (nodeId in manipulatorNeighbors):
                
                        mNeighborsCountInComponent += 1

                break


        return mNeighborsCountInComponent

    @staticmethod
    def innerp(customGraphObj, g, manipulatorNodeId, neighbors, lowerBound, subset, graphIsDirected, manipulationType = ManipulatorActions.ADD_EDGE_ONLY, useOldCutAlgorithm = False, partitionsCount = 2):

        outputManipulations = []

        gc = g.copy()
        for item in subset:
            gc.remove_edge(item[0], item[1])

        if (graphIsDirected):
            if nx.is_weakly_connected(gc):
                return -2, -2, outputManipulations

            components = list(nx.weakly_connected_components(gc))
        else:
        
            if nx.is_connected(gc):
                return -2, -2, outputManipulations

            components = list(nx.connected_components(gc))
        

        if len(components) > partitionsCount:
            return -2, -2, outputManipulations



        originalGraphManipulatorNeighbors = g.neighbors(manipulatorNodeId)

        mNeighborsCountInComponent = Utils.getManipulatorNeighborsInComponent(components, manipulatorNodeId, originalGraphManipulatorNeighbors)

        
        if (lowerBound > mNeighborsCountInComponent):
            return -2, -2, outputManipulations

        gc = Utils.apply_respect_manipulation(g, manipulatorNodeId, components, manipulationType, outputManipulations)

        customGraphObjCopy = copy.deepcopy(customGraphObj)
        customGraphObjCopy.loadFromOtherGraph(gc)
        # print("succesful aply manipulation")
        if (graphIsDirected):
            mn1, mx1, csize = Utils.cut_value_d(customGraphObjCopy, gc, manipulatorNodeId, neighbors, useOldCutAlgorithm, partitionsCount)
        else:
            mn1, mx1, csize = Utils.cut_value(customGraphObjCopy, gc, manipulatorNodeId, neighbors, useOldCutAlgorithm, partitionsCount)

        if mn1 == 1000:
            return -1, -1, outputManipulations

        return mn1, mx1, outputManipulations


    #input: g-graph, m - manipulator, erm - set of edges in the manipulation, t - type of manipulation
    #output: return the LB and UB of the graph after the manipulation, erm
    @staticmethod
    def lb_ub_for_gm(customGraphObj, g, m, neighbors, erm, graphIsDirected, manipulationType = ManipulatorActions.ADD_EDGE_ONLY, useOldCutAlgorithm = False, partitionsCount = 2):

        gc = g.copy()

        #compute the graph G(m) according to erm
        if manipulationType == ManipulatorActions.REMOVE_EDGE_ONLY:
            gc.remove_edges_from(erm)

        elif manipulationType == ManipulatorActions.ADD_EDGE_ONLY:
            gc.add_edges_from(erm)

        customGraphObjCopy = copy.deepcopy(customGraphObj)
        customGraphObjCopy.loadFromOtherGraph(gc)
        
        if (graphIsDirected):
            output = list(Utils.cut_value_d(customGraphObjCopy, gc, m, neighbors, useOldCutAlgorithm, partitionsCount))
        else:
            output = list(Utils.cut_value(customGraphObjCopy, gc, m, neighbors, useOldCutAlgorithm, partitionsCount))

        output[2] = erm
        
        return output


    @staticmethod
    def cut_value(customGraphObj, gc, manipulatorNodeId, neighbors, useOldCutAlgorithm, partitionsCount): # m is manipulator, cc1 is the part of the cut containing g, cc2 is the other part

        values = []

        if not nx.is_connected(gc):
            components = list(nx.connected_components(gc))
            if len(components) > partitionsCount:
                print("too many components")
                return(1000, 1000, 0)

            all_cuts = [components]
            cut_size = len(components)

        else:
            if (useOldCutAlgorithm):
                all_cuts, cut_size = Utils.get_all_mincuts_f(gc, os.getpid())
            else:
                all_cuts = customGraphObj.getAllMinCuts('cutvalue', 'nodes', False, partitionsCount)

                cut_size = len(all_cuts)

        for singleCutComponents in all_cuts:

            mNeighborsCountInComponent = Utils.getManipulatorNeighborsInComponent(singleCutComponents, manipulatorNodeId, neighbors)

            values.append(mNeighborsCountInComponent)

        return (min(values), max(values), cut_size)


    @staticmethod
    def cut_value_d(customGraphObj, gc, manipulatorNodeId, neighbors, useOldCutAlgorithm, partitionsCount): # m is manipulator, cc1 is the part of the cut containing g, cc2 is the other part

        values = []

        if not nx.is_weakly_connected(gc):
            components = list(nx.weakly_connected_components(gc))
            if len(components) > partitionsCount:
                print("too many components")
                return (1000, 1000,0)

            all_cuts = [components]
            cut_size = len(components)

        # print("graph is connected? " , nx.is_weakly_connected(gc))
        else:
            if (useOldCutAlgorithm):
                all_cuts, cut_size = Utils.get_all_mincuts_df(gc, os.getpid())
            else:
                all_cuts = customGraphObj.getAllMinCuts('cutvalue', 'nodes', False, partitionsCount)

                cut_size = len(all_cuts)


        for singleCutComponents in all_cuts:

            mNeighborsCountInComponent = Utils.getManipulatorNeighborsInComponent(singleCutComponents, manipulatorNodeId, neighbors)

            values.append(mNeighborsCountInComponent)

        return (min(values), max(values), cut_size)



    @staticmethod
    def get_all_mincuts_f(g, pid):

        input_path = "/tmp/temp_{}".format(pid)
        number_to_node = Utils.undirected_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "/tmp/t_{}.out".format(pid)]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout
        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        G = nx.read_graphml("/tmp/t_{}.out".format(pid))
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

        return cuts, cut_size


    @staticmethod
    def get_all_mincuts_df(g,pid):
        self_loops = list(nx.selfloop_edges(g))
        g.remove_edges_from(self_loops)

        input_path = "/tmp/temp_{}".format(pid)
        number_to_node = Utils.directed_to_metis(g, input_path)

        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "/tmp/t_{}.out".format(pid)]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout
        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        G = nx.read_graphml("/tmp/t_{}.out".format(pid))
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

                cuts.append((cc1, cc2))

            elif weight < cut_size:
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
            cuts.append((cc1, cc2))

        return cuts,cut_size

    @staticmethod
    def get_all_mincuts_d(g,m):
        self_loops = list(nx.selfloop_edges(g))
        g.remove_edges_from(self_loops)

        input_path = "/tmp/temp_{}".format(m)
        number_to_node = Utils.directed_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "/tmp/t_{}.out".format(m)]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout
        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        G = nx.read_graphml("/tmp/t_{}.out".format(m))
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
                cut2 = list(nx.edge_boundary(g, cc2, cc1))
                cut.extend(cut2)
                
                cuts.append(cut)

            elif weight < cut_size:
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


    @staticmethod
    def get_cutsize(g,m):
        input_path = "/tmp/temp_{}".format(m)
        number_to_node = Utils.undirected_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "/tmp/t_{}.out".format(m)]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout

        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])
        
        return cut_size

    @staticmethod
    def get_cutsize_d(g,m):
        input_path = "/tmp/temp_{}".format(m)
        number_to_node = Utils.directed_to_metis(g, input_path)
        cpp_command = ["./executables/mincut", input_path, "-s", "cactus", "-t", "/tmp/t_{}.out".format(m)]
        output = subprocess.run(cpp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        so = output.stdout
        
        ind1 = so.index("cut=") + 4
        ind2 = so.index(" ", so.index("cut="))
        ind3 = so.index(" ", ind2)
        cut_size = int(so[ind1:ind3])

        return cut_size

    #input: g-graph, m - manipulator,  1 - add 3 - remove
    #return: set of all possible subset of edges that m can add, remove or remove and add. according to type of manipulation
    @staticmethod
    def get_set_all_manipulation(g, m, manipulationType, lb_limit = -10):
    
        all_subsets = []


        if manipulationType == ManipulatorActions.ADD_EDGE_ONLY: #add
            missing_edges = []
            
            for v in g.nodes():
                if v != m and not g.has_edge(m, v):
                    missing_edges.append((m, v))

            for r in range(1, len(missing_edges) + 1):
                subsets = itertools.combinations(missing_edges, r)
                all_subsets.extend(subsets)

        elif manipulationType == ManipulatorActions.REMOVE_EDGE_ONLY: #minus

            adjacent_edges = list(g.edges(m))
            if lb_limit == -10:
                lb_limit =  len(adjacent_edges)
            elif lb_limit <= 0:
                return []

            for r in range(1, lb_limit + 1):
                subsets = itertools.combinations(adjacent_edges, r)
                all_subsets.extend(subsets)


        return all_subsets
