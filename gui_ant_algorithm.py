import matplotlib
import tkinter
from tkinter import StringVar, IntVar, DoubleVar, Label, Entry, Button
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from mpldatacursor import datacursor
from ant_algorithm import find_shortest_path


class GraphicInterface(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.button_ok = Button(self, text="Update", command=self.display_results)
        self.button_ok.place(y=370, x=25)
        self.button_clear = Button(self, text="Clear", command=self.delete_canvas)
        self.button_clear.place(y=370, x=130)
        self.button_create = Button(self, text="Create", command=self.create_plot)
        self.button_create.place(y=370, x=80)
        func = self.draw_shortest_path
        self.button_short_path = Button(self, text="Find the shortest path", command=func)
        self.button_short_path.place(y=370, x=175)
        self.nodes = dict()
        self.selected_nodes = dict()


    def delete_canvas(self):
        self.canvas.get_tk_widget().pack_forget()


    def display_results(self):
        points = [int(i) for i in self.points.get().split(" ")]
        for node in points:
            self.selected_nodes[node] = self.nodes[node]
        self.delete_canvas()
        self.create_canvas()
        for key, value in self.selected_nodes.items():
            self.ax.scatter(value[0], value[1], color='red', s=14)
            plt.annotate(key, (value[0], value[1]))
        print(self.selected_nodes)
    

    def draw_shortest_path(self):
        self.display_results()
        print(self.selected_nodes)
        arguments = find_shortest_path(self.selected_nodes, self.alpha.get(), 
                                       self.beta.get(), self.Q.get(), self.ro.get())
        for i in range(1, len(arguments)):
            x0 = self.selected_nodes[arguments[i-1]][0]
            x1 = self.selected_nodes[arguments[i]][0]
            y0 = self.selected_nodes[arguments[i-1]][1]
            y1 = self.selected_nodes[arguments[i]][1]
            line = lines.Line2D([x0, x1], [y0, y1])
            self.ax.add_line(line)
            plt.plot()


    def create_plot(self):
        self.create_canvas()
        self.X, self.Y = [], []

        self.X.append(0)
        self.Y.append(0)
        self.count = 1
        for i in range(1, 10):
            self.X.append(self.X[i-1] + 2)
            for j in range(1, 10):
                self.Y.append(self.Y[j-1] + 2)
                self.ax.scatter(self.X[i], self.Y[j], color='blue', s=10)
                self.nodes[self.count] = [self.X[i], self.Y[j]]
                plt.annotate(self.count, (self.X[i], self.Y[j]))
                self.count += 1

    
    def create_canvas(self):
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.grid(which='major', color='#CCCCCC', linestyle='--')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.RIGHT)
    

    def labels(self):
        self.label_points = Label(self, text="Введіть вузли для сполучення: ").place(y=110, x=25)
        self.label_alpha = Label(self, text="Введіть вагу інтенсивності сліду феромону, α: ")
        self.label_alpha.place(y=155, x=25)
        self.label_beta = Label(self, text="Введіть вагу видимості, β: ")
        self.label_beta.place(y=200, x=25)
        self.label_ro = Label(self, text="Введіть коефіцієнт випаровування, p: ").place(y=245, x=25)
        self.label_Q = Label(self, text="Введіть регульований параметр, Q: ").place(y=290, x=25)
    

    def entries(self):
        self.points = StringVar()
        self.alpha, self.beta, self.ro = DoubleVar(), DoubleVar(), DoubleVar()
        self.Q = IntVar()
        self.points_entry = Entry(self, textvariable=self.points)
        self.points_entry.place(y=135, x=25, width=250)
        self.alpha_entry = Entry(self, textvariable=self.alpha)
        self.alpha_entry.place(y=180, x=25, width=25)
        self.beta_entry = Entry(self, textvariable=self.beta)
        self.beta_entry.place(y=225, x=25, width=25)
        self.ro_entry = Entry(self, textvariable=self.ro)
        self.ro_entry.place(y=270, x=25, width=25)
        self.Q_entry = Entry(self, textvariable=self.Q)
        self.Q_entry.place(y=315, x=25, width=25)
        self.alpha.set(1)
        self.beta.set(6)
        self.ro.set(0.4)
        self.points.set("1 12 16 28 39 26 43")
        self.Q.set(100)


gui = GraphicInterface()
gui.labels()
gui.entries()
gui.title("Ant algorithm")
gui.geometry("1000x500")
gui.mainloop()