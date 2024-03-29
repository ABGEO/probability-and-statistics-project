from tkinter import *
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import matplotlib.pyplot as plt


class ChartWindow:
    def __init__(self, title, width=500, height=500):
        self.master = Tk()
        self.width = width
        self.height = height

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coords = int((screen_width / 2) - (self.width / 2))
        y_coords = int((screen_height / 2) - (self.height / 2))

        self.master.title(title)

        self.master.geometry("{}x{}+{}+{}".format(self.width, self.height, x_coords, y_coords))

    def bar_chart(self, title, data):
        types = []
        counts = []
        for item in data.values():
            types.append(item.get('description'))
            counts.append(item.get('count'))

        new_data = {
            'ტიპი': types,
            'ადამიანების რაოდენობა': counts
        }

        df = DataFrame(new_data, columns=['ტიპი', 'ადამიანების რაოდენობა'])
        df = df[['ტიპი', 'ადამიანების რაოდენობა']].groupby('ტიპი').sum()

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot()
        bar = FigureCanvasTkAgg(figure, self.master)
        bar.get_tk_widget().pack(side=TOP, fill=BOTH)
        df.plot(kind='barh', subplots=True, legend=True, ax=ax)
        ax.set_title(title)
        bar.draw()

        # Add toolbar.
        toolbar = NavigationToolbar2Tk(bar, self.master)
        toolbar.update()
        bar.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.master.mainloop()

    def pie_chart(self, title, data):
        labels = []
        counts = []
        for item in data.values():
            labels.append(item.get('description'))
            counts.append(item.get('count'))

        new_data = {
            'ტიპი': labels,
            'რაოდენობა': counts
        }

        df = DataFrame(new_data, columns=['ტიპი', 'რაოდენობა'])
        df = df[['ტიპი', 'რაოდენობა']].groupby('ტიპი').sum()

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot(111)
        pie = FigureCanvasTkAgg(figure, self.master)
        pie.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df.plot(kind='pie', subplots=True, labeldistance=None, legend=True,
                ax=ax, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        ax.set_title(title)
        ax.yaxis.set_label_text("")
        ax.xaxis.set_label_text("")
        pie.draw()

        # Add toolbar.
        toolbar = NavigationToolbar2Tk(pie, self.master)
        toolbar.update()
        pie.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.master.mainloop()

    def scatter_chart(self, title, data1, data2):
        df = DataFrame({'x': data2, 'y': data1})

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot(111)
        pie = FigureCanvasTkAgg(figure, self.master)
        pie.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df.plot(x='x', y='y', kind='scatter', ax=ax)
        ax.set_title(title)
        ax.yaxis.set_label_text("")
        ax.xaxis.set_label_text("")
        pie.draw()

        # Add toolbar.
        toolbar = NavigationToolbar2Tk(pie, self.master)
        toolbar.update()
        pie.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.master.mainloop()

    def linear_chart(self, title, data):
        df = DataFrame({'კვარტილი': list(data.keys()), 'დანახარჯების ჯამი': list(data.values())})

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot(111)
        pie = FigureCanvasTkAgg(figure, self.master)
        pie.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df.plot(x='კვარტილი', y='დანახარჯების ჯამი', ax=ax)
        ax.set_title(title)
        pie.draw()

        # Add toolbar.
        toolbar = NavigationToolbar2Tk(pie, self.master)
        toolbar.update()
        pie.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.master.mainloop()

    def distribution_chart(self, title, data):
        df = DataFrame({'რაოდენობა': data})

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot(111)
        hist = FigureCanvasTkAgg(figure, self.master)
        hist.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df.plot(kind='hist', ax=ax, bins=50)
        ax.set_title(title)
        ax.yaxis.set_label_text("რაოდენობა")
        ax.xaxis.set_label_text("დიაპაზონი")
        hist.draw()

        # Add toolbar.
        toolbar = NavigationToolbar2Tk(hist, self.master)
        toolbar.update()
        hist.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.master.mainloop()
