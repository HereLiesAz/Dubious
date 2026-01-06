# Dubious
###Censorship for Families 

## Overview
This tool generates a **Dubious Performance Script (.dps)** from a video file. It uses OpenAI's Whisper to transcribe the audio, analyzes the content for "Sin" (Profanity, Violence, Sexual content), and generates a sanitized replacement script.

## The Stack
- **Whisper:** Speech-to-Text.
- **Dubious Scoring:** Custom taxonomy for rating offensive content (0-5 scale).
- **GitHub Actions:** The compute engine.

## Usage (Local)
1. Install dependencies: `pip install -r requirements.txt`
2. Install FFmpeg (System requirement).
3. Run: `python dubious_processor.py --input video.mp4`

## Usage (Cloud)
1. Go to the **Actions** tab.
2. Select **Dubious Processing Unit**.
3. Enter the Direct URL to a video file.
4. Download the artifact (`.dps` file) when complete.
5. 
