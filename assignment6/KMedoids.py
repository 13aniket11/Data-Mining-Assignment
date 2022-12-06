from copy import deepcopy
from tkinter import *
import numpy as np
from tabulate import tabulate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt


def load_dataset(file: str, exclude_cols: list, exclude_rows: list, sep=','):
    data_pt = np.genfromtxt(file, delimiter=sep)

    y_true = data_pt[:, exclude_cols[0]]

    data_pt = np.delete(data_pt, obj=exclude_rows, axis=0)
    data_pt = np.delete(data_pt, obj=exclude_cols, axis=1)
    # replace nan with mean of column
    data_pt = np.where(np.isnan(data_pt), np.ma.array(data_pt, mask=np.isnan(data_pt)).mean(axis=0), data_pt)

    print(tabulate([['Dataset Size', data_pt.shape[0]], ['Instance Dimension', data_pt.shape[1]]], tablefmt='grid',
                   headers=['Dataset Summary', file]))

    return data_pt, y_true.tolist()


def get_distance(pt1: np.ndarray, pt2: np.ndarray, manhattan=True):
    if manhattan:
        return np.sum(np.abs(pt1 - pt2), axis=-1)
    return np.sqrt(np.sum((pt1 - pt2) ** 2, axis=-1))


def init_meloid(data_pt: np.ndarray, k: int):
    centroid_idx = np.random.randint(low=0, high=data_pt.shape[0] + 1, size=k)

    return centroid_idx


def get_cluster_assignment_with_cost(data: np.ndarray, k: int, medoid_idx, use_abs_error):
    medoids = data[medoid_idx]
    # print(medoids)
    dist = np.array([get_distance(data, m, use_abs_error) for m in medoids])
    cluster_assignment = np.argmin(dist, axis=0)
    # print(dist.shape)
    # print(cluster_assignment.shape)

    min_dist = dist[cluster_assignment, np.arange(dist.shape[1])]
    cost = np.sum(min_dist)
    # print(cost)
    return cluster_assignment, cost


def k_medoids(data,root):
    cols = []
    for i in data.columns[:-1]:
        cols.append(i)
    # atr1, atr2 = st.columns(2)
    Clickattribute1 = StringVar(root)
    Clickattribute1.set("Select Attribute 1")
    dropCols = OptionMenu(root, Clickattribute1,*cols)
    dropCols.place(x=30,y=60)
    Clickattribute2 = StringVar(root)
    Clickattribute2.set("Select Attribute 2")
    dropCols1 = OptionMenu(root, Clickattribute2,*cols)
    dropCols1.place(x=190,y=60)
    

    class KMedoidsClass:
        def __init__(self, data, k, iters,attribute1,attribute2):
            self.data = data
            self.k = k
            self.iters = iters
            self.medoids = np.array([data[i] for i in range(self.k)])
            self.colors = np.array(np.random.randint(
                0, 255, size=(self.k, 4)))/255
            self.colors[:, 3] = 1
            self.attribute2 = attribute2
            self.attribute1 = attribute1

        def manhattan(self, p1, p2):
            return np.abs((p1[0]-p2[0])) + np.abs((p1[1]-p2[1]))

        def get_costs(self, medoids, data):
            tmp_clusters = {i: [] for i in range(len(medoids))}
            cst = 0
            for d in data:
                dst = np.array([self.manhattan(d, md) for md in medoids])
                c = dst.argmin()
                tmp_clusters[c].append(d)
                cst += dst.min()

            tmp_clusters = {k: np.array(v)
                            for k, v in tmp_clusters.items()}
            return tmp_clusters, cst
        
        def visualization(self,root):
            colors = np.array(np.random.randint(
                0, 255, size=(self.k, 4)))/255
            colors[:, 3] = 1
            fig, ax = plt.subplots(figsize=(6, 6)) 
            plt.xlabel(self.attribute1)
            plt.ylabel(self.attribute2)
            [plt.scatter(self.clusters[t][:, 0], self.clusters[t][:, 1], marker="*", s=100,
                            color=colors[t]) for t in range(self.k)]
            plt.scatter(
                self.medoids[:, 0], self.medoids[:, 1], s=200, color=colors)
            # # plt.show()
            plt2 = FigureCanvasTkAgg(fig, root) 
            plt2.get_tk_widget().place(x=700,y=130)
        def fit(self,root):

            self.datanp = np.asarray(data)
            samples, _ = self.datanp.shape

            self.clusters, cost = self.get_costs(
                data=self.data, medoids=self.medoids)
            count = 0

            colors = np.array(np.random.randint(
                0, 255, size=(self.k, 4)))/255
            colors[:, 3] = 1

            fig, ax = plt.subplots(figsize=(6, 6)) 
            plt.xlabel(self.attribute1)
            plt.ylabel(self.attribute2)
            [plt.scatter(self.clusters[t][:, 0], self.clusters[t][:, 1], marker="*", s=100,
                            color=colors[t]) for t in range(self.k)]
            plt.scatter(self.medoids[:, 0],
                        self.medoids[:, 1], s=200, color=colors)
            # # plt.show()
            # st.pyplot()
            plt1 = FigureCanvasTkAgg(fig, root) 
            plt1.get_tk_widget().place(x=30,y=130)

            while True:
                swap = False
                for i in range(samples):
                    if not i in self.medoids:
                        for j in range(self.k):
                            tmp_meds = self.medoids.copy()
                            tmp_meds[j] = i
                            clusters_, cost_ = self.get_costs(
                                data=self.data, medoids=tmp_meds)

                            if cost_ < cost:
                                self.medoids = tmp_meds
                                cost = cost_
                                swap = True
                                self.clusters = clusters_
                                print("Medoids Changed to: ",self.medoids)
                                self.visualization(root)
                                # st.write(
                                #     f"Medoids Changed to: {self.medoids}.")
                                # st.subheader(f"Step :{count+1}")
                                # count += 1
                                
                                
                count += 1

                if count >= self.iters:
                    print("End of the iterations.")
                    break
                if not swap:
                    print("End")
                    break
    datat = []
    label=Label(root, text="Enter value fot k", font=("Helvetica",12))
    label.place(x=30,y=30)
    entry= Entry(root, width= 40)
    entry.focus_set()
    entry.place(x=230,y=30)
    

    Button(root,text="Measure",command= lambda:helper()).place(x=30,y=90)

    def helper():
        attribute1 = Clickattribute1.get()
        attribute2 = Clickattribute2.get()
        k = entry.get()
        arr1 = []
        arr2 = []
        for i in range(len(data)):
            arr1.append(data.loc[i, attribute1])
        for i in range(len(data)):
            arr2.append(data.loc[i, attribute2])
        for i in range(len(arr1)):
            tmp = []
            tmp.append(arr1[i])
            tmp.append(arr2[i])
            datat.append(tmp)
        kmedoid = KMedoidsClass(datat, int(k), 10,attribute1,attribute2)
        kmedoid.fit(root)
