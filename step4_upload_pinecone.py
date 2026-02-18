import numpy as np
import pandas as pd
from pinecone import Pinecone

# 🔑 Replace with your real API key
pc = Pinecone(api_key="pcsk_3z8pq8_PKhZu8iKmyFknV5C9uixxpkgid2pn7516RphFKayhTbUNwPDNRdmN6kX9hUo2Yj")

index = pc.Index("speechh")

df = pd.read_excel("word_level_dataset.xlsx")

for i, row in df.iterrows():
    word_id = f"word_{i+1}"
    embedding_path = f"word_embeddings/{word_id}.npy"

    embedding = np.load(embedding_path)

    vector = {
        "id": word_id,
        "values": embedding.tolist(),
        "metadata": {
            
            "Sentence": row["Sentence"],
            "Word": row["Word"],
            "Phonemes": row["Phonemes"]
        }
    }

    index.upsert(vectors=[vector])

    print("Uploaded:", row["Word"])

print("✅ All embeddings uploaded to Pinecone!")
