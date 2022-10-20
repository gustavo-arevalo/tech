from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
c=canvas.Canvas("archivoPdf.pdf")
c.setPageSize((80*mm, 200*mm))
c.setLineWidth(.3)
c.setFont('Helvetica',9)
c.drawImage("octo.png", 10, 90, mask='auto') #mask='auto' respeta la transparencia
c.drawString(10,40,"Texto PDF 1")
c.drawString(10,30,"Texto PDF 2")
c.drawString(10,20,"Texto PDF 3")
c.drawString(10,10,"Texto PDF 4")
c.save()
