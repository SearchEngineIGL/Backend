from django.test import TestCase

from .pdf_extraction import extract_article_pdf

class PDFExtractionTestCase(TestCase):
    def setUp(self):
        # You can set up any common objects or variables needed for the tests here
        pass

    def test_extract_article_pdf(self):
        # Replace 'path/to/your/sample.pdf' with the actual path to your sample PDF file
        sample_pdf_path = 'https://drive.google.com/uc?id=1mwtwqiMZGu0_WURi04oxjIIllFH9zExB&export=download'
        
        # Call the function to extract data from the sample PDF
        result = extract_article_pdf(sample_pdf_path)

        # Define expected values based on the content of your sample PDF
        expected_title = "excepted title"
        expected_abstract = "excepted abstract"
        # Add more expected values for other fields

        # Assert the actual results match the expected values
        # self.assertEqual(result['title'], expected_title)
        self.assertEqual(result['abstract'], expected_abstract)
        # Add more assertions for other fields
