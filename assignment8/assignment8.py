import pandas as pd
import numpy as np


class Graph:
    def __init__(self):
        self.nodes = []

    def contains(self, name):
        for node in self.nodes:
            if(node.name == name):
                return True
        return False

    # Return the node with the name, create and return new node if not found
    def find(self, name):
        if(not self.contains(name)):
            new_node = Node(name)
            self.nodes.append(new_node)
            return new_node
        else:
            return next(node for node in self.nodes if node.name == name)

    def add_edge(self, parent, child):
        parent_node = self.find(parent)
        child_node = self.find(child)

        parent_node.link_child(child_node)
        child_node.link_parent(parent_node)

    def display(self):
        for node in self.nodes:
            print(f'{node.name} links to {[child.name for child in node.children]}')

    def sort_nodes(self):
        self.nodes.sort(key=lambda node: int(node.name))

    def display_hub_auth(self):
        for node in self.nodes:
            print(f'{node.name}  Auth: {node.old_auth}  Hub: {node.old_hub}')

    def normalize_auth_hub(self):
        auth_sum = sum(node.auth for node in self.nodes)
        hub_sum = sum(node.hub for node in self.nodes)

        for node in self.nodes:
            node.auth /= auth_sum
            node.hub /= hub_sum

    def normalize_pagerank(self):
        pagerank_sum = sum(node.pagerank for node in self.nodes)

        for node in self.nodes:
            node.pagerank /= pagerank_sum

    def get_auth_hub_list(self):
        auth_list = np.asarray([node.auth for node in self.nodes], dtype='float32')
        hub_list = np.asarray([node.hub for node in self.nodes], dtype='float32')

        return np.round(auth_list, 3), np.round(hub_list, 3)

    def get_pagerank_list(self):
        pagerank_list = np.asarray([node.pagerank for node in self.nodes], dtype='float32')
        return np.round(pagerank_list, 3)


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.auth = 1.0
        self.hub = 1.0
        self.pagerank = 1.0

    def link_child(self, new_child):
        for child in self.children:
            if(child.name == new_child.name):
                return None
        self.children.append(new_child)

    def link_parent(self, new_parent):
        for parent in self.parents:
            if(parent.name == new_parent.name):
                return None
        self.parents.append(new_parent)

    def update_auth(self):
        self.auth = sum(node.hub for node in self.parents)

    def update_hub(self):
        self.hub = sum(node.auth for node in self.children)

    def update_pagerank(self, d, n):
        in_neighbors = self.parents
        pagerank_sum = sum((node.pagerank / len(node.children)) for node in in_neighbors)
        random_jumping = d / n
        self.pagerank = random_jumping + (1-d) * pagerank_sum





def ass8_main(operation,data):

    def init_graph(file):
        
        def split(line):
            str = ""
            flag = False
            for j in line:
                if not flag and j=='	':
                    str = str+','
                    flag = True
                else:
                    str = str+j
            return str.split(',')

        f = open(file)
        lines = f.readlines()

        graph = Graph()

        for line in lines: 
            [parent, child] = split(line)
                        
            graph.add_edge(parent, child)

            graph.sort_nodes()

        return graph

    if operation=="3":
        file = data

        if file:

            def PageRank_one_iter(graph, d):
                node_list = graph.nodes
                # print(node_list)
                for node in node_list:
                    node.update_pagerank(d, len(graph.nodes))
                graph.normalize_pagerank()
                # print(graph.get_pagerank_list())
                # print()


            def PageRank(iteration,graph, d):
                for i in range(int(iteration)):
                    # print(i)
                    PageRank_one_iter(graph, d)

            iteration = 100
            damping_factor = 0.15

            graph = init_graph(file)
            
            nodes = graph.nodes

            PageRank(iteration, graph, damping_factor)
            
            ranks_by_nodes = []
            page_ranks = graph.get_pagerank_list()

            for i in range(len(nodes)):
                ranks_by_nodes.append([nodes[i].name,[child.name for child in nodes[i].children],[parent.name for parent in nodes[i].parents],page_ranks[i]])
            
            
            df = pd.DataFrame(ranks_by_nodes,columns=["Node","Children","parents","Page Rank"])
            df = df.sort_values(by=["Page Rank","Node"])
            print(df)

            # table = st.table(df)

            # st.write("Total page rank sum: "+str(np.sum(graph.get_pagerank_list())))
            return (df,"Total page rank sum: " + str(np.sum(graph.get_pagerank_list())),"")
    if operation=="4":
        
        file = data

        if file:
            def HITS_one_iter(graph):
                node_list = graph.nodes

                for node in node_list:
                    node.update_auth()

                for node in node_list:
                    node.update_hub()

                graph.normalize_auth_hub()


            def HITS(graph, iteration=100):
                for i in range(iteration):
                    HITS_one_iter(graph)
                    # graph.display_hub_auth()
                    # print()


            iteration = 10

            graph = init_graph(file)

            HITS(graph,iteration)
            auth_list, hub_list = graph.get_auth_hub_list()
            
            nodes = [node.name for node in graph.nodes]

            my_data = []

            # print(hub_list)
            for i in range(len(nodes)):
                my_data.append([nodes[i],auth_list[i],hub_list[i]])

            df = pd.DataFrame(my_data,columns=["Node","Auth Value","Hub Value"])

            df = df.sort_values(["Auth Value","Hub Value"])
            # table = st.table(df)

            # print(sum(auth_list)," ",sum(hub_list))
            return (df,"Total Auth Value : " + str(sum(auth_list)),"Total Hub Value : "+str(sum(hub_list)))