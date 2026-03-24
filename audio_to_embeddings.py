import os
import torch
import librosa
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Load model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

audio_folder = "audio"
embedding_folder = "audio_embeddings"

os.makedirs(embedding_folder, exist_ok=True)

for file in os.listdir(audio_folder):

    if file.endswith(".wav"):

        audio_path = os.path.join(audio_folder, file)
        print(f"Processing {file}...")

        # Load audio using librosa
        speech, sample_rate = librosa.load(audio_path, sr=16000)

        input_values = processor(
            speech,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_values

        with torch.no_grad():
            outputs = model(input_values)

        # Mean pooling
        embedding = outputs.last_hidden_state.mean(dim=1)

        # Save embedding
        embedding_path = os.path.join(
            embedding_folder,
            file.replace(".wav", ".npy")
        )

        np.save(embedding_path, embedding.numpy())

print("All embeddings generated successfully!")
