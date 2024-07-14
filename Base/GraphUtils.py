import random
import networkx as nx

class GraphUtils:

    @staticmethod
    def add_neighbors_2dfs(g, subgraph, node, n, num_of_friends = 2):
        starting_vertex = node
        queue = [starting_vertex]
        # Define the number of vertices you want in your subgraph
        numOfVertices = n  # Adjust this value as needed
        # print("add_neighbors_2dfs")
        while len(subgraph.nodes()) < numOfVertices and  len(queue) >0:
            # Take the first vertex from the queue
            current_vertex = queue.pop(0)
            if len(subgraph.nodes()) >1 and subgraph.has_node(current_vertex):
                continue
            # Add this vertex to the subgraph
            subgraph.add_node(current_vertex)
            # Get the neighbors of the current vertex
            #neighbors = list(g.neighbors(current_vertex))
            neighbors = sorted(list(g.neighbors(current_vertex)), key=lambda x: -len(list(g.neighbors(x))))
            # Take the first two neighbors and add them to the queue
            if len(neighbors) <= num_of_friends:
                queue.extend(neighbors)
            else:
                queue.extend(neighbors[:num_of_friends])
        selected_vertices = subgraph.nodes()       
        for vertex in selected_vertices:
            neighbors = list(g.neighbors(vertex))
            for neighbor in neighbors:
                if neighbor in selected_vertices:
                    subgraph.add_edge(vertex, neighbor)



    # Define a function to add neighbors up to n levels deep
    @staticmethod
    def add_neighbors(g, subgraph, node, n):
        if n == 0:
            return
        in_neighbors = list(g.predecessors(node))
        out_neighbors = list(g.successors(node))
        subgraph.add_nodes_from(in_neighbors)
        subgraph.add_nodes_from(out_neighbors)

        subgraph.add_edges_from((node, neighbor) for neighbor in out_neighbors)
        subgraph.add_edges_from((neighbor,node) for neighbor in in_neighbors)

        for neighbor in out_neighbors:
            GraphUtils.add_neighbors(g, subgraph, neighbor, n - 1)
        for neighbor in in_neighbors:
            GraphUtils.add_neighbors(g, subgraph, neighbor, n - 1)

    @staticmethod
    def force_degree(g, deg):
        low_degree_nodes = [node for node in g.nodes if g.out_degree(node)+ g.in_degree(node) < deg]
        g.remove_nodes_from(low_degree_nodes)
        low_degree_nodes = [node for node in g.nodes if g.out_degree(node)+ g.in_degree(node) < deg]
        g.remove_nodes_from(low_degree_nodes)
        low_degree_nodes = [node for node in g.nodes if g.out_degree(node)+ g.in_degree(node) < deg]
        g.remove_nodes_from(low_degree_nodes)
        low_degree_nodes = [node for node in g.nodes if g.out_degree(node)+ g.in_degree(node) < deg]
        g.remove_nodes_from(low_degree_nodes)
        low_degree_nodes = [node for node in g.nodes if g.out_degree(node)+ g.in_degree(node) < deg]
        g.remove_nodes_from(low_degree_nodes)

    @staticmethod
    def retain_portion(g, maxNodesCount, graphIsDirected = False, numOfFriends = 2, saveGraphEnabled = False):

        selected_nodes = random.sample(list(g.nodes()), 1)
        #todo:remove!

        # Create a subgraph with the selected nodes
        if (graphIsDirected):
            subgraph = nx.DiGraph(g.subgraph(selected_nodes))
        else:
            subgraph = nx.Graph(g.subgraph(selected_nodes))
        GraphUtils.add_neighbors_2dfs(g,subgraph, selected_nodes[0], maxNodesCount, numOfFriends)

        ls = []
        for node in subgraph.nodes:
            ls.append((node, subgraph.degree(node)))

        newNodesList = ls[:min(maxNodesCount, len(ls))]

        if (graphIsDirected):
            subgraph = nx.DiGraph(subgraph.subgraph([item[0] for item in newNodesList]))
            
        else:
            subgraph = nx.Graph(subgraph.subgraph([item[0] for item in newNodesList]))

        if (saveGraphEnabled):
            GraphUtils.save_graph(subgraph, "stored_graph.graphml")

        return subgraph

    @staticmethod
    def fetch_portion_of_graph(dataFileName, graphIsDirected = False, nodesCount = 5, numOfFriends = 2):

        print('nodesCount')
        print(nodesCount)

        print('numOfFriends')
        print(numOfFriends)

        if (graphIsDirected):
            g = nx.DiGraph()
        else:
            g = nx.Graph()

        with open("datasets/" + dataFileName, "r") as f:
            for line in f:
                sp = line.split(" ")
                if int(sp[0]) not in g.nodes():
                    g.add_node(int(sp[0]))
                if int(sp[1]) not in g.nodes():
                    g.add_node(int(sp[1]))
                if (int(sp[0]), int(sp[1])) not in g.edges() and (int(sp[1]), int(sp[0])) not in g.edges():
                    g.add_edge(int(sp[0]), int(sp[1]))
        subgraph = GraphUtils.retain_portion(g, nodesCount, graphIsDirected, numOfFriends)
        num_t = 0
        while  len(subgraph.nodes) < nodesCount and num_t < 100:
            subgraph = GraphUtils.retain_portion(g, nodesCount, graphIsDirected, numOfFriends)
            num_t += 1
        return subgraph

    @staticmethod
    def fetch_whole_graph(dataFileName, graphIsDirected = False):

        if (graphIsDirected):
            g = nx.DiGraph()
        else:
            g = nx.Graph()

        with open("datasets/" + dataFileName, "r") as f:
            for line in f:
                sp = line.split(" ")
                if int(sp[0]) not in g.nodes():
                    g.add_node(int(sp[0]))
                if int(sp[1]) not in g.nodes():
                    g.add_node(int(sp[1]))
                if (int(sp[0]), int(sp[1])) not in g.edges() and (int(sp[1]), int(sp[0])) not in g.edges():
                    g.add_edge(int(sp[0]), int(sp[1]))

        return g


    @staticmethod
    def save_graph(g, gpath):
        nx.write_graphml(g, gpath)


    @staticmethod
    def load_graph(gpath):
        g = nx.read_graphml(gpath)
        return g

