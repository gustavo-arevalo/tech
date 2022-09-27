from tkinter import *
import tkinter as tk
from tkinter import Tk, ttk
from ttkbootstrap import Style

from .clientes import *

 
def frm_frincipal():

    root = tk.Tk()
    style = Style(theme='darkly')
    #root = style.master
    root.geometry("850x480")
   
    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Listado clientes", command = lambda : frm_clientes(root))
    filemenu.add_command(label="Nuevo", command=lambda : frm_nuevo_cliente(root))
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_command(label="Close", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="Clientes", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)

    menubar.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)

    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)        
    root.mainloop()

def donothing():
    pass