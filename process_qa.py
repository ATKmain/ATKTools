import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI


def process_single_response(text):
    """Process a single questionnaire response and return structured data."""
    prompt = f"""Extract information from this GCC Breakout Questionnaire response.
The questionnaire typically contains:
1. Name & Function field
2. Questions about GCC opportunities and scaling
3. Additional comments or notes

Format the response EXACTLY as follows (keep these exact headings):

## Respondent Information

### Question: Name & Function
**Answer:** [Extract the name and function/role]

### Question: Please specify what opportunities do you see to establish GCC?
**Answer:** [Their response about GCC opportunities]

### Question: Please specify what opportunities do you see to scale &/or transform GCC?
**Answer:** [Their response about scaling/transforming GCC]

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
            {
                "role": "system", 
                "content": "You are a precise assistant that extracts questionnaire responses. Always maintain the exact question headings as provided in the prompt. If information is missing, indicate with '[No response provided]'."
            },
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
        qa_pairs = {
            "Name & Function": "[No response]",
            "Opportunities to establish GCC": "[No response]",
            "Opportunities to scale/transform GCC": "[No response]"
        }
        
        current_question = None
        lines = markdown_text.split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith('### Question:'):
                current_question = line.replace('### Question:', '').strip()
            elif line.startswith('**Answer:**') and current_question:
                answer = line.replace('**Answer:**', '').strip()
                
                if "Name & Function" in current_question:
                    qa_pairs["Name & Function"] = answer
                elif "opportunities do you see to establish GCC" in current_question:
                    qa_pairs["Opportunities to establish GCC"] = answer
                elif "opportunities do you see to scale" in current_question:
                    qa_pairs["Opportunities to scale/transform GCC"] = answer
        
        # Only return if we have at least a name
        if qa_pairs["Name & Function"] != "[No response]":
            return qa_pairs
        return None
        
    except Exception as e:
        print(f"Error extracting data for Excel: {str(e)}")
        return None


def main():
    # Load environment variables
    load_dotenv()

    # Define the paths and settings
    input_path = "data/extracted_text.json"
    markdown_path = "qa_extracted.md"
    excel_path = "qa_responses.xlsx"
    
    # Set to None to process all pages, or a number for limited testing
    page_limit = 5  # Process only first 5 pages for testing
    
    try:
        # Load the extracted text
        print(f"Loading extracted text from {input_path}...")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_pages = data['total_pages']
        pages_text = data['pages']

        # Apply page limit if specified
        if page_limit:
            print(f"\nTEST MODE: Processing only first {page_limit} pages...")
            pages_to_process = min(page_limit, total_pages)
            pages_text = pages_text[:pages_to_process]
        else:
            print(f"\nProcessing all {total_pages} pages...")
            pages_to_process = total_pages

        # Process each page and collect responses
        all_responses = []
        excel_data = []
        
        for i, page_text in enumerate(pages_text, 1):
            print(f"Processing response {i} of {pages_to_process}...")
            response_text = process_single_response(page_text)
            all_responses.append(response_text)
            
            # Extract data for Excel
            qa_data = extract_data_for_excel(response_text)
            if qa_data:
                excel_data.append(qa_data)
            else:
                print(f"Warning: Could not extract data for Excel from response {i}")

        # Add suffix to output files in test mode
        if page_limit:
            markdown_path = markdown_path.replace('.md', '_test.md')
            excel_path = excel_path.replace('.xlsx', '_test.xlsx')

        # Write markdown file
        print("\nWriting markdown file...")
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write("# GCC Breakout Questionnaire Responses\n\n")
            if page_limit:
                f.write(f"This document contains the first {pages_to_process} responses from the GCC Breakout Questionnaire (TEST MODE).\n\n")
            else:
                f.write("This document contains organized responses from the GCC Breakout Questionnaire.\n\n")
            f.write("---\n\n")
            f.write("\n---\n\n".join(all_responses))

        # Create Excel file
        if excel_data:
            print("Creating Excel file...")
            df = pd.DataFrame(excel_data)
            # Reorder columns to put Name first
            columns = ["Name & Function", "Opportunities to establish GCC", "Opportunities to scale/transform GCC"]
            df = df[columns]
            df.to_excel(excel_path, index=False, sheet_name="Questionnaire Responses")
        else:
            print("Warning: No data was extracted for Excel file")

        print(f"\nFiles saved:")
        print(f"- Markdown: {markdown_path}")
        if excel_data:
            print(f"- Excel: {excel_path}")
        
        if page_limit:
            print(f"\nTest mode completed. Review the output files and if they look good, set page_limit = None to process all pages.")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 