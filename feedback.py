# query_audio_sentence.py

import os
import difflib
from pinecone import Pinecone
from groq import Groq

# ==============================
# 🔐 API KEYS
# ==============================

GROQ_API_KEY = "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"
PINECONE_API_KEY = "pcsk_6mcf8k_TYu6zfnGootEVau9B5Yp3axgshr7xVFRTQuVE27eHWXJmgbjG7SqmmY1zq99Zwc"
INDEX_NAME = "speech"

# ==============================
# 🔌 CONNECT SERVICES
# ==============================

groq_client = Groq(api_key=GROQ_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

print("✅ Connected successfully")

# ==============================
# 🎧 AUDIO INPUT
# ==============================

audio_path = input("\nEnter audio file path: ").strip().replace('"', '')

if not os.path.exists(audio_path):
    print("❌ File not found")
    exit()

# ==============================
# 🎤 AUDIO → TEXT
# ==============================

print("\n🎤 Transcribing audio...")

with open(audio_path, "rb") as file:
    transcription = groq_client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3"
    )

recognized_text = transcription.text
print("\n📝 Recognized Text:")
print(recognized_text)

# ==============================
# 🔎 FETCH ALL VECTORS
# ==============================

print("\n🔎 Fetching stored sentences from Pinecone...")

stats = index.describe_index_stats()

if stats["total_vector_count"] == 0:
    print("❌ No vectors found in Pinecone.")
    exit()

# Since Pinecone doesn't allow full scan easily,
# we query with a small random vector to get matches
results = index.query(
    vector=[0.1] * 768,
    top_k=100,
    include_metadata=True
)

if not results["matches"]:
    print("❌ No sentences retrieved.")
    exit()

# ==============================
# 🔎 FIND BEST MATCH USING TEXT SIMILARITY
# ==============================

best_sentence = ""
best_score = 0

for match in results["matches"]:
    sentence = match["metadata"].get("sentence", "")

    similarity = difflib.SequenceMatcher(
        None,
        recognized_text.lower(),
        sentence.lower()
    ).ratio()

    if similarity > best_score:
        best_score = similarity
        best_sentence = sentence

print("\n🎯 Expected Sentence:")
print(best_sentence)

print("\n📊 Sentence Similarity Score:", round(best_score, 4))

# ==============================
# 🔎 WORD-LEVEL ANALYSIS
# ==============================

recognized_words = recognized_text.lower().split()
expected_words = best_sentence.lower().split()

print("\n🔍 Word-Level Analysis\n")

for i in range(min(len(recognized_words), len(expected_words))):

    similarity = difflib.SequenceMatcher(
        None,
        recognized_words[i],
        expected_words[i]
    ).ratio()

    similarity = round(similarity, 4)

    if similarity > 0.9:
        severity = "Low"
        feedback = "Excellent pronunciation."
    elif similarity > 0.7:
        severity = "Medium"
        feedback = "Good attempt. Try clearer articulation."
    else:
        severity = "High"
        feedback = "Needs improvement. Practice slowly."

    print(f"Word {i+1}: {expected_words[i]}")
    print("Similarity:", similarity)
    print("Severity:", severity)
    print("Feedback:", feedback)
    print("-" * 60)

print("✅ Evaluation completed.")