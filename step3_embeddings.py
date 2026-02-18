import torch
import librosa
import os
import numpy as np
import pandas as pd
from transformers import AutoFeatureExtractor, HubertModel

# Load HuBERT model
feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/hubert-base-ls960")
model = HubertModel.from_pretrained("facebook/hubert-base-ls960")

# Create embedding folder
os.makedirs("word_embeddings", exist_ok=True)

# Load dataset
df = pd.read_excel("word_level_dataset.xlsx")

def get_embedding(audio_path):
    speech, sr = librosa.load(audio_path, sr=16000)
    inputs = feature_extractor(
        speech,
        sampling_rate=16000,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

for i, row in df.iterrows():
    word_id = f"word_{i+1}"
    audio_path = f"word_audio/{word_id}.wav"

    if not os.path.exists(audio_path):
        print("Missing:", audio_path)
        continue

    embedding = get_embedding(audio_path)

    np.save(f"word_embeddings/{word_id}.npy", embedding)

    print("Embedded:", row["Word"])

print("✅ All embeddings generated!")
