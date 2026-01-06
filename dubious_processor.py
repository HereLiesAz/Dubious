import argparse
import json
import subprocess
from pathlib import Path
import sys
import whisper
from dubious_scoring import MoralCompass

def log(msg):
    print(f"[DUBIOUS CORE] {msg}")

def process_media(input_path, output_dir):
    input_file = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Initialize Tools
    log("Loading Whisper Model (base)...")
    model = whisper.load_model("base") # 'base' is fast and runs on CPU reasonably well
    
    log("Calibrating Moral Compass...")
    compass = MoralCompass()
    
    # 2. Transcribe
    log(f"Transcribing {input_file.name}...")
    result = model.transcribe(str(input_file))
    
    # 3. Analyze & Score
    log("Analyzing script for sin...")
    segments_data = []
    
    for seg in result["segments"]:
        text = seg["text"].strip()
        start = seg["start"]
        end = seg["end"]
        
        # Judge the text
        scores = compass.judge_text(text)
        
        # Generate Dubious alternative if necessary
        dubious_text = text
        if max(scores.values()) > 0:
            dubious_text = compass.suggest_replacement(text, scores)
            
        segment_entry = {
            "id": seg["id"],
            "start_ms": int(start * 1000),
            "end_ms": int(end * 1000),
            "original_text": text,
            "dubious_text": dubious_text,
            "scores": scores,
            "action": "replace" if max(scores.values()) > 0 else "passthrough"
        }
        segments_data.append(segment_entry)

    # 4. Generate .dps File
    dps_data = {
        "meta": {
            "title": input_file.stem,
            "duration": result["segments"][-1]["end"],
            "version": "1.0"
        },
        "timeline": segments_data
    }
    
    dps_path = output_dir / f"{input_file.stem}.dps"
    with open(dps_path, 'w', encoding='utf-8') as f:
        json.dump(dps_data, f, indent=2)
        
    log(f"Dubious Performance Script generated: {dps_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    
    process_media(args.input, args.output)

if __name__ == "__main__":
    main()
