import io


# pip install pdfminer.six
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

class PDF:
    @staticmethod
    def extract(blob_data):
        try:
            file = io.BytesIO(blob_data)
            metadata = PDF.metadata(file)
            output = io.StringIO()
            pagenums = set()
            manager = PDFResourceManager()
            converter = TextConverter(manager, output, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, converter)

            for page in PDFPage.get_pages(file, pagenums):
                interpreter.process_page(page)

            converter.close()
            text = output.getvalue().strip()
            output.close()
            return text, metadata
        except:
            return None, None

    @staticmethod
    def metadata(file):
        try:
            parser = PDFParser(file)
            doc = PDFDocument(parser)
            info = doc.info
            return info
        except:
            return None
