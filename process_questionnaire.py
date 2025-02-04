"""
Questionnaire Processing Script using Azure OpenAI GPT-4V

This script processes scanned questionnaires in PDF format, extracting handwritten text using
Azure OpenAI's GPT-4V/4o (Vision) model. It handles multi-page PDFs and generates both individual
page extractions and a combined report.

Features:
- Converts PDF pages to high-quality images
- Uses GPT-4V to extract handwritten text
- Generates individual page extractions and images
- Creates a combined markdown report
- Organizes output in timestamped batches

Requirements:
- Azure OpenAI API access with GPT-4V/4o deployment
- Environment variables in .env file:
  - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
  - AZURE_OPENAI_API_VERSION: API version (e.g., "2024-02-15-preview")
  - AZURE_OPENAI_ENDPOINT: Your Azure endpoint URL
  - AZURE_OPENAI_DEPLOYMENT_NAME: Your GPT-4V deployment name

Usage:
    python process_questionnaire.py

Output Structure:
    output/
    └── batch_YYYYMMDD_HHMMSS/
        ├── images/              # High-quality PNG images of each page
        │   └── page_N.png
        ├── texts/              # Individual markdown files for each page
        │   └── page_N.md
        └── combined_results.md  # Combined report with all pages
"""

import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from openai import AzureOpenAI
import base64
from PIL import Image
import io
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize Azure OpenAI client with environment variables
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def encode_image_to_base64(image: Image.Image) -> str:
    """
    Convert a PIL Image to a base64 encoded string.
    
    Args:
        image (PIL.Image.Image): The input image to encode
        
    Returns:
        str: Base64 encoded string of the image
        
    Note:
        Uses PNG format with maximum quality for best OCR results
    """
    buffered = io.BytesIO()
    # Save as PNG with maximum quality for optimal GPT-4V analysis
    image.save(buffered, format="PNG", quality=100, optimize=False)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image_with_gpt4(image: Image.Image) -> str:
    """
    Analyze an image using Azure OpenAI's GPT-4V model to extract questionnaire information.
    
    Args:
        image (PIL.Image.Image): The image to analyze
        
    Returns:
        str: Markdown formatted string containing the extracted information
        
    Note:
        Uses a specific prompt structure to ensure consistent and accurate extraction
        of handwritten text and questionnaire fields.
    """
    base64_image = encode_image_to_base64(image)
    
    # System message defines the AI's role and general behavior
    system_message = """You are an expert at analyzing questionnaire images and extracting information with high accuracy. 
    Your task is to carefully read and transcribe handwritten text from questionnaire images.
    You must be thorough and precise in your extraction, paying special attention to handwritten text.
    Format your response in a clear, structured markdown format."""

    # User message provides specific instructions for the analysis
    user_message = """Please analyze this questionnaire image and extract the following information with high accuracy:

    1. First locate and transcribe the name of the person who filled out the questionnaire
    2. Then identify and transcribe each question and its corresponding handwritten answer
    3. Maintain the exact order of questions as they appear in the form
    4. If any text is unclear or ambiguous, indicate this with [unclear] notation
    
    **Format your response as follows:**
    
    ### Respondent Name
    [Name of person]
    
    ### Questionnaire Responses
    1. Question: [Question text]
   Answer: [Handwritten answer]
    
    2. Question: [Question text]
   Answer: [Handwritten answer]
    
    [Continue for all questions]
    
    **Be as accurate as possible in reading the handwritten text.**"""

    # Make API call to Azure OpenAI
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.3,  # Lower temperature for more consistent results
        max_tokens=4000   # Increased token limit for detailed responses
    )
    
    return response.choices[0].message.content

def pdf_page_to_pil(page: fitz.Page) -> Image.Image:
    """
    Convert a PyMuPDF (fitz) page to a PIL Image.
    
    Args:
        page (fitz.Page): The PDF page to convert
        
    Returns:
        PIL.Image.Image: The converted image at 300 DPI
        
    Note:
        Uses 300 DPI for high-quality text recognition
    """
    # Get the page's pixmap at 300 DPI
    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
    
    # Convert pixmap to PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def process_pdf(pdf_path: str, output_dir: str = "output", page_limit: int = 5) -> None:
    """
    Process a PDF file containing questionnaires and extract information using GPT-4V.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_dir (str): Directory to store the output files (default: "output")
        page_limit (int): Maximum number of pages to process (default: 5)
        
    Output Structure:
        Creates a timestamped batch directory containing:
        - images/: Directory with PNG images of each page
        - texts/: Directory with individual markdown files for each page
        - combined_results.md: Combined report with all pages
        
    Note:
        - Images are saved as high-quality PNGs
        - Each page's text is saved separately and also included in the combined report
        - The combined report includes links to the individual images
    """
    # Create output directory structure
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_dir = os.path.join(output_dir, f"batch_{timestamp}")
    os.makedirs(batch_dir, exist_ok=True)
    
    # Create subdirectories for images and individual extractions
    images_dir = os.path.join(batch_dir, "images")
    texts_dir = os.path.join(batch_dir, "texts")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(texts_dir, exist_ok=True)
    
    # Process the PDF
    print("Opening PDF...")
    try:
        pdf_document = fitz.open(pdf_path)
        total_pages = min(len(pdf_document), page_limit)
        
        # Create combined markdown file
        combined_md = os.path.join(batch_dir, "combined_results.md")
        
        print(f"Processing {total_pages} pages...")
        with open(combined_md, 'w', encoding='utf-8') as md_file:
            md_file.write("# Questionnaire Results\n\n")
            
            for page_num in range(total_pages):
                print(f"Processing page {page_num + 1}...")
                md_file.write(f"## Page {page_num + 1}\n\n")
                
                try:
                    # Convert PDF page to PIL Image
                    page = pdf_document.load_page(page_num)
                    image = pdf_page_to_pil(page)
                    
                    # Optimize image if needed
                    max_size = 4000  # Maximum dimension for API compatibility
                    if max(image.size) > max_size:
                        ratio = max_size / max(image.size)
                        new_size = tuple(int(dim * ratio) for dim in image.size)
                        image = image.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Save individual image
                    image_path = os.path.join(images_dir, f"page_{page_num + 1}.png")
                    image.save(image_path, "PNG", quality=100)
                    
                    # Analyze with GPT-4 Vision
                    analysis_result = analyze_image_with_gpt4(image)
                    
                    # Save individual text extraction
                    text_path = os.path.join(texts_dir, f"page_{page_num + 1}.md")
                    with open(text_path, 'w', encoding='utf-8') as text_file:
                        text_file.write(f"# Page {page_num + 1} Extraction\n\n")
                        text_file.write(analysis_result + "\n")
                    
                    # Add to combined markdown
                    md_file.write(analysis_result + "\n\n")
                    md_file.write(f"[View Image](images/page_{page_num + 1}.png)\n\n")
                    md_file.write("---\n\n")
                    
                except Exception as e:
                    error_msg = f"Error processing page {page_num + 1}: {str(e)}"
                    print(error_msg)
                    md_file.write(f"{error_msg}\n\n---\n\n")
        
        pdf_document.close()
        print(f"""Processing complete. Results saved to:
- Combined results: {combined_md}
- Individual images: {images_dir}
- Individual texts: {texts_dir}""")
        
    except Exception as e:
        print(f"Error opening PDF: {str(e)}")
        return

if __name__ == "__main__":
    pdf_path = "data/d1.pdf"
    process_pdf(pdf_path, page_limit=2) 