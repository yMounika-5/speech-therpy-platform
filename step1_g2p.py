import pandas as pd
import nltk
from g2p_en import G2p
import re

# Download required resources (first time only)
#pcsk_5TUEw2_6gTGxTiDRSNqvPqpWz8VeNy51kszey8nUt9fT7nXDe5tBD1AgTctZ81YHi8dJuV
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

g2p = G2p()

# Load your exact Excel structure
df = pd.read_excel("sentence.xlsx")

word_level_data = []

for _, row in df.iterrows():

    name = row["Name"]                # ✔ correct column
    sentence = str(row["Sentence"]).strip()

    # Extract clean words (remove punctuation)
    words = re.findall(r'\b\w+\b', sentence)

    for word in words:
        phonemes = g2p(word)
        phonemes = [p for p in phonemes if p.strip() != ""]

        word_level_data.append({
            "Name": name,
            "Sentence": sentence,
            "Word": word.lower(),
            "Phonemes": " ".join(phonemes)
        })

# Create DataFrame
word_df = pd.DataFrame(word_level_data)

# Save output
word_df.to_excel("word_level_dataset.xlsx", index=False)

print("✅ Word-level dataset with Name created successfully!")
