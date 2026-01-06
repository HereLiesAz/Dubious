# **DUBIOUS: The Reality Filter // Project Blueprint**

"Reality is just a suggestion. We provide the edit."

## **I. The Vision**

**Dubious** is not just a censorship tool; it is an active intervention in media consumption. It decouples the *intent* of a scene from its *execution*. By using AI to analyze, score, and rewrite dialogue, Dubious allows the user to act as the final editor of reality, down-mixing toxicity into palatability.

It operates on the principle of the **Sanitized Simulacrum**: We accept that the media is fake, so we might as well make it fake in a way that suits us.

### **The Modes**

1. **Player Mode:** You provide the video file. Dubious plays it, ducking the original audio and injecting AI-performed lines where necessary.  
2. **Companion Mode:** You watch Netflix on TV. Your phone listens, syncs, and acts as a "Safe Speaker," overdubbing the profanity in real-time.  
3. **Export Mode:** You generate a "Dubious Edit" audio track or script to share with others.

## **II. The Architecture**

### **1\. The Backend ( The Factory )**

* **Location:** GitHub Actions (Serverless, Free).  
* **Role:** Heavy lifting.  
  * **Input:** Video URL or Audio File.  
  * **Process:**  
    1. **Transcription:** OpenAI Whisper (Speech-to-Text).  
    2. **Judgment:** Custom MoralCompass algorithm scores every sentence (0-5) on Profanity, Violence, and Sexual content.  
    3. **Rewrite:** (Future) LLM generates sanitary alternatives.  
  * **Output:** .dps (Dubious Performance Script) JSON file.

### **2\. The Frontend ( The Stage )**

* **Location:** GitHub Pages (Static Hosting).  
* **Tech Stack:** Svelte 5 \+ Vite (PWA).  
* **Role:** Playback & Performance.  
  * **Engine:** Web Speech API (TTS) for real-time dubbing.  
  * **Logic:** Reads .dps, monitors playback time, ducks volume, speaks lines based on user tolerance settings.

### **3\. The Data (.dps)**

The "Soul" of the content. A lightweight JSON map of sin.

{  
  "meta": { "title": "Pulp Fiction", "duration": 9240 },  
  "timeline": \[  
    {  
      "start\_ms": 14500, "end\_ms": 16000,  
      "original": "Bad word.", "dubious": "Good word.",  
      "scores": { "profanity": 4, "violence": 1 }  
    }  
  \]  
}

## **III. File Structure & Implementation**

### **A. Repository Layout**

/ (Root)  
├── .github/workflows/  
│   ├── dub\_job.yml          \# Backend Automation  
│   └── deploy\_frontend.yml  \# Frontend Deployment  
├── backend/  
│   ├── dubious\_processor.py \# The Logic  
│   ├── dubious\_scoring.py   \# The Conscience  
│   └── requirements.txt     \# The Tools  
├── frontend/  
│   ├── src/  
│   │   ├── lib/  
│   │   │   ├── DubiousPlayer.svelte  
│   │   │   ├── DubiousCompanion.svelte  
│   │   │   └── audioExport.js  
│   │   ├── App.svelte  
│   │   └── main.js  
│   └── package.json  
└── README.md

### **B. Core Code Blocks**

#### **1\. Backend: The Judge (backend/dubious\_scoring.py)**

import re

class MoralCompass:  
    def \_\_init\_\_(self):  
        self.lexicon \= {  
            "damn": (1,0,0), "hell": (1,0,0), "ass": (2,0,1),  
            "shit": (3,0,0), "fuck": (4,1,1), "kill": (0,3,0)  
        }  
        self.replacements \= {  
            "fuck": "fudge", "shit": "shoot", "kill": "hug",  
            "ass": "rear", "damn": "darn", "hell": "heck"  
        }

    def judge(self, text):  
        scores \= {'p': 0, 'v': 0, 's': 0}  
        for word in re.findall(r'\\b\\w+\\b', text.lower()):  
            if word in self.lexicon:  
                p, v, s \= self.lexicon\[word\]  
                scores\['p'\] \= max(scores\['p'\], p)  
                scores\['v'\] \= max(scores\['v'\], v)  
                scores\['s'\] \= max(scores\['s'\], s)  
        return scores

    def sanitize(self, text, scores):  
        if max(scores.values()) \== 0: return text  
        new\_text \= text  
        for bad, good in self.replacements.items():  
            new\_text \= re.sub(f"(?i){bad}", good, new\_text)  
        return new\_text

#### **2\. Backend: The Processor (backend/dubious\_processor.py)**

import whisper  
import json  
from dubious\_scoring import MoralCompass

def process(input\_file):  
    model \= whisper.load\_model("base")  
    result \= model.transcribe(input\_file)  
    compass \= MoralCompass()  
    timeline \= \[\]

    for seg in result\["segments"\]:  
        scores \= compass.judge(seg\["text"\])  
        dub\_text \= compass.sanitize(seg\["text"\], scores)  
        if max(scores.values()) \> 0:  
            timeline.append({  
                "start\_ms": int(seg\["start"\] \* 1000),  
                "end\_ms": int(seg\["end"\] \* 1000),  
                "original": seg\["text"\],  
                "dubious": dub\_text,  
                "scores": scores  
            })

    return {"timeline": timeline}

#### **3\. Frontend: The Player (frontend/src/lib/DubiousPlayer.svelte)**

\<script\>  
  export let src;  
  export let script;  
  let video, currentTime;  
  let settings \= { profanity: 1 }; // User Tolerance  
  const synth \= window.speechSynthesis;

  $: if (script && currentTime) {  
    const event \= script.timeline.find(e \=\>   
      currentTime \>= e.start\_ms/1000 && currentTime \< e.end\_ms/1000  
    );  
    if (event && event.scores.p \> settings.profanity && \!synth.speaking) {  
      video.volume \= 0.1; // Duck Audio  
      const utter \= new SpeechSynthesisUtterance(event.dubious);  
      synth.speak(utter);  
    } else if (\!event) {  
      video.volume \= 1.0; // Restore  
    }  
  }  
\</script\>

\<video bind:this={video} {src} bind:currentTime controls /\>  
\<input type="range" min="0" max="5" bind:value={settings.profanity} /\>

## **IV. The Roadmap (Future Directions)**

### **Phase 1: Practical Improvements (The "Must Haves")**

1. **Audio Fingerprinting:** Currently, "Companion Mode" relies on manual sync or luck. We need to implement a browser-based audio fingerprinting system (WASM) to listen to the TV and lock onto the timestamp automatically.  
2. **Better Voices:** Browser TTS is robotic. We should add a feature to the Backend to generate **Voice Clones** (using Coqui TTS) and pack them into the .dps file as mp3 blobs, so the phone plays high-quality acting, not a robot.  
3. **Community Database:** A centralized Repo where users can upload/download .dps files for popular movies, creating the "Dubious Library."

### **Phase 2: Conceptual Expansions (The "God Mode")**

1. **Therapy Mode:** Instead of removing profanity, it rewrites arguments to be using "Non-Violent Communication" (NVC). It turns a toxic fight into a constructive dialogue.  
2. **The Gaslight Feature:** A mode that subtly changes the plot. Characters who died actually survived. Endings are changed. The user experiences a Mandella Effect in real-time.  
3. **Educational Mode:** Rewrites complex Shakespearean or scientific dialogue into "ELI5" (Explain Like I'm 5\) language for kids, while keeping the visual context.

## **V. Next Actions**

1. **Initialize the Git Repo** with the folder structure above.  
2. **Paste the Code** into the respective files.  
3. **Push to GitHub** to trigger the first Deploy Action.  
4. **Test** with the "Jen & Az" argument clip.
