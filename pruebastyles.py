import tkinter as tk
from ttkbootstrap import Style
from interfaces.ppal import FramePrincipal

def main():

    style = Style(theme='darkly')
    root = style.master
    root.geometry("850x480")

    #app = FramePrincipal(root = root)
    #app = FramePrincipal()
    app.mainloop()


if __name__ == '__main__':
    main()
