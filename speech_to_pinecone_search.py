import os
import sys
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# --- 1. THE FFMPEG BYPASS ---
# This tells Python exactly where to find the "engine" (FFmpeg) 
# even if Windows environment variables are not working.
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'

# --- 2. INITIALIZE AI MODELS (Python 3.14 Optimized) ---
print("⏳ Loading AI models (this takes a moment)...")
try:
    # Use 'tiny' for speed and low storage
    audio_model = whisper.load_model("tiny")
    # Semantic model for creating vector math
    embed_model = SentenceTransformer('all-mpnet-base-v2')
    print("✅ Models loaded successfully.")
except Exception as e:
    print(f"❌ Error loading models: {e}")

# --- 3. PINECONE CONNECTION ---
# Replace with your actual 2026 API key
pc = Pinecone(api_key="pcsk_6mcf8k_TYu6zfnGootEVau9B5Yp3axgshr7xVFRTQuVE27eHWXJmgbjG7SqmmY1zq99Zwc")
index = pc.Index("speech")

def process_audio(file_path):
    """Handles transcription and searching for a specific file."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        print(f"\n🎙️  Transcribing: {os.path.basename(file_path)}...")
        # fp16=False is REQUIRED for CPU-only processing in Python 3.14
        result = audio_model.transcribe(file_path, fp16=False)
        transcript = result['text'].strip()
        
        print(f"📝 Transcribed Text: \"{transcript}\"")
        print("\n--- ⏱️ TIMESTAMPS ---")
        for segment in result['segments']:
            print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s]: {segment['text']}")

        # Convert text to Vector
        print("\n🔎 Searching Pinecone for semantic match...")
        query_vector = embed_model.encode(transcript).tolist()
        
        # Query Pinecone
        search_results = index.query(vector=query_vector, top_k=1, include_metadata=True)

        if search_results['matches']:
            top_match = search_results['matches'][0]
            print(f"🎯 BEST MATCH FOUND: {top_match['metadata']['text']}")
            print(f"📊 ACCURACY SCORE: {top_match['score']:.4f}")
        else:
            print("❌ No matching sentences found in your database.")

    except Exception as e:
        print(f"⚠️ Transcription Error: {e}")
        print("💡 Hint: Ensure FFmpeg is installed at C:\\ffmpeg\\bin")

# --- 4. USER INTERFACE ---
if __name__ == "__main__":
    print("\n--- Day 4: Dynamic Speech Search (2026 Edition) ---")
    print("1. [R] Record New Audio (4 seconds)")
    print("2. [P] Provide File Path (Enter a .wav path)")
    
    mode = input("\nChoose an option (R/P): ").strip().upper()

    if mode == 'R':
        filename = "dynamic_input.wav"
        fs = 44100
        print("🎙️  SPEAK NOW...")
        recording = sd.rec(int(4 * fs), samplerate=fs, channels=1)
        sd.wait()
        write(filename, fs, recording)
        print(f"✅ Saved to {filename}")
        process_audio(filename)
    
    elif mode == 'P':
        path = input("📂 Paste the full path to your .wav file: ").strip()
        # Clean the path string in case of quotes
        path = path.replace('"', '').replace("'", "")
        process_audio(path)
    
    else:
        print("❌ Invalid selection. Please restart and choose R or P.")