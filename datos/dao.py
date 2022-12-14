import pymysql
from configparser import ConfigParser
import uuid

class AccesoDatos():
    def __init__(self):
        parser = ConfigParser()
        parser.read('config.ini')
        self.host = parser.get('db', 'host')
        self.user = parser.get('db','user')
        self.password = parser.get('db','password')
        self.database = parser.get('db','database')
       
    def conectar(self):
        try:
            self.conexion=pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
            )
        except pymysql.Error as e:
            print("Error al conectarse a la base de datos", e)

        self.cursor=self.conexion.cursor()
        
        #cursor.execute("select c.nombre, (select sum(todo.cantidad) from vw_clientes_ventas_detalleventaarticulo todo where c.id_cliente = todo.id_cliente and todo.id_articulo = '3ab201e0') as compra	from clientes c	order by compra desc")


    def desconectar(self):
        self.conexion.close()


    def clientes(self):
        consulta="select id_cliente, apellido_nombre, direccion, telefono from clientes"
        self.conectar()
        self.cursor.execute(consulta)
        rs = self.cursor.fetchall()
        self.desconectar()
        return rs

    def nuevo_cliente(self,registro):
        apellido_nombre = registro['apellido_nombre']
        telefono = registro['telefono']
        id_cliente = registro['id_cliente']
        direccion = registro['direccion']

        #consulta = f"INSERT INTO clientes (id_cliente, apellido_nombre, telefono, direccion) VALUES ('{str(registro['id_cliente'])}', '{registro['apellido_nombre']}', '{registro['telefono']}','{registro['direccion']}')"
        consulta = f"INSERT INTO clientes (id_cliente, apellido_nombre, telefono, direccion) VALUES ('{id_cliente}', '{apellido_nombre}', '{telefono}','{direccion}')"
        #(" + str(registro['id_cliente']) +", "+ registro['apellido_nombre'] + ", " + registro['telefono'] +", "+ registro['direccion'] +")"
        
        print(consulta)
        self.conectar()
        self.cursor.execute(consulta)
        print(f"{self.cursor.rowcount} details inserted")
        self.conexion.commit()
        self.desconectar()



    def vw_clientes_ventas(self):
        consulta="select * vw_clientes_ventas"
        self.conectar()
        self.cursor.execute(consulta)
        rs = self.cursor.fetchall()
        self.desconectar()
        return rs


