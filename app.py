from tkinter import Tk
from MainWindow import *


def main():
    root = Tk()
    main_window = MainWindow(root)
    main_window.draw()


if __name__ == '__main__':
    main()
