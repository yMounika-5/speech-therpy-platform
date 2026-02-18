import pandas as pd
import subprocess
import os

# Load word-level dataset
df = pd.read_excel("word_level_dataset.xlsx")

# Create audio folder
os.makedirs("word_audio", exist_ok=True)

model_path = "en_US-lessac-medium.onnx"

for i, row in df.iterrows():

    word = row["Word"]   # match exact column name
    word_id = f"word_{i+1}"

    output_path = f"word_audio/{word_id}.wav"

    command = [
        "piper",
        "--model", model_path,
        "--output_file", output_path
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(word.encode("utf-8"))

    print(f"Generated audio for: {word}")

print("✅ All word audio files generated!")
