from tkinter import Tk, ttk
from tkinter import *

class G_label(ttk.Label):

    def __init__(self,master, **kwargs): #**kwargs
        super(G_label,self).__init__(master)
       
        self.config(text = kwargs['texto'] if "texto" in kwargs else "G_label" )
        self.config(padding=(5,5))

class G_entry(Entry):

    def __init__(self,master, **kwargs):
        super(G_entry, self).__init__(master,textvariable=kwargs['variable'])
        self.grid(padx=15,pady=5)