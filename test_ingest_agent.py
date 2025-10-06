import fitz

def test_extract_text_pdf():
    # Create a sample PDF for testing
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello, PyMuPDF!")
    pdf_path = "sample_test.pdf"
    doc.save(pdf_path)
    doc.close()

    # Now test extraction
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    assert "Hello, PyMuPDF!" in text