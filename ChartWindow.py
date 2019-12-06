from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ChartWindow:
    def __init__(self, title):
        self.master = Tk()
        self.width = 500
        self.height = 500

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coords = int((screen_width / 2) - (self.width / 2))
        y_coords = int((screen_height / 2) - (self.height / 2))

        self.master.title(title)

        self.master.geometry("{}x{}+{}+{}".format(self.width, self.height, x_coords, y_coords))
        self.master.resizable(0, 0)


    def bar_chart(self, title, data):
        # TODO: Fix labels.
        types = []
        counts = []
        for item in data.values():
            types.append(item.get('description'))
            counts.append(item.get('count'))

        new_data = {
            'ტიპი': types,
            'რაოდენობა': counts
        }

        df = DataFrame(new_data, columns=['ტიპი', 'რაოდენობა'])
        df = df[['ტიპი', 'რაოდენობა']].groupby('ტიპი').sum()

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot(111)
        bar = FigureCanvasTkAgg(figure, self.master)
        bar.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df.plot(kind='bar', legend=True, ax=ax)
        ax.set_title(title)

        self.master.mainloop()
