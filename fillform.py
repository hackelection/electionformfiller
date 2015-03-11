from firebase import firebase

#**************AUTHENTICATION IS NEEDED TO MAKE SURE ONLY WE CAN READ THIS
firebase = firebase.FirebaseApplication('https://electionhack.firebaseio.com', None)
result = firebase.get('/forms/testform', None)
print result

from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = StringIO.StringIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(10, 100, "Hello world")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(file("template.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = file("testform-complete.pdf", "wb")
output.write(outputStream)
outputStream.close()