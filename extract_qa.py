import os
import fitz  # PyMuPDF for reading PDF files
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import base64
import pandas as pd


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


def process_single_response(text):
    """Process a single questionnaire response and return structured data."""
    prompt = f"""Extract the following information from this questionnaire response and format it in a clear way:

1. Name and Function/Role
2. All questions and their corresponding answers

Format the response as follows:

## Respondent: [Name and Function/Role]

### Question: Name & Function
**Answer:** [Their name and function/role]

### Question: [Question text]
**Answer:** [Their response]

[Continue with remaining questions and answers]

Document Text:
{text}
"""
    
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts and formats questionnaire responses."},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=messages,
            temperature=0.1,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing response: {str(e)}"


def extract_data_for_excel(markdown_text):
    """Extract data from markdown text for Excel format."""
    try:
        # Extract name from the first line that contains "Answer:"
        name_line = next(line for line in markdown_text.split('\n') if "Answer:" in line and "Name" in line)
        name = name_line.split("Answer:")[1].strip()
        
        # Extract other Q&A pairs
        qa_pairs = {}
        current_question = None
        
        for line in markdown_text.split('\n'):
            if line.startswith('### Question:'):
                current_question = line.replace('### Question:', '').strip()
            elif line.startswith('**Answer:**') and current_question:
                answer = line.replace('**Answer:**', '').strip()
                qa_pairs[current_question] = answer
                
        return name, qa_pairs
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        return None, None


def main():
    # Load environment variables
    load_dotenv()

    # Define the paths
    pdf_path = "data/d1.pdf"
    markdown_path = "qa_extracted.md"
    excel_path = "qa_responses.xlsx"
    
    try:
        print(f"Attempting to read PDF from: {os.path.abspath(pdf_path)}")
        print("Extracting text from PDF...")
        pages_text = extract_text_from_pdf(pdf_path)

        # Process each page and collect responses
        print("\nProcessing responses...")
        all_responses = []
        excel_data = []
        
        for i, page_text in enumerate(pages_text, 1):
            print(f"Processing response {i} of {len(pages_text)}...")
            response_text = process_single_response(page_text)
            all_responses.append(response_text)
            
            # Extract data for Excel
            name, qa_pairs = extract_data_for_excel(response_text)
            if name and qa_pairs:
                excel_data.append({"Name": name, **qa_pairs})

        # Write markdown file
        print("\nWriting markdown file...")
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write("# GCC Breakout Questionnaire Responses\n\n")
            f.write("This document contains organized responses from the GCC Breakout Questionnaire.\n\n")
            f.write("---\n\n")
            f.write("\n---\n\n".join(all_responses))

        # Create Excel file
        print("Creating Excel file...")
        df = pd.DataFrame(excel_data)
        df.to_excel(excel_path, index=False, sheet_name="Questionnaire Responses")

        print(f"Responses have been saved to:")
        print(f"- Markdown: {markdown_path}")
        print(f"- Excel: {excel_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 