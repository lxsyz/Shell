#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import PyPDF2
import PythonMagick
from PythonMagick import Geometry

import ghostscript

pdffilename = "dem.pdf"
pdf_im = PyPDF2.PdfFileReader(open(pdffilename, "rb"))

npage = pdf_im.getNumPages()
print('Converting %d pages.' % npage)
for p in range(2):
    print(str(p))
    # im = PythonMagick.Image()
    try:
        im = PythonMagick.Image(pdffilename + '[' + str(p) +']')
        # im.resolutionUnits("pixelsperinch")

        im.resize(Geometry(2622, 3500))
        # im.resolutionUnits(72)
        im.depth = 24
        im.antiAlias(True)
        im.density = Geometry(300, 300)
        im.quality(100)

        # im.resolutionUnits("PixelsPerInch")
        # im.read(pdffilename + '[' + str(p) +']')
        # im.magick("PNG")
        im.write('test/' + str(p) + '.jpg')
    except Exception as err:
        print("Magic Exception")
        print(err)
        continue
# print pdffilename + '[' + str(p) +']','file_out-' + str(p)+ '.png'