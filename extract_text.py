"""
PDF Text Extractor using Azure Document Intelligence

This script extracts text from PDF files using Azure Document Intelligence service.
It's designed to work with the process_qa.py script for processing questionnaire responses.

Input:
- PDF file (default: data/d1.pdf)

Output:
- JSON file (data/extracted_text.json):
  - Contains extracted text from each page
  - Includes total page count
  - Structured for easy processing by process_qa.py

Features:
- Uses Azure Document Intelligence for high-quality text extraction
- Handles multi-page PDFs
- Preserves page-by-page text separation
- Saves results for later processing to avoid repeated API calls

Requirements:
- Python 3.8+
- azure-ai-documentintelligence
- python-dotenv
- Azure Document Intelligence API access

Environment Variables Required:
- AZURE_ENDPOINT: Azure Document Intelligence endpoint
- AZURE_KEY: Azure Document Intelligence API key
"""

import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import base64


def initialize_doc_client():
    """Initialize the Document Intelligence client"""
    endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("AZURE_KEY")
    
    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )


def extract_text_from_pdf(pdf_path):
    """Extracts text from the given PDF file using Azure Document Intelligence and returns a list of page texts."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")

    print(f"Analyzing PDF using Azure Document Intelligence...")
    
    # Initialize the Document Intelligence client
    client = initialize_doc_client()
    
    # Read the PDF file
    with open(pdf_path, "rb") as f:
        document_bytes = f.read()
    
    # Analyze the document
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body={
            "base64Source": base64.b64encode(document_bytes).decode()
        },
        content_type="application/json"
    )
    
    result = poller.result()
    
    # Extract text from the result, page by page
    pages_text = []
    for page_num, page in enumerate(result.pages, 1):
        page_text = ""
        for line in page.lines:
            page_text += line.content + " "
        pages_text.append(page_text)
        print(f"Page {page_num}: Extracted {len(page_text)} characters")
    
    return pages_text


def main():
    # Load environment variables
    load_dotenv()

    # Define the paths
    pdf_path = "data/d1.pdf"
    output_path = "data/extracted_text.json"
    
    try:
        print(f"Attempting to read PDF from: {os.path.abspath(pdf_path)}")
        print("Extracting text from PDF...")
        pages_text = extract_text_from_pdf(pdf_path)

        # Save extracted text to JSON file
        print(f"\nSaving extracted text to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_pages': len(pages_text),
                'pages': pages_text
            }, f, ensure_ascii=False, indent=2)

        print(f"Text extraction completed. Results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 