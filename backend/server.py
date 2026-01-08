import os
import json
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dubious_processor import process_media

app = Flask(__name__)
CORS(app)

# Use absolute paths or relative to the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'temp_uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'temp_output')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online", "system": "Dubious Factory"})

@app.route('/api/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    try:
        print(f"Processing {filename}...")
        # Run the processor
        # process_media expects (input_path, output_dir)
        # It generates {input_stem}.dps in output_dir
        process_media(input_path, OUTPUT_FOLDER)

        # Find the generated file
        base_name = os.path.splitext(filename)[0]
        dps_filename = f"{base_name}.dps"
        dps_path = os.path.join(OUTPUT_FOLDER, dps_filename)

        if not os.path.exists(dps_path):
             return jsonify({"error": "Generation failed to produce output"}), 500

        with open(dps_path, 'r', encoding='utf-8') as f:
            dps_data = json.load(f)

        # Cleanup
        try:
            os.remove(input_path)
            os.remove(dps_path)
        except:
            pass

        return jsonify(dps_data)

    except Exception as e:
        print(f"Error processing video: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Dubious Factory Server on port 5000...")
    app.run(debug=True, port=5000)
