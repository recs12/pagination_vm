
#! python3

import click
from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import PageObject

import reportlab
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
#import pikepdf (explorings)


@click.command(help="Add pagination 1/n at bottom-right of a pdf file.")
@click.argument("pdf_name", nargs=1)
def numeration(pdf_name):
    print(f"PDF Name: {pdf_name}")
    pdf = PdfFileReader(pdf_name)
    number_total_of_pages = pdf.getNumPages()
    print(f"Number total of pages: {number_total_of_pages}")

    c = canvas.Canvas("pagination.pdf")
    c.setPageSize((17*inch, 11*inch)) #paper format: Tabloid
    for _ in range(number_total_of_pages):
        page_num = c.getPageNumber()
        text = "%s/%s" % (page_num, number_total_of_pages)
        c.drawString( 16.4*inch, 0.15*inch, text)
        c.showPage()
    c.save()


if __name__ == "__main__":
    numeration()

