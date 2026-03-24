import pandas as pd
from g2p_en import G2p
import nltk

# Ensure the resources are there
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

g2p = G2p()

input_file = "input_sentences.xlsx"
df = pd.read_excel(input_file)

phoneme_list = []

for sentence in df["Sentence"]:
    # Get raw phonemes
    raw_phonemes = g2p(str(sentence))
    
    # UNIQUE STEP: Clean out punctuation and extra spaces
    # This keeps only the actual sounds (AA, R, T, etc.)
    clean_phonemes = [p for p in raw_phonemes if p.strip() and p not in ['.', ',', '!', '?']]
    
    phoneme_list.append(" ".join(clean_phonemes))

df["Expected_Pronunciation"] = phoneme_list

# Save to the same folder
output_file = "output_phonemes.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Conversion complete! Saved {len(df)} rows to {output_file}")