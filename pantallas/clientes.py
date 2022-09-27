from tkinter import *
import tkinter
import tkinter as tk
from tkinter import Tk, ttk
from datos.dao import AccesoDatos

def frm_clientes(root):

    frm_clientes = Toplevel()
    frm_clientes.geometry("+500+300")
    
    ## Provoca que la ventana tome el focus
    frm_clientes.focus_set()
    ## Deshabilita todas las otras ventanas hasta que
    ## esta ventana sea destruida.
    frm_clientes.grab_set()
    ## Indica que la ventana es de tipo transient, lo que significa
    ## que la ventana aparece al frente del padre.
    frm_clientes.transient(master=root)

    grilla = ttk.Treeview(frm_clientes, column = ('nombre','direccion', 'telefono'))
    grilla.grid(row=4, column=0, columnspan=2, padx=10, pady= 20)

    grilla.column('#0',width=250,  anchor=tk.CENTER)
    grilla.column('#1',width=450)
    grilla.column('#2',width=100, anchor=tk.CENTER)

    grilla.heading('#0', text='NOMBRE')
    grilla.heading('#1', text='DIRECCION')
    grilla.heading('#2', text='TELEFONO')

    dao = AccesoDatos()

    for (nombre, direccion, telefono) in dao.clientes():
        grilla.insert('', 0,text=nombre, values = (direccion,telefono))

def frm_nuevo_cliente(root):
     
    frm_nuevo_cliente = Toplevel()
    frm_nuevo_cliente.geometry("+500+300")
    
    ## Provoca que la ventana tome el focus
    frm_nuevo_cliente.focus_set()
    ## Deshabilita todas las otras ventanas hasta que
    ## esta ventana sea destruida.
    frm_nuevo_cliente.grab_set()
    ## Indica que la ventana es de tipo transient, lo que significa
    ## que la ventana aparece al frente del padre.
    frm_nuevo_cliente.transient(master=root)

    marco= tkinter.LabelFrame(frm_nuevo_cliente, text="NUEVO CLIENTE")
    marco.config(relief="ridge") 
    marco.config(borderwidth=1)
    marco.config(padx=10, pady=10)
    marco.pack()
    
    apellido_nombre = StringVar()
    telefono = StringVar()
    direccion = StringVar()

    
    lb_apellido_nombre = ttk.Label(marco, text="Apellido y nombre", padding=(5,5))
    lb_apellido_nombre.grid(row=1,column=1, sticky=E)
    txt_apellido_nombre = Entry(marco, textvariable=apellido_nombre)
    txt_apellido_nombre.grid(row=1, column= 2, sticky=W)

    lb_telefono = ttk.Label(marco, text="Telefono", padding=(5,5))
    lb_telefono.grid(row=2,column=1,sticky=E)
    txt_telefono = Entry(marco, textvariable=telefono)
    txt_telefono.grid(row=2,column=2,sticky=W)

    lb_direccion = ttk.Label(marco, text="Dirección", padding=(5,5))
    lb_direccion.grid(row=3,column=1,sticky=E)
    txt_direccion = Entry(marco, textvariable=direccion)
    txt_direccion.grid(row=3,column=2,sticky=W)


    separ1 = ttk.Separator(marco, orient=HORIZONTAL).grid(column=0,row=4, ipadx=100, pady=10, columnspan=3)

    bt_aceptar = ttk.Button(marco,command=lambda: guardar_cliente((apellido_nombre.get(), telefono.get(), direccion.get())), text="Aceptar")
    bt_aceptar.grid(row = 5, column= 2, sticky=E)

    bt_cancelar = ttk.Button(marco, command=frm_nuevo_cliente.destroy, text= "Cancelar")
    bt_cancelar.grid(row=5,column=1,sticky=E)
    frm_nuevo_cliente.mainloop()


def guardar_cliente(registro):
    datos = AccesoDatos()
    datos.nuevo_cliente(registro)
    
def frm_modifica_cliemte():
    pass


#frm_nuevo_cliente()