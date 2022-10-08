from tkinter import Tk, ttk

class G_label(ttk.Label):

    def __init__(self,master, **kwargs): #**kwargs
        super(G_label,self).__init__(master)
       
        self.config(text = kwargs['texto'] if "texto" in kwargs else "G_label" )
        self.config(padding=(5,5))

        