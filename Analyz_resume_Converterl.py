from win32com import client as ct
import docx2txt
import json
import PyPDF2
import os


class FormatFileError(Exception):
    pass


class FileConverterPdfDocx:
    @classmethod
    def determine_format(cls, file):
        if file.endswith('.doc'):
            return file
        elif file.endswith('.pdf'):
            return file

        raise FormatFileError("Invalid file format. Valid: pdf, doc")

    @staticmethod
    def convert_docx_to_text(file_doc):
        FileConverterPdfDocx().determine_format(file_doc)
        with open('temp.docx', 'wb') as f:
            f.write(file_doc.getbuffer())
            
        filename = FileConverterPdfDocx().convert_doc_to_docx()
        text = docx2txt.process('temp.docx')
        os.remove('temp.docx')
        return text
    
    @staticmethod
    def convert_pdf_to_text(file_pdf):
        FileConverterPdfDocx().determine_format(file_pdf)
        # Save the uploaded PDF file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(file_pdf.getbuffer())

        # Read the PDF file and extract text
        text = ""
        with open("temp.pdf", "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Remove the temporary file
        os.remove('temp.pdf')

        return text

    @staticmethod
    def convert_doc_to_docx():
        c = ct.Dispatch('Word.Application')
        path = os.path.abspath('temp.docx')
        docx = c.Documents.Open(path)
        docx.SaveAs(path, 16)
        docx.Close()
        c.Quit()


class GgtConverter:
    def __init__(self, candidate_resume):
        self.candidate_resume = candidate_resume


    def json_file_content_to_text_candidate(self, indent=0):
        try:
            content = self.candidate_resume.getvalue().decode("utf-8")
            json_data = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            return "Error decoding JSON: " + str(e)
        return GgtConverter.json_data_to_text(json_data, indent)

    @staticmethod
    def json_data_to_text(json_data, indent=0):
        text = ""
        for key, value in json_data.items():
            if isinstance(value, dict):
                text += "  " * indent + key + ":\n"
                text += GgtConverter.json_data_to_text(value, indent + 1)
            elif isinstance(value, list):
                text += "  " * indent + key + ":\n"
                for item in value:
                    if isinstance(item, dict):
                        text += GgtConverter.json_data_to_text(item, indent + 1)
                    else:
                        text += "  " * (indent + 1) + str(item) + "\n"
            else:
                text += "  " * indent + key + ": " + str(value) + "\n"
        return text.lower()


def find_elements_in_square_brackets(text):
    elements = []
    start_index = 0
    while True:
        start_index = text.find('[', start_index)
        if start_index == -1:
            break
        end_index = text.find(']', start_index)
        if end_index == -1:
            break
        element = text[start_index + 1:end_index]
        elements.append(element)
        start_index = end_index + 1
    return elements

##Пример использования класса
# p = GgtConverter('docs/test_candidat.json')
# #print(p.file_handler())
# print(p.json_file_content_to_text_candidate())
# p = FileConverter('docs/TEST_RESUME.docx')
# print(p.file_to_text())
