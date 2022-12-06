import pandas as pd  
import numpy as np  
import math
from tkinter import *
import category_encoders as ce
import matplotlib.pyplot as plt # data visualization
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import *
from sklearn.metrics import classification_report
from collections import Counter
import pandas as pd  
import numpy as np
from sklearn import tree
from sklearn.tree import _tree
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def entropy(target):
    elm,counts = np.unique(target,return_counts=True)
    tot_counts = np.sum(counts)
    entropy = 0
    for i in range(len(elm)):
        prob = (counts[i]/tot_counts)
        entropy += (-prob*np.log2(prob))
    return entropy

def infoGain(data,split_attribute,target):
    tot_entropy = entropy(data[target])

    vals,counts= np.unique(data[split_attribute],return_counts=True)  
    weight_entropy = 0

    for i in range(len(vals)):
        weight_entropy += ((counts[i]*np.sum(counts[i])) * entropy(data.where(data[split_attribute]==vals[i]).dropna()[target]))

    information_Gain = tot_entropy - weight_entropy
    return information_Gain

def split_info(split_attribute):
    elm,counts = np.unique(split_attribute,return_counts=True)
    tot_counts = np.sum(counts)
    splitinfo = 0
    for i in range(len(elm)):
        prob = (abs(counts[i])/abs(tot_counts))
        splitinfo += (-prob*np.log2(prob))
    return splitinfo

def gini(target):
    elm,counts = np.unique(target,return_counts=True)
    tot_counts = np.sum(counts)
    gini = 0
    for i in range(len(elm)):
        prob = (counts[i]/tot_counts)
        gini += prob**2
    print(gini)
    return (1-gini)

def train_using_gini(X_train, X_test, y_train):
	clf_gini = DecisionTreeClassifier(criterion = "gini",
			random_state = 100,max_depth=3, min_samples_leaf=5)

	clf_gini.fit(X_train, y_train)
	return clf_gini
	
def tarin_using_entropy(X_train, X_test, y_train):

	clf_entropy = DecisionTreeClassifier(
			criterion = "entropy", random_state = 100,
			max_depth = 3, min_samples_leaf = 5)

	clf_entropy.fit(X_train, y_train)
	return clf_entropy

def splitdataset(data,target):
  
    # Separating the target variable
    X = data.values[:, data.columns!=target]
    Y = data[target]
    print(Y)
    print("===========================")
    print(X)
    print("===========================")

    X_train, X_test, y_train, y_test = train_test_split( 
    X, Y, test_size = 0.3, random_state = 100)
    return X, Y, X_train, X_test, y_train, y_test


def prediction(X_test, clf_object):
	y_pred = clf_object.predict(X_test)
	print("Predicted values:")
	print(y_pred)
	return y_pred


def show(split_attribute,target,data):
    X, Y, X_train, X_test, y_train, y_test = splitdataset(data,target)
    _gini = train_using_gini(X_train, X_test, y_train)
    entropy_ = tarin_using_entropy(X_train, X_test, y_train)
    y_pred_gini = prediction(X_test, _gini)
    dict_rep = classification_report(y_test, y_pred_gini,output_dict=True)
    del dict_rep['accuracy']
    del dict_rep['macro avg']
    del dict_rep['weighted avg']
    for key,indict in dict_rep.items():
        del indict['support']
        del indict['f1-score']
        dict_rep[key] = indict

    info_gain = infoGain(data,split_attribute,target)
    print("info gain:",info_gain)
    gini_index = gini(data[target])
    print("gini index:",gini_index)
    gini_ratio = (info_gain / split_info(data[split_attribute]))
    print("gini ratio:",gini_ratio)

    pddf = pd.DataFrame(confusion_matrix(y_test, y_pred_gini))
    blankIndex = ['']*len(pddf)
    pddf.index=blankIndex
    pddf.columns = blankIndex
    return (round(info_gain,3),round(gini_ratio,3),round(gini_index,3),str(pddf),str(pd.DataFrame(dict_rep)))
    # Label(root,text="Information Gain : "+str(round(info_gain,3)),fg='red',font=("Helvetica",12)).place(x=30,y=160)
    # Label(root,text="Gini Index : "+str(round(gini_index,3)),fg='red',font=("Helvetica",12)).place(x=30,y=180)
    # Label(root,text="Gini Ratio : "+str(round(gini_ratio,3)),fg='red',font=("Helvetica",12)).place(x=170,y=180)
    # Label(root,text="Confusion Matrix : "+str(pddf),fg='red',font=("Helvetica",12)).place(x=350,y=140)
    # # Label(root,text=,fg='red',font=("Helvetica",12)).place(x=270,y=110)
    # Label(root,text="Report : "+str(pd.DataFrame(dict_rep)),fg='blue',font=("Helvetica",12)).place(x=30,y=210)
    # Label(root,text="Reprt : "+str(confusion_matrix(y_test, y_pred_gini)),fg='red',font=("Helvetica",12)).place(x=90,y=150)

