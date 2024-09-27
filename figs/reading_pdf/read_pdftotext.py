import pdftotext # v2.2.2

with open("../../pdf/tables.pdf", "rb") as f:
    pages = list(pdftotext.PDF(f))

print(pages[0])
