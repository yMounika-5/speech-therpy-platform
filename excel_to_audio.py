import pandas as pd
import subprocess
import os
import re

EXCEL_FILE = "input_sentences.xlsx"
OUTPUT_DIR = "audio"
MODEL_PATH = "en_US-lessac-medium.onnx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel(EXCEL_FILE)

audio_count = 1  # continuous numbering for audio files

for sentence in df["Sentence"]:

    # Skip NaN or empty cells silently
    if pd.isna(sentence):
        continue

    sentence = str(sentence).strip()
    if not sentence:
        continue

    # Clean sentence
    clean_sentence = re.sub(r"[^\w\s]", "", sentence)
    clean_sentence = re.sub(r"\s+", " ", clean_sentence).strip()

    if not clean_sentence:
        continue

    output_file = os.path.join(OUTPUT_DIR, f"sentence_{audio_count}.wav")

    subprocess.run(
        [
            "piper",
            "--model", MODEL_PATH,
            "--output_file", output_file
        ],
        input=clean_sentence,
        text=True
    )

    audio_count += 1

print("✅ Audio generated only for valid sentences")