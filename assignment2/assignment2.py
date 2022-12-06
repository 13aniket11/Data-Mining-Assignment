from re import A
import tkinter
from tkinter import *
from tkinter import filedialog,ttk
import csv
import math
import pandas as pd
import scipy.stats as stats
import seaborn as sns


# root = tkinter.Tk()
# selected_value = StringVar()

# def open_file():
#     file = filedialog.askopenfilename(parent=root,initialdir="D:/College/BTech/SEM 7/Data Mining/DataSet/",title="Select Dataset File", filetypes=[("CSV files", "*.csv*"), ("all files", "*.*")])
#     print(file)

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
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
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
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
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
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
        else:
            res = "Median of given dataset is ("+attribute+") "+str((arr[i]+arr[j])/2)
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
    elif operation == "Midrange":
        n = len(data)
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        res = "Midrange of given dataset is ("+attribute+") "+str((arr[n-1]+arr[0])/2)
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
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
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
        else:
            res = "Standard Deviation of given dataset is ("+attribute+") "+str(math.sqrt(var)) 
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)  
                        
def computeOperation(clickedAttribute,clickedDispersion,data,root2):
    attribute = clickedAttribute.get()
    operation = clickedDispersion.get()
    if operation == "Range":
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        res = "Range of given dataset is ("+attribute+") "+str(arr[len(data)-1]-arr[0])
        Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
    elif operation == "Quartiles" or operation == "Inetrquartile range": 
        arr = []
        for i in range(len(data)):
            arr.append(data.loc[i, attribute])
        arr.sort()
        if operation == "Quartiles": 
            res1 = "Lower quartile(Q1) is ("+attribute+") "+str((len(arr)+1)/4)
            res2 = "Middle quartile(Q2) is ("+attribute+") "+str((len(arr)+1)/2)
            res3 = "Upper quartile(Q3) is ("+attribute+") "+str(3*(len(arr)+1)/4)
            Label(root2,text=res1,width=80,height=3,fg='green').grid(column=1,row=7)
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
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
        else:
            res = "Maximum value of given dataset is ("+attribute+") "+str(arr[len(data)-1])
            Label(root2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)

def plt_chart(clickedAttribute1,clickedPlot,clickedAttribute2,data,plt,clickedClass):
    attribute1 = clickedAttribute1.get()
    attribute2 = clickedAttribute2.get()
    
    operation = clickedPlot.get()
    if operation == "Quantile-Quantile Plot": 
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
        plt.show()
        
    elif operation == "Histogram": 
        sns.set_style("whitegrid")
        sns.FacetGrid(data, hue=clickedClass.get(), height=5).map(sns.histplot, attribute1).add_legend()
        plt.title("Histogram")
        plt.show(block=True)
    elif operation == "Scatter Plot":
        sns.set_style("whitegrid")
        sns.FacetGrid(data, hue=clickedClass.get(), height=4).map(plt.scatter, attribute1, attribute2).add_legend()
        plt.title("Scatter plot")
        plt.show(block=True)
    elif operation == "Boxplot":
        sns.set_style("whitegrid")
        sns.boxplot(x=attribute1,y=attribute2,data=data)
        plt.title("Boxplot")
        plt.show(block=True)
                            
def selectAttributes(root2,clickedPlot,clickedAttribute1,cols,clickedClass,clickedAttribute2):
    operation = clickedPlot.get()
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
                         
# def title_changed(event,root2,file_name):
#     topic_name = event.widget.get()
#     print(topic_name)
#     newfilename = ''
#     for i in file_name:
#         if i == "/":
#             newfilename = newfilename + "/"
#             newfilename = newfilename + i
#     data = pd.read_csv(file_name)
#     d = pd.read_csv(file_name)

#     if(topic_name == "Data Display"):
#         display_file(file_name)
#     elif(topic_name == "measures of central tendency"):
#         cols = []
#         for i in data.columns:
#             cols.append(i)
#         clickedAttribute = StringVar(root2)
#         clickedAttribute.set("Select Attribute")
#         dropCols = OptionMenu(root2, clickedAttribute, *cols)
#         dropCols.place(x=30,y=60)
        
#         measureOfCentralTendancies = ["Mean","Mode","Median","Midrange","Variance","Standard Deviation"]
#         clickedMCT = StringVar(root2)
#         clickedMCT.set("Select central tendency")
#         dropMCT = OptionMenu(root2, clickedMCT, *measureOfCentralTendancies)
#         dropMCT.place(x=190,y=60)
#         Button(root2,text="Measure",command= lambda:measureOfCentralT(clickedAttribute,root2,clickedMCT,data)).grid(column=50,row=7,padx=30,pady=100)
#     elif(topic_name=="dispersion of data"):
#         cols = []
#         for i in data.columns:
#             cols.append(i)
#         clickedAttribute = StringVar(root2)
#         clickedAttribute.set("Select Attribute")
#         dropCols = OptionMenu(root2, clickedAttribute, *cols)
#         dropCols.place(x=30,y=60)
        
#         dispersionOfData = ["Range","Quartiles","Inetrquartile range","Minimum","Maximum"]
#         clickedDispersion = StringVar(root2)
#         clickedDispersion.set("Select Dispersion Operation")
#         dropMCT = OptionMenu(root2, clickedDispersion, *dispersionOfData)
#         dropMCT.place(x=190,y=60)
#         Button(root2,text="Measure",command= lambda:computeOperation(clickedAttribute,clickedDispersion,data,root2)).grid(column=50,row=7,padx=30,pady=100)
#     else:
#         print("ok")

#  assignment_2 function
# 
def chi_sq_test_compute(attribute1,attribute2,data,root2):
    # print(attribute1,attribute2)
    # checking data
    # print(data[attribute1].value_counts(),data[attribute2].value_counts())
    data_crosstab = pd.crosstab(data[attribute1],data[attribute2],margins=True,margins_name="Total")
    # root3 = tkinter.Tk()

    # row_no = 1
    # heading = data_crosstab.columns.values.tolist()
    # heading_row = data_crosstab.

    # for i in range(len(heading)):
    #     label = tkinter.Label(root3,width=10,height=2,text=heading[i],relief=tkinter.RIDGE)
    #     label.grid(row=0,column=i+1)
    # for col in data_crosstab.values.tolist():
    #     col_no =1
    #     for row in col:
    #         label = tkinter.Label(root3,width=10,height=2,text=row,relief=tkinter.RIDGE)
    #         label.grid(row=row_no,column=col_no)
    #         col_no = col_no+1
    #     row_no = row_no+1
    rows = data[attribute1].unique()
    columns = data[attribute2].unique()
    print(data_crosstab)
    chi_square = 0.0
    for i in columns:
        for j in rows:
            obs = data_crosstab[i][j]
            expected = (data_crosstab[i]['Total'] * data_crosstab['Total'][j])/(data_crosstab['Total']['Total'])
            chi_square = chi_square + ((obs - expected)**2/expected)
    p_value = 1 - stats.chi2.cdf(chi_square,(len(rows) - 1)*(len(columns) - 1))
    dof = (len(columns) - 1)*(len(rows) - 1)
    res=""
    if(chi_square > dof):
        res = "Attributes " + attribute1 + ' and ' + attribute2 + " are strongly correlated."
    else:
        res = "Attributes " + attribute1 + ' and ' + attribute2 + " are not correlated."
    print(chi_square)
    Label(root2,text="Chi-square value is "+str(chi_square),fg='red').place(x=100,y=110)
    Label(root2,text=res,fg='green').place(x=100,y=140)

def corelation_coefficients(attribute1,attribute2,data,root2):
    sum = 0
    for i in range(len(data)):
        sum += data.loc[i, attribute1]
    avg1 = sum/len(data)
    sum = 0
    for i in range(len(data)):
        sum += (data.loc[i, attribute1]-avg1)*(data.loc[i, attribute1]-avg1)
    var1 = sum/(len(data))
    sd1 = math.sqrt(var1)
    sum = 0
    for i in range(len(data)):
        sum += data.loc[i, attribute2]
    avg2 = sum/len(data)
    sum = 0
    for i in range(len(data)):
        sum += (data.loc[i, attribute2]-avg2)*(data.loc[i, attribute2]-avg2)
    var2 = sum/(len(data))
    sd2 = math.sqrt(var2)
    
    sum = 0
    for i in range(len(data)):
        sum += (data.loc[i, attribute1]-avg1)*(data.loc[i, attribute2]-avg2)
    covariance = sum/len(data)
    pearsonCoeff = covariance/(sd1*sd2)    
    Label(root2,text="Covariance value is "+str(covariance), justify='center',height=2,fg="red").place(x=100,y=110)
    Label(root2,text="Correlation coefficient(Pearson coefficient) is "+str(pearsonCoeff), justify='center',height=2,fg="red").place(x=100,y=140)
    res = ""
    if pearsonCoeff > 0:
        res = "Attributes " + attribute1 + ' and ' + attribute2 + " are positively correlated."
    elif pearsonCoeff < 0:
        res = "Attributes " + attribute1 + ' and ' + attribute2 + " are negatively correlated."
    elif pearsonCoeff == 0:
        res = "Attributes " + attribute1 + ' and ' + attribute2 + " are independant."
    Label(root2,text=res, justify='center',height=2,fg="red").place(x=100,y=170)  

def normalization_Operations(attribute1,attribute2,data,root2,operation,d):
    if operation == "Min-Max normalization":
        n = len(data)
        arr1 = []
        for i in range(len(data)):
            arr1.append(data.loc[i, attribute1])
        arr1.sort()
        min1 = arr1[0]
        max1 = arr1[n-1]
        
        arr2 = []
        for i in range(len(data)):
            arr2.append(data.loc[i, attribute2])
        arr2.sort()
        min2 = arr2[0]
        max2 = arr2[n-1]
        
        for i in range(len(data)):
            d.loc[i, attribute1] = ((data.loc[i, attribute1]-min1)/(max1-min1))
        
        for i in range(len(data)):
            d.loc[i, attribute2] = ((data.loc[i, attribute2]-min2)/(max2-min2))
    elif operation == "Z-Score normalization":
        sum = 0
        for i in range(len(data)):
            sum += data.loc[i, attribute1]
        avg1 = sum/len(data)
        sum = 0
        for i in range(len(data)):
            sum += (data.loc[i, attribute1]-avg1)*(data.loc[i, attribute1]-avg1)
        var1 = sum/(len(data))
        sd1 = math.sqrt(var1)
        
        sum = 0
        for i in range(len(data)):
            sum += data.loc[i, attribute2]
        avg2 = sum/len(data)
        sum = 0
        for i in range(len(data)):
            sum += (data.loc[i, attribute2]-avg2)*(data.loc[i, attribute2]-avg2)
        var2 = sum/(len(data))
        sd2 = math.sqrt(var2)
        
        for i in range(len(data)):
            d.loc[i, attribute1] = ((data.loc[i, attribute1]-avg1)/sd1)
        
        for i in range(len(data)):
            d.loc[i, attribute2] = ((data.loc[i, attribute2]-avg2)/sd2)
    elif operation == "Normalization by decimal scaling":        
        j1 = 0
        j2 = 0
        n = len(data)
        arr1 = []
        for i in range(len(data)):
            arr1.append(data.loc[i, attribute1])
        arr1.sort()
        max1 = arr1[n-1]
        
        arr2 = []
        for i in range(len(data)):
            arr2.append(data.loc[i, attribute2])
        arr2.sort()
        max2 = arr2[n-1]
        
        while max1 > 1:
            max1 /= 10
            j1 += 1
        while max2 > 1:
            max2 /= 10
            j2 += 1
        
        for i in range(len(data)):
            d.loc[i, attribute1] = ((data.loc[i, attribute1])/(pow(10,j1)))
        
        for i in range(len(data)):
            d.loc[i, attribute2] = ((data.loc[i, attribute2])/(pow(10,j2)))
                            
    Label(root2,text="Normalized Attributes", justify='center',height=2,fg="green").place(x=30,y=160)
    tv1 = ttk.Treeview(root2,height=15)
    tv1.place(x=30,y=190)
    tv1["column"] = [attribute1,attribute2]
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    i = 0
    while i < len(data):
        tv1.insert("", "end", iid=i, values=(d.loc[i, attribute1],d.loc[i, attribute2]))
        i += 1
    # sns.set_style("whitegrid")
    # sns.FacetGrid(d, hue=clickedClass.get(), height=4).map(plt.scatter, attribute1, attribute2).add_legend()
    # plt.title("Scatter plot")
    # plt.show(block=True)

def ass2_title_changed(topic_name,root2,file_name):
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
    if(topic_name == "Chi-Square Test"):
        clickedAttribute = StringVar(root2)
        clickedAttribute.set("Select Attribute")
        dropCols = OptionMenu(root2, clickedAttribute, *cols)
        dropCols.place(x=30,y=60)
        
        clickedAttribute2 = StringVar(root2)
        clickedAttribute2.set("Select Attribute 2")
        dropMCT = OptionMenu(root2, clickedAttribute2, *cols)
        dropMCT.place(x=190,y=60)
        Button(root2,text="Compute",command= lambda:chi_sq_test_compute(clickedAttribute.get(),clickedAttribute2.get(),data,root2)).place(x=30,y=110)

    elif(topic_name=="Correlation(Pearson) Coefficient"):
        clickedAttribute = StringVar(root2)
        clickedAttribute.set("Select Attribute 1")
        dropCols = OptionMenu(root2, clickedAttribute, *cols)
        dropCols.place(x=30,y=60)
        
        clickedAttribute2 = StringVar(root2)
        clickedAttribute2.set("Select Attribute 2")
        dropMCT = OptionMenu(root2, clickedAttribute2, *cols)
        dropMCT.place(x=190,y=60)
        Button(root2,text="Measure",command= lambda:corelation_coefficients(clickedAttribute.get(),clickedAttribute2.get(),data,root2)).place(x=30,y=110)
    elif(topic_name == "Normalization Techniques"):
        clickedAttribute = StringVar(root2)
        clickedAttribute.set("Select Attribute 1")
        dropCols = OptionMenu(root2, clickedAttribute, *cols)
        dropCols.place(x=30,y=60)
        
        clickedAttribute2 = StringVar(root2)
        clickedAttribute2.set("Select Attribute 2")
        dropMCT = OptionMenu(root2, clickedAttribute2, *cols)
        dropMCT.place(x=190,y=60)

        normalizationOperations = ["Min-Max normalization","Z-Score normalization","Normalization by decimal scaling"]
        clickedNO = StringVar(root2)
        clickedNO.set("Select Normalization Operation")
        dropMCT = OptionMenu(root2, clickedNO, *normalizationOperations)
        dropMCT.place(x=30,y=90)

        Button(root2,text="Measure",command= lambda:normalization_Operations(clickedAttribute.get(),clickedAttribute2.get(),data,root2,clickedNO.get(),data)).place(x=30,y=130)
    else:
        print("Invalid Option")
          
# def assignment_1():
#     # file_name = open_file()
#     root2 = tkinter.Tk()
#     root2.title('Data Analysis Tool')
#     root2.geometry('500x300+10+10')
#     data=["Data Display","measures of central tendency","dispersion of data","statistical description"]

#     lbl = Label(root2,text="Select Topic : ",font=("Helvetica",12))
#     lbl.place(x=20,y=10)

#     cb = ttk.Combobox(root2,values=data,)
#     cb.place(x=140,y=10)
#     cb['state'] = 'readonly'
#     cb.bind('<<ComboboxSelected>>',lambda event: title_changed(event,root2,file_name))

def assignment_2(file_name):
    # file_name = open_file()
    root2 = tkinter.Tk()
    root2.title('Data Analysis Tool')
    root2.geometry('500x300+10+10')
    data=["Chi-Square Test","Correlation(Pearson) Coefficient","Normalization Techniques"]

    lbl = Label(root2,text="Select Topic : ",font=("Helvetica",12))
    lbl.place(x=20,y=10)

    cb = ttk.Combobox(root2,values=data)
    cb.place(x=140,y=10)
    cb['state'] = 'readonly'
    cb.bind('<<ComboboxSelected>>',lambda event: ass2_title_changed(event,root2,file_name))

# open_button = tkinter.Button(root,text="Upload File",command=assignment_2,fg='blue')
# open_button.place(x=230,y=110)

# button_exit = Button(root,text="Exit",command=exit,fg='red')
# button_exit.place(x=180,y=190)
# lbl = Label(root,text="Data Analysis Tool",fg='red',font=("Helvetica",18))
# lbl.place(x=80,y=60)
# lbl = Label(root,text="Upload Dataset To start : ",font=("Helvetica",12))
# lbl.place(x=40,y=110)
# # open_button.pack(fill='x')

# root.title('Data Analysis Tool')
# root.geometry('400x250+10+10')
# root.mainloop()
