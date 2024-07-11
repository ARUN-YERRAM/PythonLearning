from flask import Flask, request, jsonify
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import torch

app = Flask(_name_)

# Load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

# Function to load and preprocess the audio file
def load_audio(file_path):
    audio, sampling_rate = librosa.load(file_path, sr=16000)  # Load and resample to 16kHz
    return audio, sampling_rate

# Function to chunk audio
def chunk_audio(audio, chunk_length=30):
    sampling_rate = 16000
    chunk_length_samples = chunk_length * sampling_rate
    return [audio[i:i + chunk_length_samples] for i in range(0, len(audio), chunk_length_samples)]

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    try:
        if 'file_path' not in request.json:
            return jsonify({"error": "Missing file_path parameter"}), 400

        file_path = request.json['file_path']
        
        # Verify if the file exists
        try:
            audio, sampling_rate = load_audio(file_path)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404

        audio_chunks = chunk_audio(audio)

        full_transcription = []

        for chunk in audio_chunks:
            input_features = processor(chunk, sampling_rate=sampling_rate, return_tensors="pt").input_features
            predicted_ids = model.generate(input_features)  # Adjust parameters if needed
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            full_transcription.append(transcription)

        final_transcription = " ".join(full_transcription)

        return jsonify({"transcription": final_transcription})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    app.run(debug=True