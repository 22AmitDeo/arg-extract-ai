# main.py

import os
import json
from pathlib import Path
from scripts.extract_text import extract_clean_text
from scripts.argument_miner import extract_arguments_from_text
from scripts.upload_to_drive import upload_file_to_drive

# Define project paths
PDF_DIR = Path("pdfs")
TEXT_DIR = Path("extracted_text")
ARG_DIR = Path("arguments_output")

# Ensure necessary folders exist
TEXT_DIR.mkdir(exist_ok=True)
ARG_DIR.mkdir(exist_ok=True)


def run_text_extraction():
    print("📄 Step 1: Extracting text from PDFs...\n")
    for pdf_file in PDF_DIR.glob("*.pdf"):
        output_json_path = TEXT_DIR / (pdf_file.stem + ".json")
        print(f"[✓] Processing {pdf_file.name}")
        extract_clean_text(pdf_file, output_json_path)


def run_argument_extraction():
    print("\n🧠 Step 2: Extracting arguments from text...\n")
    for text_file in TEXT_DIR.glob("*.json"):
        with open(text_file, "r", encoding="utf-8") as f:
            pages = json.load(f)

        for page_data in pages:
            page_text = page_data.get("text", "")
            page_num = page_data.get("page", 1)

            if not page_text.strip():
                print(f"[!] Skipping empty page {page_num} in {text_file.name}")
                continue

            result = extract_arguments_from_text(
                page_text, text_file.stem, page_num
            )

            output_path = ARG_DIR / f"{text_file.stem}_page{page_num}.json"
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(result, out, indent=2)

            print(f"[✓] Arguments saved: {output_path.name}")


def run_upload():
    print("\n☁️ Step 3: Uploading results to Google Drive...\n")
    for arg_file in ARG_DIR.glob("*.json"):
        print(f"[→] Uploading {arg_file.name}...")
        try:
            upload_file_to_drive(arg_file)
            print(f"[✓] Uploaded: {arg_file.name}")
        except Exception as e:
            print(f"[X] Failed to upload {arg_file.name}: {e}")


def main():
    print("🔁 Starting full pipeline...\n")

    if not PDF_DIR.exists():
        print("❌ 'pdfs/' folder not found.")
        return

    run_text_extraction()
    run_argument_extraction()
    run_upload()

    print("\n🎉 All tasks completed successfully!")


if __name__ == "__main__":
    main()
