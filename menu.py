import tkinter
from tkinter import Menu

from assignment1.assignment1 import *
from assignment2.assignment2 import *
from assignment3.assignment3 import *

# home = tkinter.Tk()
# home.title("Data Analysis Tool")
# home.geometry('1200x600+10+10')

# # Menu Bar 

# menubar = Menu(home)
# home.config(menu=menubar)

# file_menu = Menu(home)
# file_menu1 = Menu(home)





# home.mainloop()
import tkinter as tk
file_name = ""

class BaseFrame(tk.Frame):
    """An abstract base class for the frames that sit inside PythonGUI.

    Args:
      master (tk.Frame): The parent widget.
      controller (PythonGUI): The controlling Tk object.

    Attributes:
      controller (PythonGUI): The controlling Tk object.

    """

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.place()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the frame."""
        raise NotImplementedError

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

class Assignment1(BaseFrame):
    def create_widgets(self):
        self.new_button = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.show_frame(ExecuteFrame),
                                    padx=5,
                                    pady=5,
                                    text="Excute")
        # self.new_button.grid(padx=5, pady=5, sticky=tk.W+tk.E)
        self.new_button.place(anchor=tk.W,x=160,y=30)
    def display_data(self,file_name):
        df = pd.read_csv(file_name)
        # self.data_table = DataTable(self)
        # self.data_table.place(x=155,y=20)
        print(df)
        # self.data_table.set_datatable(dataframe=df)


class ExecuteFrame(BaseFrame):
    """The application home page.

    Attributes:
      new_button (tk.Button): The button to switch to HomeFrame.

    """

    def create_widgets(self):
        """Create the base widgets for the frame."""
        self.new_button = tk.Button(self,
                                    anchor=tk.W,
                                    command=lambda: self.controller.show_frame(Assignment1),
                                    padx=5,
                                    pady=5,
                                    text="Home")
        # self.new_button.grid(padx=5, pady=5, sticky=tk.W+tk.E)
        self.new_button.place(anchor=tk.W,x=160,y=30)


class HomeFrame(BaseFrame):
    """The application home page.

    Attributes:
      new_button (tk.Button): The button to switch to ExecuteFrame.

    """

    def create_widgets(self):
        """Create the base widgets for the frame."""
        self.new_button = Button(self,bg='orange',relief='flat',command=lambda: self.controller.show_frame(ExecuteFrame),padx=5,pady=5,text="Execute")
        # self.new_button.grid(row=1,column=1,padx=5, pady=5, sticky=tk.W)
        print(self)
        # self.new_button.place(x=160,y=30)
        # self.lbl =  Label(self,padx=5, pady=5,text="Upload Dataset To start :+++++++++++++++++++ ",bg='red',font=("Helvetica",12))
        # self.lbl.grid(padx=5, pady=5, sticky=tk.W)
        self.new_button.place(x=160,y=40)



class PythonGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Data Analysis Tool")
        self.create_widgets()
        # self.resizable(0, 0)
        self.geometry('1200x600+10+10')

    def create_widgets(self):
        #   Frame Container
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = Menu(self)
        self.file_menu1 = Menu(self)
        self.container = Frame(self,width=1100,height=630)
        frame = Frame(self,width=130,height=650)
        # frame.grid(row=0,column=0) 
        frame.place(x=0,y=0)
        # Make the buttons with the icons to be shown
        ass_1 = Button(frame,text="Assignment 1",bg='orange',relief='flat',padx=10,pady=10)
        ass_2 = Button(frame,text="Assignment 2",bg='orange',relief='flat',padx=10,pady=10)
        ass_3 = Button(frame,text="Assignment 3",bg='orange',relief='flat',padx=10,pady=10)
        ass_4 = Button(frame,text="Assignment 4",bg='orange',relief='flat',padx=10,pady=10)
        ass_5 = Button(frame,text="Assignment 5",bg='orange',relief='flat',padx=10,pady=10)
        # Put them on the frame
        # ass_1.grid(row=0,column=0,padx=10,pady=10)
        ass_1.place(x=0,y=5)
        ass_2.place(x=0,y=40)
        ass_3.place(x=0,y=75)
        ass_4.place(x=0,y=110)
        ass_5.place(x=0,y=145)
        # ass_2.grid(row=1,column=0,padx=10,pady=10)
        # ass_3.grid(row=2,column=0,padx=10,pady=10)
        # ass_4.grid(row=3,column=0,padx=10,pady=10)
        # ass_5.grid(row=4,column=0,padx=10,pady=10)
        # frame.grid_propagate(False)

        def OpenFile():
            file_name = open_file(self)
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
                self.show_frame(HomeFrame)

            self.file_menu.add_command(
                label="Rule Based Classifier",
                command=rbc
            )

            self.file_menu.add_separator()

            def displayfile():
                # print()
                self.frames['Assignment1'].display_data(file_name)
                # display_file(file_name)
                # A = self.frames['Ass']
                # A.display_data(file_name)

            sub_menu = Menu(self.file_menu,tearoff=0)

            sub_menu.add_command(
                label="Display Data",
                command=displayfile
            )

            def mct():
                root2 = tkinter.Tk()
                root2.title('Data Analysis Tool')
                root2.geometry('400x250+10+10')
                title_changed("measures of central tendency",root2,file_name)

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
                print("File Found")
                lbl = Label(self,text="Upload File  : "+str(file_name),font=("Helvetica",9))
                lbl.place(x=150,y=20)
                self.menubar.add_cascade(
                    label="Select Tools",
                    menu=self.file_menu
                )
            else:
                print("File is not found")
                lbl = Label(self,text="File is not Uploaded ",font=("Helvetica",12))
                lbl.place(x=150,y=20)
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

        # self.container.grid(row=0, column=3)
        self.container.place(x=130,y=20)

        #   Frames
        self.frames = {}
        for f in (HomeFrame, ExecuteFrame,Assignment1): # defined subclasses of BaseFrame
            frame = f(self.container, self)
            # frame.grid(row=0, column=0)
            frame.place(x=130,y=20)
            self.frames[f.__name__] = frame
        self.show_frame(HomeFrame)

    def show_frame(self, cls):
        """Show the specified frame.

        Args:
        cls (tk.Frame): The class of the frame to show. 

        """
        self.frames[cls.__name__].tkraise()

if __name__ == "__main__":
    app = PythonGUI()
    app.mainloop()
    exit()