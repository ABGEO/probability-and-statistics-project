from MainWindow import *


if __name__ == '__main__':
    root = Tk()
    root.iconphoto(True, PhotoImage(file="./resources/icon.png"))
    main_window = MainWindow(root)
    main_window.draw()
