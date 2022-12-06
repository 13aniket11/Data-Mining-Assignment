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





def view_dtc(root,file_name):
    newfilename = ''
    for i in file_name:
        if i == "/":
            newfilename = newfilename + "/"
            newfilename = newfilename + i
    data = pd.read_csv(file_name)
    d = pd.read_csv(file_name)
    cols = []
    for i in data.columns:
        cols.append(i)

    
    clickedAttribute2 = StringVar(root)
    clickedAttribute2.set("Select Class/Target")
    dropMCT = OptionMenu(root, clickedAttribute2, *cols)
    dropMCT.place(x=0,y=0)

    Button(root,text="Measure",command= lambda:view1(clickedAttribute2.get(),data,root)).place(x=160,y=0)

def view1(targetAttr,df,root):
    colums=df.columns

    data=df
    features = list(colums)
    features.remove(targetAttr)

    def entropy(labels):
        entropy=0
        label_counts = Counter(labels)
        for label in label_counts:
            prob_of_label = label_counts[label] / len(labels)
            entropy -= prob_of_label * math.log2(prob_of_label)
        return entropy

    def information_gain(starting_labels, split_labels):
        info_gain = entropy(starting_labels)
        ans=0
        for branched_subset in split_labels:
            ans+=len(branched_subset) * entropy(branched_subset) / len(starting_labels)
        Label(root,text="Entropy : "+str(round(ans,3)),fg='red',font=("Helvetica",12)).place(x=10,y=60)
        info_gain-=ans
        return info_gain

    def split(dataset, column):
        split_data = []
        col_vals = data[column].unique()
        for col_val in col_vals:
            split_data.append(dataset[dataset[column] == col_val])
        return(split_data)

    def find_best_split(dataset):
        best_gain = 0
        best_feature = 0
        # Label(root,text="Overall Entropy : "+str(entropy(dataset[targetAttr])),fg='red',font=("Helvetica",12)).place(x=30,y=160)
        for feature in features:
            split_data = split(dataset, feature)
            split_labels = [dataframe[targetAttr] for dataframe in split_data]
            gain = information_gain(dataset[targetAttr], split_labels)
            print(gain)
            if gain > best_gain:
                best_gain, best_feature = gain, feature
        Label(root,text="Gain : "+str(best_gain),fg='red',font=("Helvetica",12)).place(x=10,y=90)
        return best_feature, best_gain

    new_data = split(data, find_best_split(data)[0]) 

    # print(new_data)

    features = list(colums)
    features.remove(targetAttr)
    x = df[features]
    y = df[targetAttr] 

    dataEncoder = preprocessing.LabelEncoder()
    encoded_x_data = x.apply(dataEncoder.fit_transform)

    Label(root,text="Information Gain : ",font=("Helvetica",12)).place(x=330,y=10)

    decision_tree = DecisionTreeClassifier(criterion="entropy")
    decision_tree = decision_tree.fit(encoded_x_data, y)
    
    fig, ax = plt.subplots(figsize=(3.5, 3.5)) 
    tree.plot_tree(decision_tree,ax=ax,feature_names=features)
    plt1 = FigureCanvasTkAgg(fig, root) 
    plt1.get_tk_widget().place(x=330,y=30)

    Label(root,text="Gini Index : ",font=("Helvetica",12)).place(x=660,y=10)

    decision_tree = DecisionTreeClassifier(criterion="gini")
    decision_tree = decision_tree.fit(encoded_x_data, y)
    
    fig, ax = plt.subplots(figsize=(3.5, 3.5)) 
    tree.plot_tree(decision_tree,ax=ax,feature_names=features)
    plt2 = FigureCanvasTkAgg(fig, root) 
    plt2.get_tk_widget().place(x=660,y=30)


    X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=1)

    clf = DecisionTreeClassifier(max_depth=2, random_state=1)

    clf = clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    c_matrix = confusion_matrix(y_test, y_pred)

    pddf = pd.DataFrame(c_matrix)
    blankIndex = ['']*len(pddf)
    pddf.index=blankIndex
    pddf.columns = blankIndex

    Label(root,text="Confusion Matrix:"+str(pddf),fg='red',font=("Helvetica",12)).place(x=10,y=220)

    Label(root,text="Model Accuracy: "+str(metrics.accuracy_score(y_test, y_pred)),fg='red',font=("Helvetica",12)).place(x=10,y=120)

    val = metrics.precision_score(y_test, y_pred, average='macro')
    # print('Precision score : ' + str(val))
    Label(root,text="Precision score : "+str(val),fg='red',font=("Helvetica",12)).place(x=10,y=150)


    val = metrics.accuracy_score(y_test, y_pred)
    Label(root,text="Accuracy score : "+str(val),fg='red',font=("Helvetica",12)).place(x=10,y=180)
   
    #Assignment 4
    # get the text representation
    text_representation = tree.export_text(clf,feature_names=features)
    print(text_representation)


    def tree_to_code(tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        feature_names = [f.replace(" ", "_")[:-5] for f in feature_names]
        print(feature_names)
        def recurse(node, depth):
            indent = "    " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                print(indent, name, np.round(threshold,2))
                recurse(tree_.children_left[node], depth + 1)
                print(indent, name, np.round(threshold,2))
                recurse(tree_.children_right[node], depth + 1)
            else:
                print(indent, tree_.value[node])
        recurse(0, 1)
    
    tree_to_code(decision_tree,features)


def view(attr2,data,root):
    # data = 'D:/College/BTech/SEM 7/Data Mining/DataSet/Iris.csv'
    df = data
    # print(df.shape)
    # print("---------------------")
    # print(df.head())
    cols = []
    col2 = []
    for i in df.columns:
        cols.append(i)
        if(i != attr2):
            col2.append(i)

    # print(col2)

    x = df.drop([attr2], axis=1)
    y = df[attr2]
    # print(x,y)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.33, random_state = 42)

    encoder = ce.OrdinalEncoder(cols=col2)


    X_train = encoder.fit_transform(X_train)

    X_test = encoder.transform(X_test)

    clf_gini = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=0)
    clf_gini.fit(X_train, y_train)
    y_pred_gini = clf_gini.predict(X_test)
    print(y_pred_gini)

    print('Model accuracy score with criterion gini index: {0:0.4f}'. format(accuracy_score(y_test, y_pred_gini)))
    

    clf_en = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)


    # fit the model
    clf_en.fit(X_train, y_train)

    y_pred_en = clf_en.predict(X_test)
    print('Model accuracy score with criterion entropy: {0:0.4f}'. format(accuracy_score(y_test, y_pred_en)))
    y_pred_train_en = clf_en.predict(X_train)
    fig = plt.figure(figsize=(6,5))
    tree.plot_tree(clf_en.fit(X_train, y_train))
    # plt.show()
    scatter3 = FigureCanvasTkAgg(fig, root) 
    scatter3.get_tk_widget().place(x=450,y=60)

    cm = confusion_matrix(y_test, y_pred_en)

    print('Confusion matrix\n\n', cm)


    # Label(root,text="Information Gain : "+str(round(info_gain,3)),fg='red',font=("Helvetica",12)).place(x=30,y=160)
    # Label(root,text="Gini Index : "+str(round(gini_index,3)),fg='red',font=("Helvetica",12)).place(x=30,y=180)
    # Label(root,text="Gini Ratio : "+str(round(gini_ratio,3)),fg='red',font=("Helvetica",12)).place(x=170,y=180)
    
    return (accuracy_score(y_test, y_pred_gini),accuracy_score(y_test, y_pred_en),cm)
