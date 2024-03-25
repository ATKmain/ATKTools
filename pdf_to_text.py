# PDF to text file converter (and extract all its images)
# dep:  pip install pymupdf
import fitz  # PyMuPDF
import os
import re  # Regular expressions library

def extract_content_from_pdf(pdf_path):
    """
    Extracts text and images from a PDF file, saving the text to a .txt file
    and images to a subfolder named after the PDF file.
    Removes multiple consecutive empty lines in text, leaving only one.

    Args:
    pdf_path (str): The file path of the PDF to be converted.
    """
    # Open the PDF file
    document = fitz.open(pdf_path)

    # Prepare to collect text
    text = ''

    # Prepare directory for images
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    img_dir = os.path.join(os.path.dirname(pdf_path), f"{base_name}_images")
    os.makedirs(img_dir, exist_ok=True)

    # Iterate through each page in the PDF
    for page_num in range(len(document)):
        # Get the page
        page = document.load_page(page_num)

        # Extract text
        text += page.get_text() + "\n"

        # Extract images
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(page.get_images(full=True)):
            # Extract the image bytes
            base_image = document.extract_image(img[0])
            image_bytes = base_image["image"]

            # Construct image file path
            image_path = os.path.join(img_dir, f"{base_name}_page_{page_num+1}_img_{image_index+1}.png")

            # Save the image
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)

    # Clean the text from multiple empty lines
    text = re.sub(r'\n\s*\n', '\n\n', text)

    # Save the text to a file
    text_file_path = os.path.splitext(pdf_path)[0] + '.txt'
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

    print(f"Text extracted and saved to {text_file_path}")
    print(f"Images extracted and saved to {img_dir}")

# Example usage
pdf_path = 'C:/Users/xxx/yyy.pdf'  # Replace this with the path to your PDF file
extract_content_from_pdf(pdf_path)

