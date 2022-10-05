import pymysql 
import uuid
    
Host = "vinculouno.com"  
User = "u222113426_goose"       
Password = "wx4OoCjh1=eB"            
  
database = "u222113426_tech"
  
conn  = pymysql.connect(host=Host, user=User, password=Password, database=database) 
  
cur  = conn.cursor() 
  
apellido_nombre = 'papo'
telefono = '4234234'
direccion = 'alberdi 12'
id_cliente = uuid.uuid4()
  
query = f"INSERT INTO clientes (id_cliente, apellido_nombre, telefono, direccion) VALUES ('{id_cliente}', '{apellido_nombre}', '{telefono}','{direccion}')"
  
cur.execute(query) 
print(f"{cur.rowcount} details inserted") 
conn.commit() 
conn.close() 