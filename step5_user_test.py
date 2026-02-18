"""
-------------------------------------------------------
Step 5: User Pronunciation Test
Project: Intelligent Speech Therapy Platform
Developed by: Uttkarsh Raj
-------------------------------------------------------
"""

import os
import librosa
import torch
from pinecone import Pinecone
from transformers import AutoFeatureExtractor, HubertModel

# 🔑 Direct API key (same style as your earlier code)
pc = Pinecone(api_key="pcsk_3z8pq8_PKhZu8iKmyFknV5C9uixxpkgid2pn7516RphFKayhTbUNwPDNRdmN6kX9hUo2Yj")

# ⚠️ IMPORTANT:
# Put here the SAME index name used in Step 4
index = pc.Index("speechh")   # <-- Change if your index name is different

# ===============================
# 🔹 Load HuBERT Model
# ===============================

print("🔄 Loading HuBERT model...")

feature_extractor = AutoFeatureExtractor.from_pretrained(
    "facebook/hubert-base-ls960"
)
model = HubertModel.from_pretrained(
    "facebook/hubert-base-ls960"
)

print("✅ HuBERT Loaded Successfully")

# ===============================
# 🔹 Embedding Function
# ===============================

def get_embedding(audio_path):

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"❌ Audio file not found: {audio_path}")

    speech, sr = librosa.load(audio_path, sr=16000)

    inputs = feature_extractor(
        speech,
        sampling_rate=16000,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    return embedding


# ===============================
# 🔹 User Audio Path
# ===============================

user_audio_path = "user_test.wav"  # Keep file in project root

print("\n🎤 Testing pronunciation for Uttkarsh Raj")
print("📂 Audio File:", user_audio_path)

# ===============================
# 🔹 Generate Embedding
# ===============================

user_embedding = get_embedding(user_audio_path)

# ===============================
# 🔹 Similarity Search
# ===============================

result = index.query(
    vector=user_embedding.tolist(),
    top_k=1,
    include_metadata=True
)

match = result["matches"][0]

matched_word = match["metadata"].get("word", "Unknown")
score = match["score"]

# ===============================
# 🔹 Results
# ===============================

print("\n🔎 Closest Word:", matched_word)
print("📊 Similarity Score:", round(score, 3))

if score > 0.90:
    print("✅ Excellent pronunciation, Uttkarsh!")
elif score > 0.80:
    print("👍 Good pronunciation.")
elif score > 0.70:
    print("⚠️ Needs improvement.")
else:
    print("❌ Poor pronunciation.")

print("\n📈 Feedback complete for Uttkarsh Raj.")
