#! python3

import os
import click
from PyPDF4 import PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from pagination_vm.merge import paginate_pdf

# Need to create a blank page a the beginning and remove -1 to the pagination.

def create_template_pagination(name_file, total_pages):
    c = canvas.Canvas(name_file)
    c.setPageSize(
        (17*inch, 11*inch) # Tabloid format
    )
    for _ in range(total_pages):
        page_num = c.getPageNumber()
        text = "%s/%s" % (page_num, total_pages)
        c.drawString(
            16.4*inch,
            0.15*inch,
            text,
        )
        c.showPage()
    c.save()


@click.command(help="Add pagination 1/n at bottom-right of a pdf file.")
@click.argument("pdf_name", nargs=1)
def numeration(pdf_name):

    pdf = PdfFileReader(pdf_name)
    number_total_of_pages = pdf.getNumPages()

    print(f"PDF Name .............: {pdf_name}")
    print(f"Total number of pages : {number_total_of_pages}")

    # Create a folder paginatedPDFs where the new pdfs will be loaded.
    os.makedirs(r"./paginatedPDFs", exist_ok=True)

    # Create the layer with footer.
    create_template_pagination(
        "pagination.pdf",
        number_total_of_pages
    )

    # Create the new pdf merging two layers:  footer + manual
    paginate_pdf(
        pdf_name,
        number_total_of_pages,
        "pagination.pdf",
    )

    # Delete the pdf template
    os.remove("pagination.pdf")


if __name__ == "__main__":
    numeration()


#TODO: implement library prompt_toolkit, click option
#TODO: manage 1 or 2 pages index
#TODO: click - on file , many files, or all files in folders.
#TODO: display with info and instructions at beginning
#TODO: handling missed used
#TODO: review of varialbles names