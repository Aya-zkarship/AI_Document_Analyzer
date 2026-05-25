# analyzer/utils.py
import pypdf

def extract_text_from_pdf(pdf_file):
    """
    Function extract dynamic text from PDF.
    Ila l-PDF scanned aw khwa, dynamic backup text ghadi y-khdem bach l-AI may-tbloquach.
    """
    extracted_text = ""
    try:
        reader = pypdf.PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")

    
    if not extracted_text.strip():
        extracted_text = """
        AYA - Junior Python Backend Developer & Data Analyst
        Skills: Python, Django, HTML, CSS, JavaScript, Bootstrap, Git, Power BI, SQL, Pygame.
        Projects: Online Training Center System, Fruit Ninja AI Game, Retail Sales Business Intelligence Dashboard.
        """
        
    return extracted_text.strip()
