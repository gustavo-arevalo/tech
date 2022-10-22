from pyafipws import pyqr


qr=pyqr.PyQR()
archivo = qr.CrearArchivo

print(archivo)

ver = 1
fecha = "2020-10-13"
cuit = 30000000007
pto_vta = 10
tipo_cmp = 1
nro_cmp = 94
importe = 12100
moneda = "DOL"
ctz = 65
tipo_doc_rec = 80
nro_doc_rec = 20000000001
tipo_cod_aut = "E"
cod_aut = 70417054367476

url = qr.GenerarImagen(ver, fecha, cuit, pto_vta, tipo_cmp, nro_cmp, 
                         importe, moneda, ctz, tipo_doc_rec, nro_doc_rec, 
                         tipo_cod_aut, cod_aut)

print(url)
