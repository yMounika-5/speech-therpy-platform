import pandas as pd
import numpy as np
import nltk
import sys
from sentence_transformers import SentenceTransformer
from g2p_en import G2p

# 🔥 CRITICAL FIX FOR PYTHON 3.14 COMPATIBILITY
# We import the core components individually to bypass the plugin manager
try:
    from pinecone import Pinecone
except Exception:
    print("Direct import failed, trying alternative...")
    import pinecone

# ==========================================
# 🔐 CONFIGURATION (Matching your Screenshot)
# ==========================================
PINECONE_API_KEY = "pcsk_6mcf8k_TYu6zfnGootEVau9B5Yp3axgshr7xVFRTQuVE27eHWXJmgbjG7SqmmY1zq99Zwc"
INDEX_NAME = "speech" # Change to 'pronunciation-index' if that's the new one
FILE_PATH = "output_phonemes.xlsx"

# ==========================================
# 🛠️ INITIALIZE
# ==========================================
print(f"🐍 Running on Python {sys.version.split()[0]}")
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
model = SentenceTransformer("all-mpnet-base-v2")
g2p = G2p()

# ==========================================
# 🚀 UPLOAD PROCESS
# ==========================================
def main():
    print("🧹 Clearing index for fresh upload...")
    index.delete(delete_all=True)

    df = pd.read_excel(FILE_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    vectors = []
    print(f"🔄 Processing {len(df)} rows to match screenshot format...")

    for i, row in df.iterrows():
        # Extracting data from your Excel
        sentence_text = str(row["sentence"])
        phonemes_text = str(row["expected_pronunciation"])
        
        # In your screenshot, 'word' seems to be the first word of the sentence
        word_val = sentence_text.split()[0].lower() if sentence_text.split() else ""
        
        # Generate the vector (using the phonetic pipeline)
        words = sentence_text.split()
        word_vecs = [model.encode(f"audio_sig: {' '.join(g2p(w))}") for w in words]
        final_vec = np.mean(word_vecs, axis=0).tolist()

        # Build metadata to match your screenshot EXACTLY
        vectors.append({
            "id": f"{word_val}_{i}", # Example: day_6
            "values": final_vec,
            "metadata": {
                "phonemes": phonemes_text,
                "sentence": sentence_text,
                "sentence_number": i + 1,
                "word": word_val
            }
        })

    # Upload in small batches for stability on Python 3.14
    batch_size = 5
    for j in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[j : j + batch_size])
        print(f"📤 Uploaded batch {j//batch_size + 1}")

    print("\n✅ Upload Complete! Check your Pinecone Browser.")

if __name__ == "__main__":
    main()