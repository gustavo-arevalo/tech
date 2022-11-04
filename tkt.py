from configparser import ConfigParser
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import PIL
from PIL import Image
from pyafipws import pyqr
from datetime import datetime

def ticket(datos_factura):
    
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
    tipo_comprobante = 6 #factura B
    fecha_hora = datetime.now()
    numero_factura = 1254

    largo_ticket = 0
    alto_renglon = 10
    img_logo = PIL.Image.open("octopeque.png")
    img_logo_afip = PIL.Image.open("afip.png")
    ancho_logo, alto_logo = img_logo.size
    ancho_logo_afip, alto_logo_afip = img_logo_afip.size

    ancho_qr = 190
    alto_qr = 300

    largo_ticket += alto_logo
    
    largo_ticket += (len(datos_factura["items"]) * alto_renglon)
    largo_encabezado = largo_ticket #hasta aca es el largo del encabezado
    largo_ticket += alto_qr
    largo_ticket += alto_logo_afip
    largo_ticket += (13 * alto_renglon) # 13 * renglones de encabezado mas pie que son 13 hasta ahora
    
    
    

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
    c.drawString(10,largo_ticket-largo_encabezado-120,'NRO. FACTRA: '+str(numero_factura))
    c.setFont('Helvetica',9)
    c.drawString(10,largo_ticket-largo_encabezado-130,'A consumidor final ')

    desp = 150
    for item in datos_factura["items"]:
        c.drawString(10,largo_ticket-largo_encabezado-desp,item['departamento'] +'  (iva '+ str(item['tasa_iva']) + ')')        
        c.drawRightString(75*mm,largo_ticket-largo_encabezado-desp,'$'+str(item['precio']))
        desp += 10

    desp += 10
    c.setFont('Helvetica-Bold',12)
    c.drawRightString(75*mm,largo_ticket-largo_encabezado-desp,'TOTAL $'+str(datos_factura["total"]))
    c.setFont('Helvetica',9)
    desp += 20
    c.drawString(10,largo_ticket-largo_encabezado-desp,'CAE '+ datos_factura["cae"] )
    c.drawRightString(75*mm,largo_ticket-largo_encabezado-desp,'Vto. CAE '+ datos_factura["vto_cae"] )

    qr=pyqr.PyQR()
    archivo = qr.CrearArchivo

    # dejo el texto de guia de parametros
    #url = qr.GenerarImagen(ver, fecha, cuit, pto_vta, tipo_comprobante, nro_cmp, 
    #                         precio, moneda, ctz, tipo_doc_rec, nro_doc_rec, 
    #                         tipo_cod_aut, cod_aut)

    #formateo fecha para el qr
    fecha=fecha_hora.strftime("%d/%m/%Y")
     
    url = qr.GenerarImagen(1, fecha, cuit, int(punto_venta), int(tipo_comprobante), int(numero_factura), 
                         float(total), "PES", 0, 99, 1, "E", int(cae))


    imagen = Image.open("qr.png")
    imagen = imagen.resize((150,150))
    imagen.save("qr.png")

    desp += 170
    c.drawImage("qr.png",0, largo_ticket-largo_encabezado-desp, preserveAspectRatio=True, mask='auto', width=80*mm, anchor = 'c')
    desp += 30
    c.drawImage("afip.png",0, largo_ticket-largo_encabezado-desp, preserveAspectRatio=True, mask='auto', width=80*mm, anchor = 'c')
    desp += 10
    c.drawCentredString(40*mm, largo_ticket-largo_encabezado-desp, "COMPROBANTE AUTORIZAO")
    desp += 10
    c.drawCentredString(40*mm, largo_ticket-largo_encabezado-desp, "Esta Administración Federal no se")
    desp += 10
    c.drawCentredString(40*mm, largo_ticket-largo_encabezado-desp, "responzabiliza por los datos ingresados")
    desp += 10
    c.drawCentredString(40*mm, largo_ticket-largo_encabezado-desp, "en el detalle de la operación.")

    c.showPage()
    c.save()
    print("milimietras " + str(mm))


total = 12300
cae = "566322188663321"
vto_cae ="30/12/2022"

"""
items = [{"departamento":"almacen","cantidad":1,"precio": 125.50,"tasa_iva": 21},
        {"departamento":"verduleria","cantidad":1,"precio": 525.50,"tasa_iva": 10.5},
        {"departamento":"cigarrillos","cantidad":1,"precio": 325.50,"tasa_iva": 10.5}]
"""
datos_factura = {"total": 12300, "cae" : "566322188663321", "vto_cae" : "30/12/2022",
    "items" : [{"departamento":"almacen","cantidad":1,"precio": 125.50,"tasa_iva": 21},
        {"departamento":"verduleria","cantidad":1,"precio": 525.50,"tasa_iva": 10.5},
        {"departamento":"cigarrillos","cantidad":1,"precio": 325.50,"tasa_iva": 10.5}] }



#ticket(datos_factura, total, cae, vto_cae)
ticket(datos_factura)

    