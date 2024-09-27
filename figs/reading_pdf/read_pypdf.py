from pypdf import PdfReader # v4.3.1

reader = PdfReader("../../pdf/tables.pdf")

print(reader.pages[0].extract_text())

