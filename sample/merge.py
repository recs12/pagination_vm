from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import PageObject


manuals = PdfFileReader(open("manuals.pdf", "rb"))
# Retrieves a page by number from this PDF file.
manuals_page = manuals.getPage(1)  # pageNumber: 0

pagination = PdfFileReader(open("pagination.pdf", "rb"))
pagination_page = pagination.getPage(0)

# Stack blank page
translated_page = PageObject.createBlankPage(
    None,
	width = manuals_page.mediaBox.getHeight(), # width = 1224
	height = manuals_page.mediaBox.getWidth(), # height = 792
)

# Stack pagination
translated_page.mergePage(
    pagination_page
)

# Stack manual
translated_page.mergeRotatedScaledTranslatedPage(
	manuals_page,
	rotation=-90,
	scale=1,
	tx= 0,
	ty= 792,
	expand=True
)

writer = PdfFileWriter()
writer.addPage(translated_page)

with open("out.pdf", "wb") as _:
    writer.write(_)
