from configparser import ConfigParser
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import PIL
from PIL import Image
from pyafipws import pyqr
from datetime import datetime

def ticket(items,total):
    #print(len(items))
    #print(items[0]["departamento"])
    parser = ConfigParser()
    parser.read('config.ini')
    empresa = parser.get('fiscal','empresa')
    logo = parser.get('fiscal','logo')
    cuit = parser.get('fiscal','cuit')
    iibb = parser.get('fiscal','iibb')
    domicilio = parser.get('fiscal','domicilio')
    inicio_actividades = parser.get('fiscal','inicio_actividades')
    condicion_iva = parser.get('fiscal','condicion_iva')
    punto_venta = parser.get('fiscal','punto_venta')
    tipo_factura = parser.get('fiscal','tipo_factura')
    fecha_hora = datetime.now()
    numero_factura = "0003-0001254"

    largo_ticket = 0
    alto_renglon = 10
    img_logo = PIL.Image.open("octopeque.png")
    ancho_logo, alto_logo = img_logo.size

    ancho_qr = 190
    alto_qr = 190

    largo_ticket += alto_logo
    print(largo_ticket)
    largo_ticket += (len(items) * alto_renglon)
    largo_encabezado = largo_ticket
    largo_ticket += alto_qr
    largo_ticket += (10 * alto_renglon) # 10 * renglones de encabezado que son 10 hasta ahora
    
    
    print(largo_ticket)

    c=canvas.Canvas("ticket.pdf")
    c.setPageSize((80*mm, largo_ticket))
    c.setLineWidth(.3)
    c.setFont('Helvetica',9)

    c.drawImage("octopeque.png", 0, largo_ticket - alto_logo,
    preserveAspectRatio=True, mask='auto', width = 80*mm, anchor = 'c')

    c.drawString(10,largo_ticket-largo_encabezado,empresa)
    c.drawString(10,largo_ticket-largo_encabezado-10,'CUIT '+cuit)
    c.drawString(10,largo_ticket-largo_encabezado-20,'IIBB '+iibb)
    c.drawString(10,largo_ticket-largo_encabezado-30,domicilio)
    c.drawString(10,largo_ticket-largo_encabezado-40,'INICIO ACTIVIDADES '+inicio_actividades)
    c.drawString(10,largo_ticket-largo_encabezado-50,'CONDICION IVA: '+condicion_iva)
    c.setFont('Helvetica-Bold',9)
    c.drawCentredString(40*mm, largo_ticket-largo_encabezado-70, tipo_factura)
    c.setFont('Helvetica',9)
    c.drawString(10,largo_ticket-largo_encabezado-90,'PTO VTA: '+punto_venta)
    c.drawString(10,largo_ticket-largo_encabezado-100,'FECHA: '+fecha_hora.strftime("%d/%m/%Y %H:%M:%S"+'hs.'))
    c.setFont('Helvetica-Bold',9)
    c.drawString(10,largo_ticket-largo_encabezado-120,'NRO. FACTRA: '+numero_factura)
    c.setFont('Helvetica',9)
    c.drawString(10,largo_ticket-largo_encabezado-130,'A consumidor final ')

    desp = 150
    for item in items:
        c.drawString(10,largo_ticket-largo_encabezado-desp,item['departamento'] +'      '+ str(item['tasa_iva']) + '     ' + str(item['importe']))
        desp += 10
    c.save()




items = [{"departamento":"almacen","cantidad":1,"importe": 125.50,"tasa_iva": 21},
        {"departamento":"verduleria","cantidad":1,"importe": 525.50,"tasa_iva": 10.5}]
total = 12300

ticket(items, total)

    