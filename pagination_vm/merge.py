from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import PageObject


def paginate_pdf(pdf_name, number_page, pagination_template):
    """Create a new pdf with the pagination footer
	starting from the second page of the manual.
	"""

    writer = PdfFileWriter()

    stream_manuals = open(pdf_name, "rb")
    manuals = PdfFileReader(stream_manuals)
    stream_pagination = open(pagination_template, "rb")
    pagination = PdfFileReader(stream_pagination)

    for i in range(number_page):
        manuals_page = manuals.getPage(i)  # pageNumber: 0
        pagination_page = pagination.getPage(i)

        # Stack blank page
        translated_page = PageObject.createBlankPage(
            None,
            width=manuals_page.mediaBox.getHeight(),  # width = 1224
            height=manuals_page.mediaBox.getWidth(),  # height = 792
        )

        # Stack pagination
        translated_page.mergePage(pagination_page)

        # Stack manual
        translated_page.mergeRotatedScaledTranslatedPage(
            manuals_page, rotation=-90, scale=1, tx=0, ty=792, expand=True
        )

        writer.addPage(translated_page)

    pdf_out = "./paginatedPDFs/"+pdf_name  # New name of the output pdf file.

    with open(pdf_out, "wb") as _:
        writer.write(_)

    stream_manuals.close()
    stream_pagination.close()

    print(f"{pdf_out} copied to paginatedPDFs\n")
