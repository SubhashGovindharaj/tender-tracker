# data_processing/processor.py
# Data processing functions for tender documents

import pdfplumber
import re
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        return ""

def extract_key_details(text):
    """
    Extract key tender details from text like EMD amount, deadlines, etc.
    Returns a dictionary of extracted information
    """
    details = {}
    
    # Extract EMD amount (simplified regex patterns, would need refinement for real data)
    emd_pattern = r"EMD.*?(?:Rs\.|₹|INR)\s*([\d,]+(?:\.\d+)?)"
    emd_match = re.search(emd_pattern, text, re.IGNORECASE)
    if emd_match:
        details["extracted_emd"] = emd_match.group(1)
    
    # Extract deadline
    deadline_pattern = r"(?:submission|closing|due)\s*date.*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})"
    deadline_match = re.search(deadline_pattern, text, re.IGNORECASE)
    if deadline_match:
        details["extracted_deadline"] = deadline_match.group(1)
    
    # Extract scope of work
    scope_pattern = r"(?:scope\s+of\s+work|statement\s+of\s+work).*?((?:\w+\W+){50})"
    scope_match = re.search(scope_pattern, text, re.IGNORECASE)
    if scope_match:
        details["extracted_scope"] = scope_match.group(1).strip()
    
    # Extract eligibility criteria
    eligibility_pattern = r"(?:eligibility|qualification)\s+criteria.*?((?:\w+\W+){50})"
    eligibility_match = re.search(eligibility_pattern, text, re.IGNORECASE)
    if eligibility_match:
        details["extracted_eligibility"] = eligibility_match.group(1).strip()
    
    return details

def process_tender_document(document_path):
    """
    Process a tender document to extract all relevant information
    """
    if document_path.endswith('.pdf'):
        text = extract_text_from_pdf(document_path)
    else:
        # For text files
        with open(document_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    # Extract details
    details = extract_key_details(text)
    details['full_text'] = text
    
    return details