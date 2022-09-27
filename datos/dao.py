import pymysql

class AccesoDatos():
    def __init__(self):
        pass

    def conectar(self):
        try:
            self.conexion=pymysql.connect(
            host="vinculouno.com",
            user="u222113426_goose",
            password="wx4OoCjh1=eB",
            database="u222113426_tech"
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
        print(registro)
        pass

    def vw_clientes_ventas(self):
        consulta="select * vw_clientes_ventas"
        self.conectar()
        self.cursor.execute(consulta)
        rs = self.cursor.fetchall()
        self.desconectar()
        return rs


