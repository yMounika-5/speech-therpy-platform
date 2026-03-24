import numpy as np

embedding = np.load("audio_embeddings/sentence_1.npy")

print("Shape:", embedding.shape)
print("First 10 values:", embedding.flatten()[:10])
