import os
import subprocess
import sys
import time
import platform
import shutil

def run_command(command, cwd=None, ignore_errors=False):
    """Execution helper that prints the command being run."""
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        if not ignore_errors:
            sys.exit(1)

def download_file(url, path):
    """Download a file using curl (available on Mac/Linux)."""
    if os.path.exists(path):
        print(f"File {path} already exists. Skipping download.")
        return
    
    print(f"Downloading {url} to {path}...")
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    run_command(f"curl -L \"{url}\" -o \"{path}\"")

def main():
    base_dir = os.getcwd()
    comfy_dir = os.path.join(base_dir, "ComfyUI")
    
    print("--- 🚀 Starting ComfyUI Setup Script ---")

    # Step 1: Clone ComfyUI
    if not os.path.exists(comfy_dir):
        print("Step 1: Cloning ComfyUI...")
        run_command("git clone https://github.com/comfyanonymous/ComfyUI")
    else:
        print("Step 1: ComfyUI directory already exists.")
    
    os.chdir(comfy_dir)
    
    # Step 2: Install dependencies
    print("\nStep 2: Installing dependencies...")
    # xformers is often specific to NVIDIA/Linux. Skip or optional on Mac.
    if platform.system() == "Linux":
        print("Installing xformers (Linux)...")
        run_command(f"{sys.executable} -m pip install -q xformers==0.0.28.post1 --no-deps", ignore_errors=True)
    
    print("Installing requirements.txt...")
    run_command(f"{sys.executable} -m pip install -q -r requirements.txt")

    # Step 3: Create necessary directories
    print("\nStep 3: Creating directories...")
    os.makedirs("models/checkpoints", exist_ok=True)
    os.makedirs("models/ipadapter", exist_ok=True)
    os.makedirs("models/clip_vision", exist_ok=True)

    # Step 4: Download RealVisXL model
    print("\nStep 4: Downloading RealVisXL model (this may take a while)...")
    download_file(
        "https://civitai.com/api/download/models/361593",
        "models/checkpoints/RealVisXL_V4.safetensors"
    )

    # Step 5: Download IP-Adapter models
    print("\nStep 5: Downloading IP-Adapter models...")
    download_file(
        "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors",
        "models/ipadapter/ip-adapter-plus-face_sdxl.safetensors"
    )
    download_file(
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors",
        "models/clip_vision/CLIP-ViT-H-14.safetensors"
    )

    # Step 6: Install ComfyUI Manager
    print("\nStep 6: Installing ComfyUI Manager...")
    if not os.path.exists("custom_nodes/ComfyUI-Manager"):
        run_command("git clone https://github.com/ltdrdata/ComfyUI-Manager.git", cwd="custom_nodes")
    else:
        print("ComfyUI Manager already installed.")

    # Step 7: Install IP-Adapter nodes
    print("\nStep 7: Installing IP-Adapter nodes...")
    if not os.path.exists("custom_nodes/ComfyUI_IPAdapter_plus"):
        run_command("git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git", cwd="custom_nodes")
    else:
        print("ComfyUI IPAdapter plus already installed.")

    # Step 8: Run ComfyUI
    print("\nStep 8: Starting ComfyUI...")
    
    # Running ComfyUI
    cmd = [sys.executable, 'main.py', '--dont-print-server', '--listen', '0.0.0.0']
    
    print(f"Executing: {' '.join(cmd)}")
    print("⏳ Waiting for server to start...")

    try:
        # Start the process
        comfy_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True, # Read as text
            bufsize=1  # Line buffered
        )

        # Wait a bit
        time.sleep(5)
        print("✅ ComfyUI should be running now at http://localhost:8188")
        
        # Handle Cloudflare Tunnel (Linux specific in original notebook)
        if platform.system() == "Linux" and platform.machine() == "x86_64":
            print("\n🌐 Attempting to set up Cloudflare tunnel (Linux)...")
            if not os.path.exists("cloudflared-linux-amd64"):
                download_file("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "cloudflared-linux-amd64")
                run_command("chmod +x cloudflared-linux-amd64")
            
            print("Starting tunnel... (Check output for URL)")
            subprocess.Popen(["./cloudflared-linux-amd64", "tunnel", "--url", "http://localhost:8188"])

        # Stream output from ComfyUI
        while True:
            line = comfy_process.stdout.readline()
            if not line and comfy_process.poll() is not None:
                break
            if line:
                print(f"[ComfyUI] {line.strip()}")
                
    except KeyboardInterrupt:
        print("\nStopping ComfyUI...")
        comfy_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
