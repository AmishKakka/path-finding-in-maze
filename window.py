import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import maze


class MainWindow():
    def __init__(self):
        self.base = tk.Tk()
        self.base.title('Path finding in maze')
        self.width, self.height = 300, 200
        #self.base.iconphoto(False, tk.PhotoImage(file='..\maze.png'))
        self.base.geometry(str(self.width)+'x'+str(self.height))
        self.base.minsize(self.width, self.height)
        self.base.maxsize(self.base.winfo_screenwidth(), self.base.winfo_screenheight())

        self.upload = tk.Button(self.base, text="Upload .txt file which has the maze", 
                                bg='yellow',
                                bd=1.5,        
                                font='Times 15',
                                relief='ridge',
                                command=self.open_file)
        self.upload.pack(side='top', pady=15)

        self.options = []
        self.base.mainloop()

    def open_file(self):
        self.file = askopenfilename(filetypes=(("Text Files", "*.txt"),))
        try:
            if self.file is not None:
                # Calling the maze module which has the Maze class.
                self.m = maze.Maze(self.file)
                self.m.output_image("../maze.png")
                self.image = Image.open("../maze.png")
                
                # Resizing the image if it is beyond the screen limits.
                if self.image.size[0] >= self.base.winfo_screenwidth()-100:
                    self.image = self.image.resize((self.base.winfo_screenwidth()-100, self.image.size[1]))
                if self.image.size[1] >= self.base.winfo_screenheight()-200:
                    self.image = self.image.resize((self.image.size[0], self.base.winfo_screenheight()-200))
                
                # Holding on to the image so that no garbage collector error shows up.
                self.img = ImageTk.PhotoImage(image=self.image)
                self.width, self.height = int(self.image.size[0]*1.5), int(self.image.size[1]*1.75)
                self.base.geometry(str(self.width)+'x'+str(self.height))
            
                self.canvas = tk.Canvas(self.base, height=self.image.size[1], width=self.image.size[0])
                self.canvas.pack(side='top', pady=5)
                self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.img)
                
                self.showSol = tk.Button(self.base, text="Show Solution",
                                        bg='yellow',
                                        bd=1.5,
                                        font='Times 20',
                                        relief='ridge',
                                        command=self.solve_maze)
                self.showSol.pack(side='bottom', pady=15)
        except FileNotFoundError as fe:
            print("Error: Please upload a valid file !")

    def solve_maze(self):
        import mazeAStarSearch
        self.aStar = mazeAStarSearch.AStar(self.file)
        # Calling the 'solve' function inside the aStar class.
        self.aStar.solve()
        self.numStates, self.statesExplored = self.aStar.num_explored-1, self.aStar.sol
        
        img_sol = Image.open("../mazeSolution.png")
        self.sol_img = ImageTk.PhotoImage(image=img_sol)
        self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.sol_img)
        self.showSol.destroy()
        self.moreOptions = tk.Button(self.base, text="More Information",
                                        bg='blue',
                                        bd=1.5,
                                        font='Times 20',
                                        relief='ridge',
                                        command=self.newWindow)
        self.moreOptions.pack(side='bottom', pady=5)

    def newWindow(self):
        self.nW = tk.Toplevel(self.base, background='cyan')
        self.nW.geometry('400x200')
        self.nW.title('Details')
        
        label = tk.Label(self.nW, text="Explored a total of "+str(self.numStates)+" states.", background='cyan')
        label.config(font=('Times New Roman', 15))
        label.pack(side='top', pady=5)

        label2 = tk.Label(self.nW, text="Solution states\nROW          COLUMN", height=2, background='cyan')
        label2.config(font=('Times New Roman', 12))
        label2.pack(side='top', pady=0)

        label3 = tk.Label(self.nW, background='cyan')
        label3.pack(side='top', pady=0)
        scroll_bar = tk.Scrollbar(label3, orient=tk.VERTICAL, width=0)
        scroll_bar.pack(side='right')
        mylist = tk.Listbox(label3, yscrollcommand=scroll_bar.set)
        for idx in self.statesExplored:
            mylist.insert(tk.END, "         "+str(idx[0])+"       ||         "+str(idx[1]))
        mylist.pack(side='top')
        scroll_bar.config(command=mylist.yview) 
    

