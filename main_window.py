import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import maze


class MainWindow():
    def __init__(self):
        self.base = tk.Tk()
        self.base.title('Path finding in maze')
        self.width, self.height = 300, 200
        #self.base.iconphoto(False, tk.PhotoImage(file='Project\maze.png'))
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
        self.file = askopenfilename(initialdir=r"C:\Users\amish\Desktop\PYTHON\Path Finding in Maze",
                                filetypes=(("Text Files", "*.txt"),) )
        try:
            if self.file is not None:
                # Calling the maze module which has the Maze class.
                m = maze.Maze(self.file)
                m.output_image("Path Finding in Maze\maze.png")
                self.image = Image.open("Path Finding in Maze\maze.png")
                # Holding on to the image so that no garbage collector error shows up.
                self.img = ImageTk.PhotoImage(image=self.image)
                self.width, self.height = int(self.image.size[0]*1.5), int(self.image.size[1]*1.5)
                self.base.geometry(str(self.width)+'x'+str(self.height))
            
                self.canvas = tk.Canvas(self.base, height=self.image.size[1], width=self.image.size[0])
                self.canvas.pack(side='top', pady=25)
                self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.img)
                
                self.showSol = tk.Button(self.base, text="Show Solution",
                                        bg='yellow',
                                        bd=1.5,
                                        font='Times 20',
                                        relief='ridge',
                                        command=self.new_window)
                self.showSol.pack(side='bottom', pady=5)
        except FileNotFoundError as fe:
            print("Error: Please upload a valid file !")

    def new_window(self):
        self.nW = tk.Toplevel(self.base)
        self.nW.geometry('400x200')
        self.nW.title('OPTIONS')

        var = tk.StringVar(self.nW, None)
        tk.Label(self.nW, text="Choose an algorithm to solve the maze:", 
                font='Times 15').place(x=20, y=20)
        tk.Radiobutton(self.nW, text='Breadth-first Search',
                        font='Times 10', 
                        variable=var, 
                        value=1,
                        command=lambda: self.collect_options(1)).place(x=20, y=50)
        tk.Radiobutton(self.nW, text='Depth-first Search',
                        font='Times 10', 
                        variable=var, 
                        value=2,
                        command=lambda: self.collect_options(2)).place(x=20, y=80)
        tk.Radiobutton(self.nW, text='A* Search',
                        font='Times 10', 
                        variable=var, 
                        value=3,
                        command=lambda: self.collect_options(3)).place(x=20, y=110)

    def collect_options(self, val):
        self.options.append(val)
        self.submit = tk.Button(self.nW, text="Submit", 
                                bg='yellow',
                                font='Times 18',
                                bd=1.5,
                                command=self.solve_maze).place(x=100, y=150)

    def solve_maze(self):
        o = self.options.pop()
        if o==1:
            import mazeBFS
            mazeBFS.solve(self.file)
        if o==2:
            import mazeDFS
            mazeDFS.solve(self.file)
        if o==3:
            import mazeAStarSearch
            aStar = mazeAStarSearch.AStar(self.file)
            aStar.solve()

        img_sol = Image.open("Path Finding in Maze\mazeSolution.png")
        self.sol_img = ImageTk.PhotoImage(image=img_sol)
        self.canvas.create_image(self.image.size[0]//2, self.image.size[1]//2, image=self.sol_img)
        self.nW.destroy()
        self.showSol.destroy()
        

if __name__=='__main__':
    MainWindow()