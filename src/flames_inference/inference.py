import os
import subprocess
from .utils import set_env_vars

def download_model(model_dir):
    """Downloads FLAMeS model from Zenodo."""
    os.makedirs(model_dir, exist_ok=True)
    
    # Check if model is already installed/downloaded
    # Zenodo record ID: 17955359. Will verify file "Dataset004_WML.zip" exists.
    
    # We might need to allow user to specify a cache dir for models
    # For now, we download to model_dir
    
    zip_path = os.path.join(model_dir, "Dataset004_WML.zip")
    if os.path.exists(zip_path):
        print(f"Model zip found at {zip_path}")
    else:
        print("Downloading FLAMeS model from Zenodo...")
        # zenodo_get is a CLI tool, we can use it via subprocess or import if available as library (it's a script usually)
        # Using subprocess for safety as it's installed via dependencies
        subprocess.run(["zenodo_get", "17955359", "-o", model_dir], check=True)
        
    return zip_path

def install_model(model_zip_path):
    """Installs the nnUNet model from zip."""
    print("Installing model from zip...")
    subprocess.run(["nnUNetv2_install_pretrained_model_from_zip", model_zip_path], check=True)

def run_inference(input_dir, output_dir, device='cuda'):
    """
    Runs nnUNetv2 inference.
    
    Args:
        input_dir: Directory containing preprocessed (skull-stripped) images.
        output_dir: Directory to save segmentation results.
        device: 'cuda' or 'cpu'. Note: nnUNet handles device via environment or flags usually, 
                but here we primarily ensure the command runs.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Dataset ID 004, Configuration 3d_fullres, Trainer nnUNetTrainer_8000epochs
    cmd = [
        "nnUNetv2_predict",
        "-i", input_dir,
        "-o", output_dir,
        "-d", "004",
        "-c", "3d_fullres",
        "-tr", "nnUNetTrainer_8000epochs"
    ]
    
    if device == 'cpu':
        cmd.append("--disable_tta") # TTA might be slow on CPU too, but specific device flag for nnUNet might be needed
        cmd.extend(["-device", "cpu"])

    print(f"Running inference on {input_dir} -> {output_dir}")
    subprocess.run(cmd, check=True)
