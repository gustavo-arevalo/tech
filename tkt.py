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
    inicioa_ctividades = parser.get('fiscal','inicio_actividades')
    condicion_iva = parser.get('fiscal','condicion_iva')
    punto_venta = parser.get('fiscal','punto_venta')
    fecha_hora = datetime.now()
    numero_factura = 0

    largo_ticket = 0
    alto_renglon = 10
    img_logo = PIL.Image.open("octopeque.png")
    ancho_logo, alto_logo = img_logo.size

    ancho_qr = 190
    alto_qr = 190

    largo_ticket += alto_logo
    largo_ticket += (len(items) * alto_renglon)
    largo_encabezado = largo_ticket
    largo_ticket += alto_qr
    largo_ticket += (10 * alto_renglon) # 10 * renglones de encabezado que son 10 hasta ahora
    
    

    c=canvas.Canvas("ticket.pdf")
    c.setPageSize((80*mm, largo_ticket*mm))
    c.setLineWidth(.3)
    c.setFont('Helvetica',9)

    c.drawImage("octopeque.png", 0, largo_ticket*mm - alto_logo,
    preserveAspectRatio=True, mask='auto', width = 80*mm, anchor = 'c')

    c.drawString(10,largo_ticket-largo_encabezado-10*alto_renglon,empresa)

    #for item in items
    #    c.drawString(10,40,item['departamento' +' '+ item['tasa_iva'] + ' ' + item['importe'] ])
    c.save




items = [{"departamento":"almacen","cantidad":1,"importe": 125.50,"tasa_iva": 21},
        {"departamento":"verduleria","cantidad":1,"importe": 525.50,"tasa_iva": 10.5}]
total = 12300

ticket(items, total)

    