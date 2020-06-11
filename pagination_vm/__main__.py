#! python3

import os
import sys
import click
from PyPDF4 import PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from logzero import logger
from pagination_vm.merge import paginate_pdf
from pagination_vm.info import headlines

def confirmation(func):
    response = input(
        """Press y/[Y] to proceed or any key to exit.\n>"""
    )
    if response.lower() not in ["y"]:
        print("Process canceled")
        sys.exit()
    else:
        func()


def create_template_pagination(name_file, total_pages, index, subtitle):
    c = canvas.Canvas(name_file)
    c.setPageSize(
        (17*inch, 11*inch) # set tabloid format
    )
    for _ in range(index):
        c.showPage() # Add one or two empty page at beginning of the template
    for _ in range(total_pages-index):
        page_num = c.getPageNumber()
        text = "%s/%s" % (page_num-index , total_pages-index)
        c.drawString(
            16.4*inch,
            0.15*inch,
            text,
        )
        c.drawString(
            1*inch,
            0.15*inch,
            subtitle,
        )
        c.showPage()
    c.save()

def getDocuments(content):
    if not content:
        return os.listdir()
    else:
        return content

@click.command(help="Add pagination 1/n et title at bottom of a pdf file.")
@click.option('--index', default=1, help='Number of indexed pages.')
@click.argument("documents",  nargs=-1) # tuple
def add_footer(documents, index):
    try:
        documents = getDocuments(documents)
        assert(len(documents) != 0), "No pdf files found in this folder."

        for doc in documents:
            if doc.lower().endswith(".pdf"):
                pdf = PdfFileReader(doc)
                number_total_of_pages = pdf.getNumPages()

                print(f"PDF Name .............: {doc}")
                print(f"Total number of pages : {number_total_of_pages}")

                # Create a folder paginatedPDFs where the new pdfs will be loaded.
                os.makedirs(r"./paginatedPDFs", exist_ok=True)

                # Create the layer with footer.
                create_template_pagination(
                    "pagination.pdf",
                    number_total_of_pages,
                    index,
                    subtitle=doc[:-4],
                )

                # Create the new pdf merging two layers:  footer + manual
                paginate_pdf(
                    doc,
                    number_total_of_pages,
                    "pagination.pdf",
                )

                # Delete the pdf template
                os.remove("pagination.pdf")
    except AssertionError as a:
        logger.exception(a)
    except FileNotFoundError as e:
        logger.exception(e)
    else:
        pass
    finally:
        documents = None
        input("\nPress any key to exit...")
        sys.exit()


if __name__ == "__main__":
    print(headlines)
    confirmation(add_footer)
