import os

import io
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter

def watermark_pdf_doc(path_to_doc, document_recipient):
    """[summary]
    Args:
        path_to_doc ([str]): [Path to .pdf document to be watermarked]
        document_recipient ([str]): [Name in watermark text]
    """
    msg = 'Vertraulich an {} - '.format(document_recipient) * 10

    packet = io.BytesIO()
    # create a new PDF with Reportlab & set font
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica-Bold', 10)
    can.setFillColor('red', alpha=0.3)
    can.rotate(45)
    can.drawCentredString(300, 0, msg)
    can.drawCentredString(300, 100, msg)
    can.drawCentredString(300, 200, msg)
    can.drawCentredString(300, 300, msg)
    can.drawCentredString(300, -100, msg)
    can.drawCentredString(300, -200, msg)
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # read existing PDF
    existing_pdf = PdfReader(open(path_to_doc, "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    for page in range(len(existing_pdf.pages)):
        new_page = existing_pdf.pages[page]
        new_page.merge_page(new_pdf.pages[0])
        output.add_page(new_page)

    # Write "output" to a real file
    signed_doc_name = path_to_doc.split('.')[0] + '_watermarked.pdf'
    outputStream = open(signed_doc_name, "wb")
    output.write(outputStream)
    outputStream.close()




def merge_pdfs(pdf_files_list, output_file_name):
    """[summary]
    Args:
        pdf_files_list ([list]): [List of pdf files to be merged]
        output_file_name ([str]): [Result file name]
    """
    merger = PdfMerger()
    [merger.append(pdf) for pdf in pdf_files_list]
    merger.write(output_file_name)
    merger.close()

    return output_file_name


def main():

    watermark = "Mr. Landlord"
    full_output = "templates/watermarked/docs.pdf"

    dir_entries = list(map(lambda f: f"templates/source/{f}", os.listdir("templates/source")))
    dir_files = list(filter(lambda f: os.path.isfile(f), dir_entries))
    if "templates/source/.DS_Store" in dir_files:
        dir_files.remove("templates/source/.DS_Store")

    merge_pdfs(dir_files, full_output) # merge all pdf files in 1
    watermark_pdf_doc(full_output, watermark) # watermark file


if __name__ == "__main__":
    main()
