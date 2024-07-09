# This script reads a file, tokenizes its content using the GPT-2 tokenizer (which is very similar to GPT-4's tokenizer for English text), and prints the total number of tokens.
from transformers import GPT2Tokenizer

def count_tokens(filename):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # GPT-2 and GPT-4 tokenization are similar
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    tokens = tokenizer.tokenize(content)
    return len(tokens)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    print(f"Total tokens: {count_tokens(filename)}")
