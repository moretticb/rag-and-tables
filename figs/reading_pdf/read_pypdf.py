from pypdf import PdfReader # v4.3.1

reader = PdfReader("tables.pdf")

print(reader.pages[1].extract_text())

