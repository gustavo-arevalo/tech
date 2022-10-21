from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

import PIL 
from PIL import Image 
  
img = PIL.Image.open("octopeque.png") 
wid, hgt = img.size 


c=canvas.Canvas("archivoPdf.pdf")
c.setPageSize((80*mm, 200*mm))
c.setLineWidth(.3)
c.setFont('Helvetica',9)
c.drawImage("octopeque.png", 10, 200*mm - hgt, mask='auto') #mask='auto' respeta la transparencia
c.drawString(10,50,"ancho:"+str(wid)+ " alto:"+str(hgt))
c.drawString(10,40,"Texto PDF 1")
c.drawString(10,30,"Texto PDF 2")
c.drawString(10,20,"Texto PDF 3")
c.drawString(10,10,"Texto PDF 4")
c.save()
