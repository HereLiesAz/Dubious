# Dubious - Censorship for Families 
*Because reality is just a suggestion.*

## **Overview**

**Dubious** is an auditory hallucination engine. It decouples the intent of a performance from its execution.

By utilizing AI (Whisper, Demucs, and TTS), Dubious analyzes the prosody of an original audio track and allows for the seamless injection of alternate dialogue. Whether used for **High-Fidelity Dubbing**, **Language Localization**, or **Content Sanitation** (censorship), the goal remains the same: to create a simulacrum so convincing that the viewer forgets they are being lied to.

## **The Architecture**

The system is divided into two distinct lobes:

1. **The Backend (The Factory):** A Python-based analysis engine that performs the auditory lobotomy. It separates stems, transcribes text, measures emotional intensity, and generates the **Dubious Performance Script (.dps)**.  
2. **The Frontend (The Stage):** A Svelte-based PWA (Progressive Web App) that acts as the playback client. It reads the .dps and synthesizes the new reality in real-time.

## **Setup & Usage**

### **1\. The Backend (Local Analysis)**

If you prefer to run the surgery on your own silicon rather than GitHub's.

**Prerequisites:**

* Python 3.10+  
* FFmpeg (installed and on your system PATH)

**Installation:**

cd backend  
pip install \-r requirements.txt

Operation:  
To generate a .dps file from a video:  
python dubious\_processor.py \--input path/to/video.mp4 \--output ../frontend/public/scripts/

### **2\. The Frontend (The Player)**

The interface for consuming the altered media.

**Prerequisites:**

* Node.js 20+

**Installation:**

cd frontend  
npm install

Operation:  
To run the local development server:  
npm run dev

Open http://localhost:5173 in your browser.

## **The .dps Protocol**

The **Dubious Performance Script** is the DNA of the edit. It is a JSON file that maps time to truth.

{  
  "meta": { "title": "Example" },  
  "timeline": \[  
    {  
      "start\_ms": 12000,  
      "end\_ms": 14000,  
      "original\_text": "I reject your reality.",  
      "dubious\_text": "I accept your cookies.",  
      "scores": { "profanity": 0, "violence": 5 }  
    }  
  \]  
}

## **Modes of Deception**

1. **Player Mode:** Load a video file directly into the browser. The app ducks the original audio and overlays the synthetic performance based on the .dps.  
2. **Companion Mode:** Watch media on an external screen (TV/Laptop). The app runs on your phone, listening to the room audio. When it hears the target phrase, it overrides the room audio with the sanitized dub via the phone speakers.

## **Deployment**

Pushing to the main branch triggers the GitHub Action deploy\_frontend.yml, which builds the PWA and serves it via GitHub Pages.

