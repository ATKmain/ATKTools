import os
import fitz  # PyMuPDF for reading PDF files
from dotenv import load_dotenv
from openai import AzureOpenAI
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
    """Extracts all text from the given PDF file using Azure Document Intelligence."""
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
    
    # Extract text from the result
    text = ""
    for page_num, page in enumerate(result.pages, 1):
        page_text = ""
        for line in page.lines:
            page_text += line.content + " "
        text += page_text + "\n"
        print(f"Page {page_num}: Extracted {len(page_text)} characters")
    
    if text.strip():
        print(f"\nTotal extracted text length: {len(text)} characters")
        print("\nFirst 500 characters of extracted text:")
        print("-" * 50)
        print(text[:500])
        print("-" * 50)
    else:
        print("Warning: No text was extracted from the PDF!")
    
    return text


def extract_qa_from_text(text, deployment_name):
    """Uses Azure OpenAI to extract question and answer pairs from text and return them in markdown format."""
    if not text.strip():
        return "Error: No text was provided for Q&A extraction. Please check if the PDF contains searchable text."
        
    prompt = f"""Analyze the following questionnaire responses and organize them by person/respondent. 
Each page appears to be a response from a different person.

For each respondent, extract and format the information as follows:

## Respondent: [Name and Function/Role]

### Question: Name & Function
**Answer:** [Their name and function/role]

### Question: [Question text]
**Answer:** [Their response]

[Continue with all questions and answers for this respondent]

---

[Repeat for next respondent]

Important:
- Start each respondent's section with their name as a header
- Include all questions and answers for each respondent
- Use markdown formatting
- Separate each respondent's section with a horizontal line (---)
- Make sure to capture any additional comments or notes they provided

Document Text:
{text}
"""
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that organizes questionnaire responses into a clear, person-by-person format."},
        {"role": "user", "content": prompt}
    ]

    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=0.1,  # Reduced temperature for more consistent formatting
            max_tokens=2000   # Increased token limit for longer responses
        )
        
        # Add a header to the markdown file
        header = """# GCC Breakout Questionnaire Responses

This document contains organized responses from the GCC Breakout Questionnaire, with each respondent's answers presented separately.

---

"""
        return header + response.choices[0].message.content
    except Exception as e:
        return f"Error during Q&A extraction: {str(e)}"


def main():
    # Load environment variables from .env
    load_dotenv()

    # Get the deployment name from environment variables
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not deployment_name:
        print("Error: AZURE_OPENAI_DEPLOYMENT_NAME not found in environment variables")
        return

    # Define the path to the original PDF file (not the searchable output)
    pdf_path = "data/d1.pdf"
    
    try:
        print(f"Attempting to read PDF from: {os.path.abspath(pdf_path)}")
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)

        print("\nExtracting Q&A pairs using Azure OpenAI...")
        qa_markdown = extract_qa_from_text(text, deployment_name)

        # Write the output to a markdown file
        output_path = "qa_extracted.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(qa_markdown)

        print(f"Q&A pairs extracted and saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 