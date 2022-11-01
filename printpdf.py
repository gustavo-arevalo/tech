import win32api
import win32print



GHOSTSCRIPT_PATH = "c:\\Program Files\\gs\\gs10.00.0\\bin\\gswin64.exe"
GSPRINT_PATH = "c:\\Program Files\\gs\\gs10.00.0\\bin\\gsprint.exe"


currentprinter = "EPSON TM-T88V Receipt" #win32print.GetDefaultPrinter()

#win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "ticket.pdf"', '.', 0)
#win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "ticket.pdf"', '.', 0)
#print('-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "ticket.pdf"')
#win32api.ShellExecute()

    #currentprinter = win32print.GetDefaultPrinter()
    #win32api.ShellExecute(0, "print", 'PDFfile.pdf', '/d:"%s"' % currentprinter, ".", 0)

#win32api.ShellExecute(0, "print", "ticket.pdf", None, ".", 0) #comano original

win32api.ShellExecute(0, "print", "ticket.pdf", '/d:"%s"' % currentprinter, ".", 0)
