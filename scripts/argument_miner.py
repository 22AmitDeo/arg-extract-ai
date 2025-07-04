# argument_miner.py

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load your Gemini 2.0 API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini 2.0 endpoint (based on your screenshot)
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Output folder
OUTPUT_DIR = Path("arguments_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_arguments_from_text(text, filename, page_number):
    """
    Sends a prompt to Gemini 2.0 Flash and extracts arguments from academic text.
    """
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
    }

    prompt = f"""
You are an AI assistant for academic research. Extract the core arguments from the given academic paragraph.

Identify and extract the following:
- Claim
- Evidence
- Conclusion

Respond ONLY in this JSON format:
{{
  "claim": "...",
  "evidence": "...",
  "conclusion": "...",
  "source": "{filename}",
  "page": {page_number}
}}

Text:
\"\"\"
{text}
\"\"\"
"""

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        # Get the generated content
        raw_text = data['candidates'][0]['content']['parts'][0]['text']

        # Attempt to parse as JSON
        return json.loads(raw_text)

    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        return {
            "error": str(e),
            "raw_response": data if 'data' in locals() else None,
            "source": filename,
            "page": page_number
        }


def process_file(filepath, page_number=1):
    """
    Reads a text file, extracts arguments using Gemini, and saves to output folder.
    """
    filename = filepath.stem
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    result = extract_arguments_from_text(text, filename, page_number)

    output_path = OUTPUT_DIR / f"{filename}_page{page_number}.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=2)

    print(f"[✓] Processed: {filepath.name} → {output_path.name}")


def main():
    input_dir = Path("extracted_text")
    if not input_dir.exists():
        print("❌ Folder 'extracted_text/' not found.")
        return

    text_files = list(input_dir.glob("*.txt"))
    if not text_files:
        print("⚠️ No .txt files found.")
        return

    for file in text_files:
        process_file(file, page_number=1)  # Extend later to detect actual pages


if __name__ == "__main__":
    main()
