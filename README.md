# ComfyUI AI Consistent Face Generator Setup

This directory contains a Python script converted from the `image-generator.ipynb` notebook. It automates the setup and execution of ComfyUI with specific models (RealVisXL, IP-Adapter) for consistent face generation.

## Prerequisites

- Python 3.10 or higher
- Git
- `curl` (usually installed by default on macOS/Linux)

## Usage

1.  Open your terminal in this directory.
2.  Run the setup script:

    ```bash
    python setup_and_run.py
    ```

## What the Script Does

1.  **Clones ComfyUI**: Downloads the core ComfyUI repository.
2.  **Installs Dependencies**: Installs required Python packages from `requirements.txt`.
3.  **Downloads Models**: Fetches large model files (~6GB+) needed for the workflow:
    - `RealVisXL_V4.safetensors`
    - `ip-adapter-plus-face_sdxl.safetensors`
    - `CLIP-ViT-H-14.safetensors`
4.  **Installs Custom Nodes**: automatically installs `ComfyUI-Manager` and `ComfyUI_IPAdapter_plus`.
5.  **Runs the Server**: Starts the ComfyUI server on `http://localhost:8188`.

## Notes for macOS Users

- The script attempts to interpret the notebook's logic for local execution.
- If you are on Apple Silicon (M1/M2/M3), PyTorch should automatically use MPS (Metal Performance Shaders) acceleration, but some specific CUDA optimizations (like `xformers`) are skipped as they are incompatible.
- The Cloudflare tunnel part of the original notebook is Linux-specific and is skipped on macOS. You can access the UI directly at `http://localhost:8188`.
