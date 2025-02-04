import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from openai import AzureOpenAI
import base64
from PIL import Image
import io
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    # Save as PNG with maximum quality
    image.save(buffered, format="PNG", quality=100, optimize=False)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image_with_gpt4(image):
    """Analyze image using GPT-4 Vision"""
    base64_image = encode_image_to_base64(image)
    
    system_message = """You are an expert at analyzing questionnaire images and extracting information with high accuracy. 
    Your task is to carefully read and transcribe handwritten text from questionnaire images.
    You must be thorough and precise in your extraction, paying special attention to handwritten text.
    Format your response in a clear, structured markdown format."""

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

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # This should be set to your GPT-4V deployment name
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
        temperature=0.3,  # Lower temperature for more accurate responses
        max_tokens=4000   # Increased token limit for more detailed responses
    )
    
    return response.choices[0].message.content

def pdf_page_to_pil(page):
    """Convert PDF page to PIL Image"""
    # Get the page's pixmap with high resolution
    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
    
    # Convert pixmap to PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def process_pdf(pdf_path, output_dir="output", page_limit=5):
    """Process PDF and generate markdown output"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamp for this batch
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a subdirectory for this processing batch
    batch_dir = os.path.join(output_dir, f"batch_{timestamp}")
    os.makedirs(batch_dir, exist_ok=True)
    
    # Create subdirectories for images and individual extractions
    images_dir = os.path.join(batch_dir, "images")
    texts_dir = os.path.join(batch_dir, "texts")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(texts_dir, exist_ok=True)
    
    # Open the PDF
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
                    max_size = 4000  # Maximum dimension
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