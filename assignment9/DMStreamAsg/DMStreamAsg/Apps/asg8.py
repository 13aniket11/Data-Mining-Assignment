# Import libraries
from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse
import operator

import streamlit as st
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import collections
from scipy.cluster import hierarchy
from sklearn import datasets
from random import randint
import random
import plotly.express as px
import altair as alt
import seaborn as sns

def app(dataset):

    st.header("Assignment 8")
    def printf(url):
        st.markdown(f'<p style="color:#000;font:lucida;font-size:20px;">{url}</p>', unsafe_allow_html=True)

    operation = st.selectbox("Operation", ["WebCrawler",'PageRank','HITS'])
    
    if operation == "WebCrawler":
        input_url = st.text_input("Paste URL here")
        # Set for storing urls with same domain
        links_intern = set()
        # input_url = "http://www.walchandsangli.ac.in/"
        depth = st.number_input("Enter depth (less than 5)", value=1 ,max_value=5, min_value=0)
        # depth = 5

        # Set for storing urls with different domain
        links_extern = set()


        # Method for crawling a url at next level
        def level_crawler(input_url):
            temp_urls = set()
            current_url_domain = urlparse(input_url).netloc

            # Creates beautiful soup object to extract html tags
            beautiful_soup_object = BeautifulSoup(
                requests.get(input_url).content, "lxml")

            # Access all anchor tags from input
            # url page and divide them into internal
            # and external categories
            idx=0
            for anchor in beautiful_soup_object.findAll("a"):
                href = anchor.attrs.get("href")
                if(href != "" or href != None):
                    href = urljoin(input_url, href)
                    href_parsed = urlparse(href)
                    href = href_parsed.scheme
                    href += "://"
                    href += href_parsed.netloc
                    href += href_parsed.path
                    final_parsed_href = urlparse(href)
                    is_valid = bool(final_parsed_href.scheme) and bool(
                        final_parsed_href.netloc)
                    if is_valid:
                        if current_url_domain not in href and href not in links_extern:
                            idx+=1
                            st.write(f"link {idx} - {href}")
                            links_extern.add(href)
                        if current_url_domain in href and href not in links_intern:
                            idx+=1
                            st.write(f"link {idx} - {href}")
                            links_intern.add(href)
                            temp_urls.add(href)
            return temp_urls

        def crawl(input_url, depth):

            if(depth == 0):
                st.write("Page - {}".format(input_url))

            elif(depth == 1):
                level_crawler(input_url)

            else:
                # We have used a BFS approach
                # considering the structure as
                # a tree. It uses a queue based
                # approach to traverse
                # links upto a particular depth.
                queue = []
                queue.append(input_url)
                for j in range(depth):
                    st.subheader(f"Level {j} -")
                    idx=0
                    for count in range(len(queue)):
                        idx+=1
                        url = queue.pop(0)
                        printf(f"Page {idx} : {url} ")
                        urls = level_crawler(url)
                        for i in urls:
                            queue.append(i)

        if st.button("Crawl"):
            crawl(input_url, depth)
    
    if operation == "PageRank":
        st.dataframe(dataset.head(1000), width=1000, height=500)
        
        # Adjacency Matrix representation in Python


        class Graph(object):

            # Initialize the matrix
            def __init__(self, size):
                self.adjMatrix = []
                self.inbound = dict()
                self.outbound = dict()
                self.pagerank = dict()
                self.vertex = set()
                self.cnt = 0
                # for i in range(size+1):
                #     self.adjMatrix.append([0 for i in range(size+1)])
                self.size = size

            # Add edges
            def add_edge(self, v1, v2):
                if v1 == v2:
                    printf("Same vertex %d and %d" % (v1, v2))
                # self.adjMatrix[v1][v2] = 1
                self.vertex.add(v1)
                self.vertex.add(v2)
                if self.inbound.get(v2,-1) == -1:
                    self.inbound[v2] = [v1]
                else:
                    self.inbound[v2].append(v1)
                if self.outbound.get(v1,-1) == -1:
                    self.outbound[v1] = [v2]
                else:
                    self.outbound[v1].append(v2)

                
                # self.adjMatrix[v2][v1] = 1

            # Remove edges
            # def remove_edge(self, v1, v2):
            #     if self.adjMatrix[v1][v2] == 0:
            #         print("No edge between %d and %d" % (v1, v2))
            #         return
            #     self.adjMatrix[v1][v2] = 0
            #     self.adjMatrix[v2][v1] = 0

            def __len__(self):
                return self.size

            # Print the matrix
            def print_matrix(self):
                # if self.size < 1000:
                #     for row in self.adjMatrix:
                #         for val in row:
                #             printf('{:4}'.format(val), end="")
                #         printf("\n")
                #     printf("Inbound:")
                #     st.write(self.inbound)

                #     printf("Outbound:")
                #     st.write(self.outbound)
                # else:
                pass
            
            def pageRank(self):
                self.cnt = 0
                if len(self.pagerank) == 0:
                    for i in self.vertex:
                        self.pagerank[i] = 1/self.size
                prevrank = self.pagerank
                # print(self.pagerank)
                for i in self.vertex:
                    pagesum = 0.0
                    inb = self.inbound.get(i,-1)
                    if inb == -1:
                        continue
                    for j in inb:
                        pagesum += (self.pagerank[j]/len(self.outbound[j]))
                    self.pagerank[i] = pagesum
                    if (prevrank[i]-self.pagerank[i]) <= 0.1:
                        self.cnt+=1
            def printRank(self):
                printf(self.pagerank)
            def arrangeRank(self):
                sorted_rank = dict( sorted(self.pagerank.items(), key=operator.itemgetter(1),reverse=True))
                # printf(sorted_rank)
                printf("PageRank Sorted : "+str(len(sorted_rank)))
                i = 1
                printf(f"Rank ___ Node ________ PageRank Score")
                for key, rank in sorted_rank.items():
                    if i == 11:
                        break
                    printf(f"{i} _____ {key} ________ {rank}")
                    i += 1

                # st.dataframe(sorted_rank)

        def main():
            g = Graph(7)
            input_list = []
            
            d = 0.5
            for i in range(len(dataset)):
                    input_list.append([dataset.loc[i, 'fromNode'],dataset.loc[i, 'toNode']])
                    g.add_edge(dataset.loc[i, 'fromNode'],dataset.loc[i, 'toNode'])
            size = len(g.vertex)
            if size <= 10000:
                adj_matrix = np.zeros([size+1,size+1])

                for i in input_list:
                    adj_matrix[i[0]][i[1]] = 1

                st.subheader("Adjecency Matrix")
                st.dataframe(adj_matrix, width=1000, height=500)
        
                
            printf("Total Node:"+str(len(g.vertex)))
            printf("Total Edges: "+str(len(input_list)))
            # for i in input_list:

            # g.print_matrix()

            i = 0
            while i<5:
                if g.cnt == g.size:
                    break
                g.pageRank()
                i += 1
            # g.printRank()
            g.arrangeRank()

        main()

    if operation == "HITS":
        input_list = []
        
        st.subheader("Dataset")
        st.dataframe(dataset.head(1000), width=1000, height=500)
        vertex = set()
        for i in range(len(dataset)):
                input_list.append([dataset.loc[i, 'fromNode'],dataset.loc[i, 'toNode']])
                vertex.add(dataset.loc[i, 'fromNode'])
                vertex.add(dataset.loc[i, 'toNode'])
        size = len(vertex)
        adj_matrix = np.zeros([size+1,size+1])

        for i in input_list:
            adj_matrix[i[0]][i[1]] = 1
        
        printf("No of Nodes: "+str(size))
        printf("No of Edges: "+str(len(dataset)))
        st.subheader("Adjecency Matrix")
        st.dataframe(adj_matrix, width=1000, height=500)
        A = adj_matrix
        # st.dataframe(A)
        At = adj_matrix.transpose()
        st.subheader("Transpose of Adj matrix")
        st.dataframe(At)

        u = [1 for i in range(size+1)]
        printf("Hub weight matrix (U)")
        st.dataframe(u)
        # printf("Hub weight vector (V)")
        # printf(u)
        v = np.matrix([])
        for i in range(5):
            v = np.dot(At,u)
            u = np.dot(A,v)

        # u.sort(reverse=True)
        hubdict = dict()
        for i in range(len(u)):
            hubdict[i]= u[i]
        
        authdict = dict()
        for i in range(len(v)):
            authdict[i]=v[i]

        hubdict = dict( sorted(hubdict.items(), key=operator.itemgetter(1),reverse=True))
        authdict = dict( sorted(authdict.items(), key=operator.itemgetter(1),reverse=True))
        # printf(sorted_rank)
        printf("HubPages : ")
        i = 1
        printf(f"Rank ___ Node ________ Hubs score")
        for key, rank in hubdict.items():
            if i == 11:
                break
            printf(f"{i} _____ {key} ________ {rank}")
            i += 1

        printf("Authoritative Pages : ")
        i = 1
        printf(f"Rank ___ Node ________ Auth score")
        for key, rank in authdict.items():
            if i == 11:
                break
            printf(f"{i} _____ {key} ________ {rank}")
            i += 1

        # u = sorted(u, reverse=True)
        # printf("Hub weight matrix (U)")
        # st.dataframe(u)
        # v = sorted(v, reverse=True)
        # printf("Hub weight vector Authority (V)")
        # st.dataframe(v[:11])


    