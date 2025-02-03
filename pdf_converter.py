import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from dotenv import load_dotenv
from pypdf import PdfWriter, PdfReader
import fitz  # PyMuPDF
import time
import base64

# Load environment variables
load_dotenv()

def initialize_client():
    """Initialize the Document Intelligence client"""
    endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("AZURE_KEY")
    
    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def analyze_document(client, file_path):
    """Analyze the document using Azure Document Intelligence"""
    # Check file size - Azure has a 500MB limit
    file_size = os.path.getsize(file_path)
    max_size = 500 * 1024 * 1024  # 500MB in bytes
    
    if file_size > max_size:
        raise ValueError(f"File size ({file_size/1024/1024:.2f}MB) exceeds Azure's 500MB limit")
    
    # Get subscription tier to determine page limit
    try:
        account_properties = client.get_resource_details()
        is_free_tier = account_properties.sku_name.lower() == 'f0'
        
        if is_free_tier:
            print("Warning: Using free tier (F0) - only the first two pages will be processed")
            pages = "1-2"
        else:
            pages = "1-"  # Process all pages in paid tier
            
    except Exception:
        # If unable to determine tier, assume paid tier
        pages = "1-"
        print("Warning: Unable to determine subscription tier")
    
    with open(file_path, "rb") as f:
        document_bytes = f.read()
        
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body={
            "base64Source": base64.b64encode(document_bytes).decode()
        },
        content_type="application/json",
        pages=pages  # Specify pages based on tier
    )
    
    return poller.result()

def create_searchable_pdf(input_path, output_path, result):
    """Create a searchable PDF with recognized text"""
    try:
        # Open the PDF with PyMuPDF
        doc = fitz.open(input_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            print(f"Processing page {page_num + 1}")
            
            # Get the recognized text for this page
            page_text = result.pages[page_num]
            
            # Add text annotations for each line
            for line in page_text.lines:
                try:
                    points = line.polygon
                    page_width = page.rect.width
                    page_height = page.rect.height
                    
                    x0 = points[0] * page_width
                    y0 = points[1] * page_height
                    
                    page.insert_text(
                        (x0, y0),
                        line.content,
                        color=(0, 0, 0),
                        opacity=0
                    )
                except Exception as e:
                    print(f"Warning: Error processing line on page {page_num + 1}: {str(e)}")
                    continue
        
        doc.save(output_path)
        doc.close()
        print(f"Successfully created searchable PDF: {output_path}")
        
    except Exception as e:
        print(f"Error creating searchable PDF: {str(e)}")
        raise

def main():
    # Initialize the client
    client = initialize_client()
    
    # Input and output file paths
    input_file = "C:/repo/pythonScripts/data/fe2.pdf"
    output_file = "C:/repo/pythonScripts/data/fe2_searchable_output.pdf"
    
    print("Starting document analysis...")
    
    # Analyze the document
    result = analyze_document(client, input_file)
    
    print("Creating searchable PDF...")
    
    # Create searchable PDF
    create_searchable_pdf(input_file, output_file, result)
    
    print(f"Searchable PDF created: {output_file}")

if __name__ == "__main__":
    main() 