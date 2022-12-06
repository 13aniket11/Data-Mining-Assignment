import numpy.random as random
from numpy.core.fromnumeric import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn import datasets
from scipy.cluster.hierarchy import dendrogram, linkage
import pylab as pl
import math
from random import randint



def calDist(X1, X2):
    sum = 0
    for x1, x2 in zip(X1, X2):
        sum += (x1 - x2) ** 2
    return sum ** 0.5
    return (((X1[0]-X2[0])**2)+(X1[1]-X2[1])**2)**0.5

def getNeibor(data, dataSet, e):
    res = []
    for i in range(len(dataSet)):
        if calDist(data, dataSet[i]) < e:
            res.append(i)
    return res

def DBSCAN(dataSet, e, minPts):
    coreObjs = {}
    C = {}
    for i in range(len(dataSet)):
        neibor = getNeibor(dataSet[i], dataSet, e)
        if len(neibor) >= minPts:
            coreObjs[i] = neibor
    oldCoreObjs = coreObjs.copy()
    # st.write(oldCoreObjs)
    # CoreObjs set of COres points
    k = 0
    notAccess = list(range(len(dataSet)))

    # his will check the relation of core point with each other
    while len(coreObjs) > 0:
        OldNotAccess = []
        OldNotAccess.extend(notAccess)
        cores = coreObjs.keys()
        randNum = random.randint(0, len(cores))
        cores = list(cores)
        core = cores[randNum]
        queue = []
        queue.append(core)
        notAccess.remove(core)
        while len(queue) > 0:
            q = queue[0]
            del queue[0]
            if q in oldCoreObjs.keys():
                delte = [val for val in oldCoreObjs[q]
                            if val in notAccess]
                queue.extend(delte)
                notAccess = [
                    val for val in notAccess if val not in delte]
        k += 1
        C[k] = [val for val in OldNotAccess if val not in notAccess]
        for x in C[k]:
            if x in coreObjs.keys():
                del coreObjs[x]
    # st.write(C)
    print(C)
    return C

def draw(C, dataSet,attribute1,attribute2,root):
    color = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
    vis = set()
    for i in C.keys():
        X = []
        Y = []
        datas = C[i]
        for k in datas:
            vis.add(k)
        for j in range(len(datas)):
            X.append(dataSet[datas[j]][0])
            Y.append(dataSet[datas[j]][1])
        plt.scatter(X, Y, marker='o',
                    color=color[i % len(color)], label=i)
    vis = list(vis)
    unvis1 = []
    unvis2 = []
    for i in range(len(dataSet)):
        if i not in vis:
            unvis1.append(dataSet[i][0])
            unvis2.append(dataSet[i][1])
    fig, ax = plt.subplots(figsize=(6, 6)) 
    plt.xlabel(attribute1)
    plt.ylabel(attribute2)
    plt.scatter(unvis1, unvis2, marker='o', color='black')
    plt.legend(loc='lower right')
    plt1 = FigureCanvasTkAgg(fig, root) 
    plt1.get_tk_widget().place(x=30,y=130)
    # plt.show()
    # st.pyplot()

def main_dbscan(data,root):

    cols = []

    for i in data.columns[:-1]:
        cols.append(i)
    # atr1, atr2 = st.columns(2)
    Clickattribute1 = StringVar(root)
    Clickattribute1.set("Select Attribute 1")
    dropCols = OptionMenu(root, Clickattribute1,*cols)
    dropCols.place(x=30,y=90)
    Clickattribute2 = StringVar(root)
    Clickattribute2.set("Select Attribute 2")
    dropCols1 = OptionMenu(root, Clickattribute2,*cols)
    dropCols1.place(x=190,y=90)

    dataset = []
    arr1 = []
    arr2 = []

    label=Label(root, text="Insert value for eps", font=("Helvetica",12))
    label.place(x=30,y=30)
    entry= Entry(root, width= 40)
    entry.focus_set()
    entry.place(x=230,y=30)
    
    label1=Label(root, text="Insert mimimum number of points in cluster", font=("Helvetica",12))
    label1.place(x=30,y=60)
    entry1= Entry(root, width= 40)
    entry1.focus_set()
    entry1.place(x=230,y=60)
    
    
    def helper():
        attribute1 = Clickattribute1.get()
        attribute2 = Clickattribute2.get()

        for i in range(len(data)):
            arr1.append(data.loc[i, attribute1])
        for i in range(len(data)):
            arr2.append(data.loc[i, attribute2])
        for i in range(len(arr1)):
            tmp = []
            tmp.append(arr1[i])
            tmp.append(arr2[i])
            dataset.append(tmp)
        r = int(entry.get())
        mnp = int(entry1.get())
        C = DBSCAN(dataset, r, mnp)
        draw(C, dataset,attribute1,attribute2,root)    
    
    Button(root,text="Measure",command= lambda:helper()).place(x=30,y=130)


def main_asgens(data,root):
    iris = datasets.load_iris()
    cols = []
    for i in data.columns[:-1]:
        cols.append(i)

    Clickattribute1 = StringVar(root)
    Clickattribute1.set("Select Attribute 1")
    dropCols = OptionMenu(root, Clickattribute1,*cols)
    dropCols.place(x=30,y=90)
    Clickattribute2 = StringVar(root)
    Clickattribute2.set("Select Attribute 2")
    dropCols1 = OptionMenu(root, Clickattribute2,*cols)
    dropCols1.place(x=190,y=90)

    label=Label(root, text="Insert value for K", font=("Helvetica",12))
    label.place(x=30,y=30)
    entry= Entry(root, width= 40)
    entry.focus_set()
    entry.place(x=230,y=30)

    dataset = []
    arr1 = []
    arr2 = []
    

    def dist(a, b):
        return math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2))


    def dist_avg(Ci, Cj):
        return sum(dist(i, j) for i in Ci for j in Cj)/(len(Ci)*len(Cj))

    def find_Min(M):
        min = 1000
        x = 0
        y = 0
        for i in range(len(M)):
            for j in range(len(M[i])):
                if i != j and M[i][j] < min:
                    min = M[i][j]
                    x = i; 
                    y = j
        return (x, y, min)

    def AGNES(dataset, dist, k):
        C = []
        M = []
        for i in dataset:
            Ci = []
            Ci.append(i)
            C.append(Ci)
#     print(C)
        for i in C:
            Mi = []
            for j in C:
#             print(Mi)
                Mi.append(dist(i, j))
            M.append(Mi)
#     print(len(M))
        q = len(dataset)
#     print(q)
        while q > k:
            x, y, min = find_Min(M)
#         print(find_Min(M))
            C[x].extend(C[y])
            C.remove(C[y])
            M = []
            for i in C:
                Mi = []
                for j in C:
                    Mi.append(dist(i, j))
                M.append(Mi)
            q -= 1
        return C
    def draw(C):
        attribute1 = Clickattribute1.get()
        attribute2 = Clickattribute2.get()
        fig, ax = plt.subplots(figsize=(6, 6)) 
        # st.subheader("Plot of cluster using AGNES")
        colValue = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
        c = ["Setosa","Versicolor","Virginica"]
        for i in range(len(C)):
            coo_X = []    
            coo_Y = []    
            for j in range(len(C[i])):
                coo_X.append(C[i][j][0])
                coo_Y.append(C[i][j][1])
            pl.xlabel(attribute1)
            pl.ylabel(attribute2)
            # pl.scatter(coo_X, coo_Y, marker='x', color=colValue[i%len(colValue)], label=i)
            pl.scatter(coo_X, coo_Y, color=colValue[i%len(colValue)], label=i)

        pl.legend(loc='upper right')
        # pl.show()
        plt2 = FigureCanvasTkAgg(fig, root) 
        plt2.get_tk_widget().place(x=700,y=170)
        # st.pyplot()

    def helper():
        attribute1 = Clickattribute1.get()
        attribute2 = Clickattribute2.get()
        n = int(entry.get())
        for i in range(len(data)):
                arr1.append(data.loc[i, attribute1])
        for i in range(len(data)):
                arr2.append(data.loc[i, attribute2])
        for i in range(len(arr1)):
            tmp = []
            tmp.append(arr1[i])
            tmp.append(arr2[i])
            dataset.append(tmp)
        # st.write(dataset)
        C = AGNES(dataset, dist_avg,n)
        draw(C)
        dist_sin = linkage(iris.data, method="ward")

        fig, ax = plt.subplots(figsize=(6, 6)) 
        plt.figure(figsize=(20,15))
        dendrogram(dist_sin, above_threshold_color='#070dde',orientation='right',leaf_rotation=90,ax=ax)
        plt.xlabel('Distance')
        plt.ylabel('Index')
        plt.title("Dendrogram plot", fontsize=18)
        plt1 = FigureCanvasTkAgg(fig, root) 
        plt1.get_tk_widget().place(x=30,y=170)
        # plt.show()
        # st.pyplot()
    Button(root,text="Measure",command= lambda:helper()).place(x=30,y=130)


def main_diana(data,root):
    iris = datasets.load_iris()
    arr = []
    n=0

    cols = []
    for i in data.columns[:-1]:
        cols.append(i)
    Clickattribute1 = StringVar(root)
    Clickattribute1.set("Select Attribute 1")
    dropCols = OptionMenu(root, Clickattribute1,*cols)
    dropCols.place(x=30,y=90)
    Clickattribute2 = StringVar(root)
    Clickattribute2.set("Select Attribute 2")
    dropCols1 = OptionMenu(root, Clickattribute2,*cols)
    dropCols1.place(x=190,y=90)

    label=Label(root, text="Enter no of Clusters (k): ", font=("Helvetica",12))
    label.place(x=30,y=30)
    entry= Entry(root, width= 40)
    entry.focus_set()
    entry.place(x=230,y=30)

    def helper():
        attribute1 = Clickattribute1.get()
        attribute2 = Clickattribute2.get()
        k = int(entry.get())
        for i in range(len(data)):
                arr.append([data.loc[i, attribute1],data.loc[i, attribute2]])
        
        # arr = []
        # n=0
        # for i in X:
        #   arr.append([i[0],i[1]])
        #   n += 1

        # print(X)
        # print("------------")
        # print(arr[0], arr[1])
        # print("------------")
        # print(atr2)




        # arr = np.array([[1, 2],[3,2],[2,5],[1,3],[6,5],[7,5],[4,6],[3,5],[4,1],[5,6],[3,8],[8,5]])
        # k = 3
        minPoints = 0
        if len(arr)%k==0:
            minPoints=len(arr)//k
        else:
            minPoints = (len(arr)//k)+1
        # print(len(arr))
        print(minPoints)

        def Euclid(a,b):
            # print(a,b)
        # finding sum of squares
            sum_sq = np.sum(np.square(a - b))
            return np.sqrt(sum_sq)



        points=[[0]]
        def findPoints(point):
            max = 0
            pt=-1
            for i  in point:
                for j in range(len(arr)):
                    if j in point:
                        continue
                    else:
                    # print(arr[i], arr[j])
                        dis = Euclid(np.array(arr[i]),np.array(arr[j]))
                        if max < dis:
                            max = dis
                            # print(max)
                            pt=j
            return pt

        travetsedPoints=[0]
        for i in range(0,k):
            if len(travetsedPoints) >= len(arr):
                break
            
            # if len(points)>=k:
            #   break

            while(len(points[i])<minPoints):
            # while(True):
                pt = findPoints(travetsedPoints)
                if pt in travetsedPoints:
                    break
                travetsedPoints.append(pt)
                points[i].append(pt)
            points.append([])
        points.remove([])
        # st.write(points)



        # colarr = ['blue','green','red','black']

        colarr = []

        for i in range(k):
            colarr.append('#%06X' % randint(0, 0xFFFFFF))

        i=0
        cluster=[]
        for j in range(k):
            cluster.append(j)

        # st.subheader("Cluster and Points")
        # # annotations=["Point-1","Point-2","Point-3","Point-4","Point-5"]
        # fig, axes = plt.subplots(1, figsize=(15, 20))
        # for atr in points:
        #     for j in range(minPoints):
        #         if atr[j]==-1:
        #             continue
        #     pltY = atr[j]
        #     pltX = cluster[i%(k+1)]
        #     # pltX = arr[atr[j]][0]
        #     # pltY = arr[atr[j]][1]
        #     # pltY = data.loc[:,classatr]
        #     plt.scatter(pltX, pltY, color=colarr[i])
        #     label = str("(" + str(arr[atr[j]][0]) + "," + str(arr[atr[j]][1]) + ")")
        #     plt.text(pltX, pltY, label)

        #     i += 1

        # plt.legend(loc=1, prop={'size':4})
        # # plt.show()
        # st.pyplot()

        j=0
        def findIndex(ptarr):
            # print("Ptarr: ", ptarr)
            for j in range(len(points)):
                if ptarr in points[j]:
                    return j
            
        fig, axes = plt.subplots(1, figsize=(6, 6))
        clusters=[]
        for i in range(k):
            clusters.append([[],[]])

        for i in range(len(arr)):
            j = findIndex(i)
            clusters[j%k][0].append(arr[i][0])
            clusters[j%k][1].append(arr[i][1])

            # print(i)
            # plt.scatter(arr[i][0],arr[i][1], color = colarr[j])
        for i in range(len(clusters)):
            plt.scatter(clusters[i][0],clusters[i][1], color = colarr[i%k], label=cluster[i])
        plt.title("Cluster plot using DIANA")
        plt.xlabel(attribute2)
        plt.ylabel(attribute1)
        plt.legend(loc=1, prop={'size':15})
        plt1 = FigureCanvasTkAgg(fig, root) 
        plt1.get_tk_widget().place(x=30,y=170)
        # plt.legend(["x*2" , "x*3"])
        # plt.show()
        # st.subheader("Clustering using DIANA")
        # st.pyplot()

        # st.write("Dendogram")
        # dismatrix =[]
        # for i in range(len(arr)):
        #     for j in range(i+1, len(arr)):
        #         dismatrix.append([Euclid(np.array(arr[i]),np.array(arr[j]))])
            # print(arr[i], arr[j])
            # print(arr[j])
        # ytdist = dismatrix
        # st.subheader("Dendogram plot")
        # st.dataframe(iris.data)
        dist_sin = linkage(iris.data, method="ward")
        fig1, ax = plt.subplots(figsize=(5, 6)) 
        # plt.clf()
        plt.figure(figsize=(20,15))
        dendrogram(dist_sin, above_threshold_color='#070dde',orientation='left',leaf_rotation=90,ax=ax)
        plt.xlabel('Distance')
        plt.ylabel('Index')
        plt.title("Dendrogram plot", fontsize=18)
        plt1 = FigureCanvasTkAgg(fig1, root) 
        plt1.get_tk_widget().place(x=700,y=170)
        # plt.show()
        # st.pyplot()
    Button(root,text="Measure",command= lambda:helper()).place(x=30,y=130)
