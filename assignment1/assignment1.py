import tkinter
from tkinter import *
from tkinter import filedialog,ttk
import csv
import math
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


# root = tkinter.Tk()
# selected_value = StringVar()

def open_file(root):
    # root = tkinter.Tk()
    file = filedialog.askopenfilename(parent=root,initialdir="D:/College/BTech/SEM 7/Data Mining/DataSet/",title="Select Dataset File", filetypes=[("CSV files", "*.csv*"), ("all files", "*.*")])
    print(file)
    return file

def display_file(file_name):
    with open(file_name,newline="") as file:
        reader = csv.reader(file)
        # print(reader)
        root1 = tkinter.Tk()

        # for scroll 
        h = Scrollbar(root1,orient="horizontal")
        v= Scrollbar(root1,orient="vertical")
        
        # h.pack(side=BOTTOM,fill=X)
        # v.pack(side=RIGHT,fill=Y)

        row_no = 0
        for col in reader:
            col_no =0
            for row in col:
                label = tkinter.Label(root1,width=10,height=2,text=row,relief=tkinter.RIDGE)
                
                label.grid(row=row_no,column=col_no)
                col_no = col_no+1
            row_no = row_no+1

        # v.config(command=)
def measureOfCentralT(clickedAttribute,root2,clickedMCT,data):
    attribute = clickedAttribute.get()
    operation = clickedMCT.get()
    if operation == "Mean":
        sum = 0
        for i in range(len(data)):
            sum += data.loc[i, attribute]
        avg = sum/len(data)
        res = "Mean of given dataset is ("+attribute+") "+str(avg)
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
    elif operation == "Mode": 
        freq = {}
        for i in range(len(data)):
            freq[data.loc[i, attribute]] = 0
        maxFreq = 0
        maxFreqElem = 0
        for i in range(len(data)):
            freq[data.loc[i, attribute]] = freq[data.loc[i, attribute]]+1
            if freq[data.loc[i, attribute]] > maxFreq:
                maxFreq = freq[data.loc[i, attribute]]
                maxFreqElem = data.loc[i, attribute]
        res = "Mode of given dataset is ("+attribute+") "+str(maxFreqElem)
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
    elif operation == "Median":
        n = len(data)
        i = int(n/2)
        j = int((n/2)-1)
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        if n%2 == 1:
            res = "Median of given dataset is ("+attribute+") "+str(arr[i])
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
        else:
            res = "Median of given dataset is ("+attribute+") "+str((arr[i]+arr[j])/2)
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
    elif operation == "Midrange":
        n = len(data)
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        res = "Midrange of given dataset is ("+attribute+") "+str((arr[n-1]+arr[0])/2)
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
    elif operation == "Variance" or operation == "Standard Deviation":
        sum = 0
        for i in range(len(data)):
            sum += data.loc[i, attribute]
        avg = sum/len(data)
        sum = 0
        for i in range(len(data)):
            sum += (data.loc[i, attribute]-avg)*(data.loc[i, attribute]-avg)
        var = sum/(len(data))
        if operation == "Variance":
            res = "Variance of given dataset is ("+attribute+") "+str(var)
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
        else:
            res = "Standard Deviation of given dataset is ("+attribute+") "+str(math.sqrt(var)) 
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)  
                        
def computeOperation(clickedAttribute,clickedDispersion,data,root2):
    attribute = clickedAttribute.get()
    operation = clickedDispersion.get()
    if operation == "Range":
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        res = "Range of given dataset is ("+attribute+") "+str(arr[len(data)-1]-arr[0])
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
    elif operation == "Quartiles" or operation == "Inetrquartile range": 
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        if operation == "Quartiles": 
            res1 = "Lower quartile(Q1) is ("+attribute+") "+str((len(arr)+1)/4)
            res2 = "Middle quartile(Q2) is ("+attribute+") "+str((len(arr)+1)/2)
            res3 = "Upper quartile(Q3) is ("+attribute+") "+str(3*(len(arr)+1)/4)
            Label(root2,text=res1,width=80,height=3,fg='green').grid(column=1,row=8)
            Label(root2,text=res2,width=80,height=3,fg='green').grid(column=1,row=8)
            Label(root2,text=res3,width=80,height=3,fg='green').grid(column=1,row=9)
        else:
            res = "Interquartile range(Q3-Q1) of given dataset is ("+attribute+") "+str((3*(len(arr)+1)/4)-((len(arr)+1)/4))
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
            
    elif operation == "Minimum" or operation == "Maximum":
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        if operation == "Minimum":
            res = "Minimum value of given dataset is ("+attribute+") "+str(arr[0])
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
        else:
            res = "Maximum value of given dataset is ("+attribute+") "+str(arr[len(data)-1])
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)

def plt_chart(clickedAttribute1,clickedPlot,clickedAttribute2,data,clickedClass,root2):
    attribute1 = clickedAttribute1.get()
    attribute2 = clickedAttribute2.get()
    fig, ax = plt.subplots(figsize=(4, 4)) 
    operation = clickedPlot
    if operation == "Quantile-Quantile Plot": 
        # fig, ax = plt.subplots(figsize=(4, 4)) 
        arr = []
        sum = 0
        for i in range(len(data)):
            arr.append(data.loc[i, attribute1])  
            sum += data.loc[i, attribute1]
        avg = sum/len(arr)
        sum = 0
        for i in range(len(data)):
            sum += (data.loc[i, attribute1]-avg)*(data.loc[i, attribute1]-avg)
        var = sum/(len(data))
        sd = math.sqrt(var)
        z = (arr-avg)/sd

        stats.probplot(z, dist="norm", plot=plt)
        plt.title("Normal Q-Q plot")
        plt2 = FigureCanvasTkAgg(fig, root2) 
        plt2.draw()
        # toolbar = NavigationToolbar2Tk(plt2,root2)
        # toolbar.update()
        plt2.get_tk_widget().place(x=20,y=90)
        # plt.show()
        
    elif operation == "Histogram": 
        # fig, ax = plt.subplots(figsize=(4, 4)) 
        sns.set_style("whitegrid")
        sns.FacetGrid(data, hue=clickedClass.get(), height=5).map(sns.histplot, attribute1).add_legend()
        plt.title("Histogram")
        plt2 = FigureCanvasTkAgg(fig, root2) 
        plt2.draw()
        # toolbar = NavigationToolbar2Tk(plt2,root2)
        # toolbar.update()
        plt2.get_tk_widget().place(x=20,y=90)

        # plt.show(block=True)
    elif operation == "Scatter Plot":
        # fig, ax = plt.subplots(figsize=(4, 4)) 
        sns.set_style("whitegrid")
        sns.FacetGrid(data, hue=clickedClass.get(), height=4).map(plt.scatter, attribute1, attribute2).add_legend()
        plt.title("Scatter plot")
        plt2 = FigureCanvasTkAgg(fig, root2) 
        plt2.draw()
        # toolbar = NavigationToolbar2Tk(plt2,root2)
        # toolbar.update()
        plt2.get_tk_widget().place(x=20,y=90)
        # plt.show(block=True)
    elif operation == "Boxplot":
        # fig, ax = plt.subplots(figsize=(4, 4)) 
        sns.set_style("whitegrid")
        sns.boxplot(x=attribute1,y=attribute2,data=data)
        plt.title("Boxplot")
        # plt.show(block=True)
        plt2 = FigureCanvasTkAgg(fig, root2) 
        plt2.draw()
        # toolbar = NavigationToolbar2Tk(plt2,root2)
        # toolbar.update()
        plt2.get_tk_widget().place(x=20,y=90)
    
                            
def selectAttributes(root2,clickedPlot,clickedAttribute1,cols,clickedClass,clickedAttribute2):
    operation = clickedPlot
    if operation == "Quantile-Quantile Plot":
        dropCols = OptionMenu(root2, clickedAttribute1, *cols)
        dropCols.grid(column=3,row=8,padx=20,pady=30)  
        Button(root2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)
    
    elif operation == "Histogram":   
        dropCols = OptionMenu(root2, clickedAttribute1, *cols)
        dropCols.grid(column=3,row=8,padx=20,pady=30)  
        dropCols = OptionMenu(root2, clickedClass, *cols)
        dropCols.grid(column=5,row=8,padx=20,pady=30) 
        Button(root2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)
                        
    elif operation == "Scatter Plot":
        dropCols = OptionMenu(root2, clickedAttribute1, *cols)
        dropCols.grid(column=2,row=8,padx=20,pady=30)
        dropCols = OptionMenu(root2, clickedAttribute2, *cols)
        dropCols.grid(column=3,row=8,padx=20,pady=30)
        dropCols = OptionMenu(root2, clickedClass, *cols)
        dropCols.grid(column=5,row=8)
        Button(root2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)

    elif operation == "Boxplot":
        dropCols = OptionMenu(root2, clickedAttribute1, *cols)
        dropCols.grid(column=2,row=8,padx=20,pady=30)
        dropCols = OptionMenu(root2, clickedAttribute2, *cols)
        dropCols.grid(column=3,row=8,padx=20,pady=30)
        Button(root2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)
                     
def title_changed(topic_name,root2,file_name):
    # topic_name = event.widget.get()
    print(topic_name)
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
    if(topic_name == "Data Display"):
        display_file(file_name)
    elif(topic_name == "measures of central tendency"):
        cols = []
        for i in data.columns:
            cols.append(i)
        clickedAttribute = StringVar(root2)
        clickedAttribute.set("Select Attribute")
        dropCols = OptionMenu(root2, clickedAttribute, *cols)
        dropCols.place(x=20,y=100)
        
        measureOfCentralTendancies = ["Mean","Mode","Median","Midrange","Variance","Standard Deviation"]
        clickedMCT = StringVar(root2)
        clickedMCT.set("Select central tendency")
        dropMCT = OptionMenu(root2, clickedMCT, *measureOfCentralTendancies)
        dropMCT.place(x=160,y=100)
        Button(root2,text="Measure",command= lambda:measureOfCentralT(clickedAttribute,root2,clickedMCT,data)).grid(column=1,row=7,padx=160,pady=170)
    elif(topic_name=="dispersion of data"):
        cols = []
        for i in data.columns:
            cols.append(i)
        clickedAttribute = StringVar(root2)
        clickedAttribute.set("Select Attribute")
        dropCols = OptionMenu(root2, clickedAttribute, *cols)
        dropCols.place(x=20,y=100)
        
        dispersionOfData = ["Range","Quartiles","Inetrquartile range","Minimum","Maximum"]
        clickedDispersion = StringVar(root2)
        clickedDispersion.set("Select Dispersion Operation")
        dropMCT = OptionMenu(root2, clickedDispersion, *dispersionOfData)
        dropMCT.place(x=160,y=100)
        Button(root2,text="Measure",command= lambda:computeOperation(clickedAttribute,clickedDispersion,data,root2)).grid(column=1,row=7,padx=160,pady=170)
    elif(topic_name=="statistical description"):

        clickedAttribute1 = StringVar(root2)
        clickedAttribute1.set("Select First Attribute")
        dropCols1 = OptionMenu(root2, clickedAttribute1, *cols,command=lambda x:update())
        dropCols1.place(x=20,y=20)

        clickedAttribute2 = StringVar(root2)
        clickedAttribute2.set("Select Second Attribute")
        dropCols2 = OptionMenu(root2, clickedAttribute2, *cols,command=lambda x:update())
        dropCols2.place(x=180,y=20)
        
        clickedClass = StringVar(root2)
        clickedClass.set("Select Class")
        dropCols3 = OptionMenu(root2, clickedClass, *cols,command=lambda x:update())
        dropCols3.place(x=350,y=20)
        def update():
            
            if(clickedAttribute1.get() != "Select First Attribute" and clickedAttribute2.get()!="Select Second Attribute" and clickedClass.get() != "Select Class"):
                v = IntVar()
                text_radio = ["Quantile Plot","Histogram","Scatter Plot","Boxplot"]
                # for i in range(len(text_radio)):
                Radiobutton(root2,text=text_radio[0],value=1,variable=v,command=lambda:plt_chart(clickedAttribute1,text_radio[0],clickedAttribute2,data,clickedClass,root2)).place(x=int(20+0*100),y=60)
                Radiobutton(root2,text=text_radio[1],value=2,variable=v,command=lambda:plt_chart(clickedAttribute1,text_radio[1],clickedAttribute2,data,clickedClass,root2)).place(x=int(20+1*100),y=60)
                Radiobutton(root2,text=text_radio[2],value=3,variable=v,command=lambda:plt_chart(clickedAttribute1,text_radio[2],clickedAttribute2,data,clickedClass,root2)).place(x=int(20+2*100),y=60)
                Radiobutton(root2,text=text_radio[3],value=4,variable=v,command=lambda:plt_chart(clickedAttribute1,text_radio[3],clickedAttribute2,data,clickedClass,root2)).place(x=int(20+3*100),y=60)
                print(clickedAttribute2.get(),clickedAttribute2.get(),clickedClass.get())


        
def title(file_name):
    # file_name = open_file()
    root2 = tkinter.Tk()
    root2.title('Data Analysis Tool')
    root2.geometry('500x300+10+10')
    data=["Data Display","measures of central tendency","dispersion of data","statistical description"]

    lbl = Label(root2,text="Select Topic : ",font=("Helvetica",12))
    lbl.place(x=20,y=10)

    cb = ttk.Combobox(root2,values=data)
    cb.place(x=280,y=10)
    cb['state'] = 'readonly'
    cb.bind('<<ComboboxSelected>>',lambda event: title_changed(event,root2,file_name))
    

# open_button = tkinter.Button(root,text="Upload File",command=title,fg='blue')
# open_button.place(x=230,y=110)

# button_exit = Button(root,text="Exit",command=exit,fg='red')
# button_exit.place(x=180,y=150)
# lbl = Label(root,text="Data Analysis Tool",fg='red',font=("Helvetica",18))
# lbl.place(x=80,y=100)
# lbl = Label(root,text="Upload Dataset To start : ",font=("Helvetica",12))
# lbl.place(x=40,y=110)
# # open_button.pack(fill='x')

# root.title('Data Analysis Tool')
# root.geometry('400x250+10+10')
# root.mainloop()
