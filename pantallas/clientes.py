from tkinter import *
import tkinter
import tkinter as tk
from tkinter import Tk, ttk
from tkinter.messagebox import showerror
from turtle import title
from datos.dao import AccesoDatos
import uuid
from mis_clases.mis_wg import G_entry, G_label

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
    grilla.grid(row=0, column=0, columnspan=6, padx=10, pady= 20)

    grilla.column('#0',width=250,  anchor=tk.CENTER)
    grilla.column('#1',width=450)
    grilla.column('#2',width=100, anchor=tk.CENTER)

    grilla.heading('#0', text='NOMBRE')
    grilla.heading('#1', text='DIRECCION')
    grilla.heading('#2', text='TELEFONO')

    dao = AccesoDatos()

    for (id_cliente, nombre, direccion, telefono) in dao.clientes():
        grilla.insert('', 0,text=id_cliente, values = (nombre, direccion,telefono))

    bt_nuevo_cliente = ttk.Button(frm_clientes,width=10, command = lambda: frm_nuevo_cliente(frm_clientes), text="Nuevo")
    bt_nuevo_cliente.grid(row = 2, column= 5, padx=10, pady= 20,sticky=E)

    bt_cancelar = ttk.Button(frm_clientes, width=10, command=frm_clientes.destroy, text= "Cancelar")
    bt_cancelar.grid(row=2,column=4, padx=10, pady= 20,sticky=E)

    lb_pru=G_label(frm_clientes,texto = "Botonasos")
    lb_pru.grid(row=2,column=3)

    txt_prueba = G_entry(frm_clientes,variable=nombre)
    txt_prueba.grid(row=2,column=2)
    

def frm_nuevo_cliente(root):
     
    frm_nuevo_cliente = Toplevel()
    #frm_nuevo_cliente.geometry("+500+300")
    frm_nuevo_cliente.title("Nuevo Cliente")
    
    ## Provoca que la ventana tome el focus
    frm_nuevo_cliente.focus_set()
    ## Deshabilita todas las otras ventanas hasta que
    ## esta ventana sea destruida.
    frm_nuevo_cliente.grab_set()
    ## Indica que la ventana es de tipo transient, lo que significa
    ## que la ventana aparece al frente del padre.
    frm_nuevo_cliente.transient(master=root)

   
    apellido_nombre = StringVar()
    telefono = StringVar()
    direccion = StringVar()

    marco = ttk.Frame(frm_nuevo_cliente, padding=(20,20))
    marco.grid(row=1,column=2)

    
    lb_apellido_nombre = G_label(marco, texto="Apellido y nombre")
    lb_apellido_nombre.grid(row=1,column=1, sticky=E)
    txt_apellido_nombre = G_entry(marco, variable=apellido_nombre)
    txt_apellido_nombre.grid(row=1, column= 2, sticky=W)

    lb_telefono = G_label(marco, texto="Telefono")
    lb_telefono.grid(row=2,column=1,sticky=E)
    txt_telefono = G_entry(marco, variable=telefono)
    txt_telefono.grid(row=2,column=2,sticky=W)

    lb_direccion = G_label(marco, texto="Dirección")
    lb_direccion.grid(row=3,column=1,sticky=E)
    txt_direccion = G_entry(marco, variable=direccion)
    txt_direccion.grid(row=3,column=2,sticky=W)


    #separ1 = ttk.Separator(frm_nuevo_cliente, orient=HORIZONTAL).grid(column=0,row=4, ipadx=100, pady=10, columnspan=3)

    bt_aceptar = ttk.Button(marco,command=lambda: guardar_cliente({"id_cliente":uuid.uuid4(),"apellido_nombre":apellido_nombre.get(), "telefono":telefono.get(), "direccion":direccion.get()}), text="Aceptar")
    bt_aceptar.grid(row = 5, column = 2, sticky=E)

    bt_cancelar = ttk.Button(marco, command=frm_nuevo_cliente.destroy, text= "Cancelar")
    bt_cancelar.grid(row = 5,column = 2, pady=20, sticky=W)
    frm_nuevo_cliente.mainloop()


def guardar_cliente(registro):
    if not registro['apellido_nombre']:
        showerror("Ojo","No se ingreso el nombre")

    #datos = AccesoDatos()
    #datos.nuevo_cliente(registro)
    
def frm_modifica_cliemte():
    pass


#frm_nuevo_cliente()