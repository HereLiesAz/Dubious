import os
import subprocess
import argparse
import sys
from pathlib import Path

def log(message):
    """Prints a message with a timestamp, proving we exist in linear time."""
    print(f"[DUBIOUS] {message}")

def check_gpu():
    """Checks if we have access to a GPU, or if we are suffering on a CPU."""
    import torch
    if torch.cuda.is_available():
        log(f"GPU Detected: {torch.cuda.get_device_name(0)}. fast_mode = True")
        return True
    else:
        log("No GPU detected. We are running on pure silicon grit. Expect delays.")
        return False

def lobotomize_audio(input_path, output_dir):
    """
    Separates the soul (vocals) from the body (instruments).
    Uses Facebook's Demucs model.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        log(f"Error: Input file {input_path} does not exist. Reality is broken.")
        sys.exit(1)

    log(f"Beginning separation of {input_file.name}...")
    
    # We use 'htdemucs' (Hybrid Transformer) because it is faster on CPU.
    # --two-stems=vocals tells it we only care about 'voice' vs 'everything else'.
    cmd = [
        "python", "-m", "demucs.separate",
        "-n", "htdemucs",
        "--two-stems=vocals",
        str(input_file),
        "-o", str(output_dir)
    ]

    try:
        subprocess.run(cmd, check=True)
        log("Separation complete. The subject is now divided.")
    except subprocess.CalledProcessError as e:
        log(f"Surgery failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Dubious Audio Processor")
    parser.add_argument("--input", required=True, help="Path to the victim video file")
    parser.add_argument("--output", default="separated", help="Directory to store the remains")
    
    args = parser.parse_args()
    
    check_gpu()
    lobotomize_audio(args.input, args.output)

if __name__ == "__main__":
    main()
      
