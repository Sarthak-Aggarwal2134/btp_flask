from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_files = [f for f in request.files.values()]

    if not audio_files:
        return jsonify({'error': 'No audio files provided'}), 400

    results = []
    for file in audio_files:
        # Save the file securely
        filename = secure_filename(file.filename)
        audio_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(audio_path)

        # Call intonation.py to process the audio and get the json result
        result_file = subprocess.check_output(['python3', 'intonation.py', audio_path]).decode('utf-8').strip()

        # Read the generated JSON file
        with open(result_file, 'r') as f:
            result_data = f.read()

        # Print the result to terminal
        print(f"Result for {filename}: {result_data}")

        results.append(result_data)

        # Optionally delete the uploaded audio and generated JSON files
        # os.remove(audio_path)
        # os.remove(result_file)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
