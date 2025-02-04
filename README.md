# ATKTools

Welcome to ATKTools! This repository contains various scripts and tools that I (ATK) find useful. Feel free to explore, use, and contribute to the repository.

## Repository Structure

Here's the current structure of the repository:

```
ATKTools/
│
├── README.md
├── tmp/
│   └── [Temporary files go here]
├── data/
│   └── [Data files go here]
├── output/
│   └── batch_YYYYMMDD_HHMMSS/
│       ├── images/
│       │   └── [Extracted page images]
│       ├── texts/
│       │   └── [Individual page extractions]
│       └── combined_results.md
├── gpu_benchmark_tensorflow.py
├── gpu_benchmark_torch.py
├── json-converter.html
├── json-converter2.html
├── jsonstrin_to_json.py
├── md_to_docx.py
├── pdf_to_text.py
├── process_questionnaire.py
├── snake_continue_codelama70b2.py
├── snake_game_codelama70b.py
├── snake_game_gemeni_pro.py
├── snake_game_mixtral.py
├── snake_game_mixtral_ollama2.py
├── snake_game_Whitemartina.py
├── btc_cycles_comparison.py
├── btc_price_history.py
├── convertDocxToMD.py
├── token_count.py
```

## Description of Files

### Document Processing and AI
- **process_questionnaire.py**: Script to process scanned questionnaires using Azure OpenAI GPT-4o. Features:
  - Converts PDF pages to high-quality images
  - Uses GPT-4o Vision to extract handwritten text
  - Generates individual page extractions and images
  - Creates a combined markdown report
  - Organizes output in timestamped batches

- **extract_text.py**: Script to extract text from PDFs using Azure Document Intelligence. Features:
  - High-quality text extraction from PDFs
  - Handles multi-page documents
  - Saves extracted text in JSON format
  - Avoids repeated API calls by saving results

- **process_qa.py**: Script to process questionnaire responses using Azure OpenAI. Features:
  - Works with extract_text.py output
  - Formats responses in markdown and Excel
  - Supports test mode for validation
  - Creates organized Q&A pairs
  - Generates tabulated Excel summary

### Bitcoin Analysis
- **btc_cycles_comparison.py**: Script for comparing Bitcoin market cycles.
- **btc_price_history.py**: Script to fetch and analyze Bitcoin price history.

### Document Conversion
- **convertDocxToMD.py**: Script to convert DOCX files to Markdown format.
- **md_to_docx.py**: Script to convert Markdown files to DOCX format.
- **pdf_to_text.py**: Script to extract text from PDF files.

### GPU Benchmarking
- **gpu_benchmark_tensorflow.py**: Benchmarking script for TensorFlow on GPU.
- **gpu_benchmark_torch.py**: Benchmarking script for PyTorch on GPU.

### JSON Utilities
- **json-converter.html**: HTML file for a tool to convert JSON files.
- **json-converter2.html**: Another version of the JSON converter tool.
- **jsonstrin_to_json.py**: Script to convert JSON strings to JSON format.

### Snake Game Variants
- **snake_continue_codelama70b2.py**: Snake game implementation with Codelama70b2.
- **snake_game_codelama70b.py**: Snake game implementation with Codelama70b.
- **snake_game_gemeni_pro.py**: Snake game implementation with Gemeni Pro.
- **snake_game_mixtral.py**: Snake game implementation with Mixtral.
- **snake_game_mixtral_ollama2.py**: Snake game implementation with Mixtral Ollama2.
- **snake_game_Whitemartina.py**: Snake game implementation with Whitemartina.

### Miscellaneous
- **token_count.py**: Script to count tokens in a given input.

## Requirements

Different scripts may have different requirements. For specific requirements:

### process_questionnaire.py
```
python-dotenv==1.0.0
openai==1.12.0
PyMuPDF==1.23.26
Pillow==10.2.0
```

## Contributing

Contributions are welcome! If you have any useful scripts or tools that you would like to share, feel free to fork the repository and submit a pull request.

## License

This repository is open source and available under the [MIT License](LICENSE).
