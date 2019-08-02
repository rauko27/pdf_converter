import io
import sys

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


def blank_table(s_dict):
    row = s_dict[0] + ' ' + s_dict[1] + ' ' + s_dict[2] + ' ' + s_dict[3] + '\n'
    print(row)
    file.write(row)
    file.write('\n')


def patient_table(s_dict):
    for i in range(0, len(s_dict) - 3, 4):
        row = s_dict[i] + ',' + s_dict[i + 1] + ',' + s_dict[i + 2] + ',' + s_dict[i + 3] + '\n'
        print(row)
        file.write(row)
    file.write('\n')


def result_table(s_dict):
    header = s_dict[0] + ',' + s_dict[1] + ',' + s_dict[2] + ',' + s_dict[3] + ',' + s_dict[
        4] + "." + s_dict[5] + '\n'
    print(header)
    file.write(header)
    for i in range(6, len(s_dict) - 3, 6):
        row = s_dict[i] + ',' + s_dict[i + 1] + ' ' + s_dict[i + 2] + ',' + s_dict[i + 3] + ',' + \
              s_dict[i + 4] + ',' + \
              s_dict[i + 5] + '\n'
        print(row)
        file.write(row)
    file.write('\n')


def note_table(s_dict):
    row = s_dict + '\n'
    print(row)
    file.write(row)
    file.write('\n')


def done_table(s_dict):
    header = s_dict[0]
    print(header)
    file.write(header)
    row = s_dict[1] + ',' + s_dict[2]
    print(row)
    file.write(row)


# FILE_NAME = 'example_pdf_2'
for i in range(len(sys.argv)-1):
    FILE_NAME = sys.argv[i+1]

    pdf_dict = extract_text_from_pdf('{}'.format(FILE_NAME)).split('  ')
    print(pdf_dict)

    blank_info = pdf_dict[0].split(' ')
    patient_info = pdf_dict[1].split(' ')
    result_info = pdf_dict[3].split(' ')
    note_info = pdf_dict[4]
    done_info = pdf_dict[5].split(' ')

    with open('{}.csv'.format(FILE_NAME), 'w') as file:
        blank_table(blank_info)
        patient_table(patient_info)
        file.write(pdf_dict[2] + '\n')
        result_table(result_info)
        note_table(note_info)
        done_table(done_info)
