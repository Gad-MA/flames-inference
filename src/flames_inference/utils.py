import os
import torch
import re

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

def validate_filename(filename):
    """
    Validates if the given filename follows the format `CASE_IDENTIFIER_0000.nii.gz`.

    Args:
        filename (str): The filename to validate.

    Returns:
        bool: True if the filename is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9]+_[0-9]+_0000\.nii\.gz$"
    return bool(re.match(pattern, filename))

# Example usage:
# print(validate_filename("brain_001_0000.nii.gz"))  # True
# print(validate_filename("invalid_name.nii.gz"))    # False
