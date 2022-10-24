from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import PIL
from PIL import Image
from pyafipws import pyqr


qr=pyqr.PyQR()
#archivo = qr.CrearArchivo


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






c=canvas.Canvas("ticket.pdf")
c.setPageSize((80*mm, 200*mm))
c.setLineWidth(.3)
c.setFont('Helvetica',9)


img = PIL.Image.open("octopeque.png")
wid, hgt = img.size

c.drawImage("octopeque.png", 0, 200*mm - hgt,
preserveAspectRatio=True, mask='auto', width = 80*mm, anchor = 'c')

img = PIL.Image.open("qr.png")

img = img.resize((190,190))
img.save("qr.png")
wid, hgt = img.size
c.drawImage("qr.png" ,0, 10, preserveAspectRatio=True, mask='auto', width=80*mm, anchor = 'c')


#mask='auto' respeta la transparencia
c.drawString(10,50,"ancho:"+str(wid)+ " alto:"+str(hgt))
c.drawString(10,40,"Texto PDF 1")
c.drawString(10,30,"Texto PDF 2")
c.drawString(10,20,"Texto PDF 3")
c.drawString(10,10,"Texto PDF 4")
c.save()
