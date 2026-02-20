import os
import torch

def check_gpu():
    """Checks if GPU is available."""
    if torch.cuda.is_available():
        print("✅ GPU is available.")
        return True
    else:
        print("❗ GPU not available. Running on CPU might be slow.")
        return False

def set_env_vars(base_dir):
    """Sets environment variables for nnUNet."""
    os.environ["nnUNet_raw"] = os.path.join(base_dir, "nnUNet_raw")
    os.environ["nnUNet_preprocessed"] = os.path.join(base_dir, "nnUNet_preprocessed")
    os.environ["nnUNet_results"] = os.path.join(base_dir, "nnUNet_results")
    
    for key in ["nnUNet_raw", "nnUNet_preprocessed", "nnUNet_results"]:
        os.makedirs(os.environ[key], exist_ok=True)
        print(f"Set {key}={os.environ[key]}")
