import os
import numpy as np
import pandas as pd

embedding_folder = "audio_embeddings"
all_embeddings = []

for file in sorted(os.listdir(embedding_folder)):
    if file.endswith(".npy"):
        path = os.path.join(embedding_folder, file)
        data = np.load(path)

        # Flatten (1,768) → (768,)
        vector = data.flatten()

        # Add filename as first column
        row = [file] + vector.tolist()
        all_embeddings.append(row)

# Create column names
columns = ["File_Name"] + [f"Dim_{i}" for i in range(768)]

df = pd.DataFrame(all_embeddings, columns=columns)

# Save to Excel
df.to_excel("audio_embeddings.xlsx", index=False)

print("✅ Excel file created: embeddings.xlsx")
