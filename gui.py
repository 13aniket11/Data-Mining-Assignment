from cmath import exp
import tkinter as tk
from tkinter import Menu
from pandastable import Table, TableModel
from assignment1.assignment1 import *
from assignment2.assignment2 import *
from assignment3.assignment3 import *
from assignment5.assignment5 import *
from assignment6.kmeans import *
from assignment6.KMedoids import *
from assignment8.assignment8 import *
from assignment8.bfs import *
from assignment8.dfs import *
from assignment7.apriorialgo import *
from assignment6.dbscan import *

file_name = ""
data = pd.read_csv('D:/College/BTech/SEM 7/Data Mining/DataSet/Iris.csv')

class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        self.stored_dataframe = pd.DataFrame()

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children())
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col)

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)
        return None

    def find_value(self, pairs):
        # pairs is a dictionary
        new_df = self.stored_dataframe
        for col, value in pairs.items():
            query_string = f"{col}.str.contains('{value}')"
            new_df = new_df.query(query_string, engine="python")
        self._draw_table(new_df)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Data Analysis Tool")
        # self.create_widgets()
        self.resizable(0, 0)
        # self.geometry('1200x600+10+10')
        self.geometry('%dx%d'%(self.winfo_screenwidth(),self.winfo_screenheight()))
        # self.attributes('-fullscreen',True)
        self.config(bg="#f27d92")
        self._frame = None
        self.menu_bar()
        self.data_table = DataTable(self)
        self.switch_frame(StartPage)
        self.side_bar()
        lbl = Label(self,text="Upload File Before Using Tools",fg='red',font=("Helvetica",13))
        lbl.place(x=140,y=5)

    def side_bar(self):
<<<<<<< HEAD
        frame = Frame(self,bg='violet',width=130,height=650)
        # frame.grid(row=0,column=0) 
        frame.pack(side=LEFT,fill=BOTH)
        # Make the buttons with the icons to be shown
        ass_1 = Button(frame,text="Assignment 1",bg='violet',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment1))
        ass_2 = Button(frame,text="Assignment 2",bg='violet',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment2))
        ass_3 = Button(frame,text="Assignment 3 - 4",bg='violet',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment3))
        ass_4 = Button(frame,text="Assignment 4",bg='violet',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment3))
        ass_5 = Button(frame,text="Assignment 5",bg='violet',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment5))
=======
        frame = Frame(self,bg='#55bdca',width=130,height=650)
        # frame.grid(row=0,column=0) 
        frame.pack(side=LEFT,fill=BOTH)
        # Make the buttons with the icons to be shown
        ass_1 = Button(frame,text="Assignment 1",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment1))
        ass_2 = Button(frame,text="Assignment 2",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment2))
        ass_3 = Button(frame,text="Assignment 3 - 4",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment3))
        ass_4 = Button(frame,text="Assignment 4",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment3))
        ass_5 = Button(frame,text="Assignment 5",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment5))
        ass_6 = Button(frame,text="Assignment 6",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment6))
        ass_7 = Button(frame,text="Assignment 7",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment7))
        ass_8 = Button(frame,text="Assignment 8",bg='#55bdca',relief='flat',padx=10,pady=10,command=lambda:self.switch_frame(Assignment8))

>>>>>>> ba710d8ca6026636b5f897503bc6d0d83e53021c
        # Put them on the frame
        # ass_1.grid(row=0,column=0,padx=10,pady=10)
        ass_1.place(x=0,y=5)
        ass_2.place(x=0,y=40)
        ass_3.place(x=0,y=75)
        # ass_4.place(x=0,y=110)
        ass_5.place(x=0,y=110)
        ass_6.place(x=0,y=145)
        ass_7.place(x=0,y=180)
        ass_8.place(x=0,y=215)

    def menu_bar(self):
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = Menu(self)
        self.file_menu1 = Menu(self)
        def OpenFile():
            if self._frame is not None:
                self._frame.destroy()
            global file_name 
            file_name = open_file(self)
            global data
            data = pd.read_csv(file_name)
            def ass2():
                assignment_2(file_name)
            self.file_menu.add_command(
                label="Data pre-processing Task",
                command=ass2
            )

            def class_task():
                root = tkinter.Tk()
                root.title('Data Analysis Tool ')
                root.geometry('600x400+10+10')
                view_dtc(root,file_name)

            self.file_menu.add_command(
                label="Classification Task",
                command=class_task
            )

            def rbc():
                self.show_frame(StartPage)

            self.file_menu.add_command(
                label="Rule Based Classifier",
                command=rbc
            )

            self.file_menu.add_separator()

            def displayfile():
                # print(self._frame)
                if(self._frame is not None):
                    self._frame.destroy()
                self.switch_frame(StartPage)
                self._frame.show_data(file_name)

            sub_menu = Menu(self.file_menu,tearoff=0)

            sub_menu.add_command(
                label="Display Data",
                command=displayfile
            )

            def mct():
                if(self._frame is not None):
                    self._frame.destroy()
                self.switch_frame(Assignment1)
                title_changed("measures of central tendency",self._frame,file_name)

            sub_menu.add_command(
                label="Measures of Central Tendency",
                command=mct
            )

            def dod():
                root2 = tkinter.Tk()
                root2.title('Data Analysis Tool')
                root2.geometry('400x250+10+10')
                title_changed("dispersion of data",root2,file_name)

            sub_menu.add_command(
                label="Dispersion of Data",
                command=dod

            )
            def sd():
                root2 = tkinter.Tk()
                root2.title('Data Analysis Tool')
                root2.geometry('400x250+10+10')
                title_changed("statistical description",root2,file_name)

            sub_menu.add_command(
                label="statistical description",
                command=sd
            )

            self.file_menu.add_cascade(
                label="More",
                menu=sub_menu
            )

            if(file_name):
                if(self._frame is not None):
                    self._frame.destroy()
                self.switch_frame(StartPage)
                print("File Found")
                lbl = Label(self,text="Upload File  : "+str(file_name),fg='green',font=("Helvetica",13))
                lbl.place(x=140,y=5)                
                self._frame.show_data(file_name)
                self.menubar.add_cascade(
                    label="Select Tools",
                    menu=self.file_menu
                )
            else:
                print("Invalid Path")
                lbl = Label(self,text="File is not Uploaded ",fg='red',font=("Helvetica",13))
                lbl.place(x=140,y=5)
                return 

        self.file_menu1.add_command(
            label="Open File",
            command=OpenFile
        )

        self.file_menu1.add_separator()

        self.file_menu1.add_command(
            label="Exit",
            command=self.destroy
        )

        self.menubar.add_cascade(
            label="file",
            menu=self.file_menu1,
        )

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        # new_frame
        self._frame = new_frame
        self._frame.config(bg="#f27d92")
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self.data_table = DataTable(self)

    def show_data(self,file_name):
        if(file_name):
            df = pd.read_csv(file_name)
            self.data_table.place(x=00, y=40,width=1070, height=540)
            self.data_table.set_datatable(dataframe=df)
        else:
            print("File is not uploaded")
    
class Assignment1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        tk.Button(self, text="Measures of central tendency",
                  command=lambda:self.sub_frame("measures of central tendency") ).place(x=80, y=40)
        tk.Button(self, text="dispersion of data",
                  command=lambda: self.sub_frame("dispersion of data")).place(x=280, y=40)
        tk.Button(self, text="statistical description",
                  command=lambda: self.sub_frame("statistical description")).place(x=400, y=40)
    def sub_frame(self,title_name):
        new_frame = Frame(self,width=900,height=500)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=80,y=70)
        title_changed(title_name,self._frame,file_name)

class Assignment2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        tk.Button(self, text="Chi-Square Test",
                  command=lambda:self.sub_frame("Chi-Square Test") ).place(x=80, y=40)
        tk.Button(self, text="Correlation(Pearson) Coefficient",
                  command=lambda: self.sub_frame("Correlation(Pearson) Coefficient")).place(x=200, y=40)
        tk.Button(self, text="Normalization Techniques",
                  command=lambda: self.sub_frame("Normalization Techniques")).place(x=400, y=40)
    
    def sub_frame(self,title_name):
        new_frame = Frame(self,width=900,height=500)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=80,y=70)
        ass2_title_changed(title_name,self._frame,file_name)

class Assignment3(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        self.sub_frame()
            
    def sub_frame(self):
        new_frame = Frame(self,width=1000,height=500)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=20,y=20)
        view_dtc(self._frame,file_name)

class Assignment5(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        tk.Button(self, text="Naïve Bayesian Classifier.",
                  command=lambda:self.sub_frame("Naïve Bayesian Classifier.") ).place(x=80, y=20)
        tk.Button(self, text="k-NN classifier",
                  command=lambda: self.sub_frame("k-NN classifier")).place(x=280, y=20)
        tk.Button(self, text="ANN classifier",
                  command=lambda: self.sub_frame("ANN classifier")).place(x=400, y=20)
    
            
    def sub_frame(self,title_name):
        new_frame = Frame(self,width=1200,height=600)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=20,y=40)
        if(title_name=="ANN classifier"):
            ann(file_name,self._frame)
        elif(title_name=="Naïve Bayesian Classifier."):
            main(self._frame,file_name)
        elif(title_name=="k-NN classifier"):
            knn_main(file_name, self._frame)
        

class Assignment6(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        tk.Button(self, text="AGNES",
                  command=lambda:self.sub_frame("AGNES") ).place(x=80, y=20)
        tk.Button(self, text="DIANA",
                  command=lambda:self.sub_frame("DIANA") ).place(x=150, y=20)
        tk.Button(self, text="k-Means",
                  command=lambda: self.sub_frame("k-Means")).place(x=280, y=20)
        tk.Button(self, text="k-Medoids classifier",
                  command=lambda: self.sub_frame("k-Medoids classifier")).place(x=400, y=20)
        tk.Button(self, text="DBSCAN",
                  command=lambda: self.sub_frame("DBSCAN")).place(x=600, y=20)
    def sub_frame(self,title_name):
        new_frame = Frame(self,width=1600,height=800,bg="#f27d92")
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=20,y=50)
        data = pd.read_csv(file_name)
        if(title_name=="AGNES"):
            main_asgens(data,self._frame)
        elif(title_name=="DIANA"):
            main_diana(data,self._frame)
        elif(title_name=="k-Means"):
            kmeans_main(data,self._frame)
        elif(title_name=="k-Medoids classifier"):
            data = pd.read_csv(file_name)
            k_medoids(data, self._frame)
        elif(title_name=="DBSCAN"):
            # kmeans_main(file_name, self._frame)         
            main_dbscan(data,self._frame)



class Assignment7(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        tk.Button(self, text="frequent item sets",
                  command=lambda:self.sub_frame("1") ).place(x=80, y=20)
        tk.Button(self, text="Association Rules",
                  command=lambda: self.sub_frame("2")).place(x=280, y=20)
    
    def sub_frame(self,title_name):
        new_frame = Frame(self,width=1200,height=600,bg="#f27d92")
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=20,y=50)
        bread = pd.read_csv(file_name)

        bread = bread.drop_duplicates()

        bread = bread.drop('DateTime', axis=1)
        print(len(set(bread['Items'])))
        print(bread.head)

        transaction = pd.crosstab(index= bread['TransactionNo'], columns= bread['Items'])
        print(transaction)
        my_freq_itemset = NONE
        
        if(title_name == "1"):
            my_freq_itemset = aa_helper(title_name,transaction, bread)
            
            print(type(my_freq_itemset))
            f = Frame(self._frame)
            f.place(x=20,y=50)
            pt = Table(f,dataframe=my_freq_itemset,showstatusbar=True)
            pt.show()
        elif(title_name == "2"):
            my_freq_itemset = aa_helper(title_name,transaction, bread)
            
            print(my_freq_itemset)
            f = Frame(self._frame)
            f.place(x=20,y=50)
            pt = Table(f,dataframe=my_freq_itemset,showstatusbar=True)
            pt.show()

class Assignment8(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # self['width']=800
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        self._frame =None
        tk.Button(self, text="BFS",
                  command=lambda:self.sub_frame("1") ).place(x=80, y=20)
        tk.Button(self, text="DFS",
                  command=lambda: self.sub_frame("2")).place(x=200, y=20)
        tk.Button(self, text="Rank of Web Page",
                  command=lambda: self.sub_frame("3")).place(x=300, y=20)
        tk.Button(self, text="HITS Algorithm",
                  command=lambda: self.sub_frame("4")).place(x=500, y=20)
    def sub_frame(self,title_name):
        new_frame = Frame(self,width=1200,height=600,bg="#f27d92")
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=20,y=50)
        if(title_name=="1"):
            label=Label(self._frame, text="Enter URL", font=("Helvetica",12))
            label.place(x=30,y=50)
            entry= Entry(self._frame, width= 40)
            entry.focus_set()
            entry.place(x=230,y=50)
            def bfs_test():
                url = BFS_crawler(entry.get())
                print(url)
                s = Scrollbar(self._frame)
                t = Text(self._frame, width=800)
                t.focus_set()
                # s.pack(side=RIGHT, fill=Y)
                t.place(x=20,y=120)
                s.config(command=t.yview)
                t.config(yscrollcommand=s.set)
                j = 0
                for i in url: 
                    t.insert(tk.END, str(j) + " " + i + "\n")
                    j = j + 1
            Button(self._frame,text="Compute",command= lambda:bfs_test()).place(x=230,y=70)
            
        elif(title_name=="2"):
            label=Label(self._frame, text="Enter URL", font=("Helvetica",12))
            label.place(x=30,y=50)
            entry= Entry(self._frame, width= 40)
            entry.focus_set()
            entry.place(x=230,y=50)
            def dfs_test():
                url = DFS_crawler(entry.get())
                print(url)
                s = Scrollbar(self._frame)
                t = Text(self._frame, width=800)
                t.focus_set()
                # s.pack(side=RIGHT, fill=Y)
                t.place(x=20,y=120)
                s.config(command=t.yview)
                t.config(yscrollcommand=s.set)
                j = 0
                for i in url: 
                    t.insert(tk.END, str(j) + " " + i + "\n")
                    j = j + 1
            Button(self._frame,text="Compute",command= lambda:dfs_test()).place(x=230,y=70)
            
        elif(title_name=="3" or title_name=="4"):
            filename = open_file(self._frame)
            print(filename)
            df,x,y = ass8_main(title_name, filename)
            label=Label(self._frame, text=x + " " + y, font=("Helvetica",12))
            label.place(x=30,y=50)
            f = Frame(self._frame)
            f.place(x=30,y=90)
            pt = Table(f,dataframe=df,showstatusbar=True)
            pt.show()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill=BOTH,side=RIGHT,expand=True)
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()