import pandas as pd
import operator
import numpy as np  
from sklearn.neighbors import KNeighborsClassifier

# def open_file():
#     file = filedialog.askopenfilename(parent=root,initialdir="D:/College/BTech/SEM 7/Data Mining/DataSet/",title="Select Dataset File", filetypes=[("CSV files", "*.csv*"), ("all files", "*.*")])
#     print(file)    
def calDist(d1, d2, length):
    distance = 0
    for x in range(length):
        distance += np.square(d1[x] - d2[x])
       
    return np.sqrt(distance)


def knn(data,test,k):
    dist = {}
    length = test.shape[1]
    # print(length)

    for i in range(len(data)):    
        cal_dist = calDist(test,data.iloc[i],length)
        dist[i] = cal_dist[0]
    
    sort_d = sorted(dist.items(),key=operator.itemgetter(1))

    nn = []
    for i in range(k):
        nn.append(sort_d[i][0])

    class_list = data['Species'].unique()
    class_dict = {}
    for i in range(len(class_list)):
        class_dict[class_list[i]] = 0

    # print(class_dict)
    for i in range(len(nn)):
        response = data.iloc[nn[i]][-1]
 
        if response in class_dict:
            class_dict[response] += 1
        else:
            class_dict[response] = 1  

    sortedVotes = sorted(class_dict.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedVotes)
    return (sortedVotes[0][0],nn)

def buit_in_function(data):
    x=data.iloc[:,:4]
    y=data['Species']
    neigh=KNeighborsClassifier(n_neighbors=4)
    neigh.fit(data.iloc[:,:4],data["Species"])
    

def main():
    file_name="D:/College/BTech/SEM 7/Data Mining/DataSet/Iris.csv"
    data = pd.read_csv(file_name)
    print(data)
    testSet = [[2.4, 3.6, 4.4]]
    k = int(input())
    test = pd.DataFrame(testSet)
    nn = knn(data, test,k)
    print(nn)

    

    # print(type(data))


if __name__ == "__main__":
    main()


# upload data
# split into test and train
# 
