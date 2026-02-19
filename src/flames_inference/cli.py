import argparse
import os
import sys
from pathlib import Path
from .utils import check_gpu, set_env_vars
from .preprocessing import batch_synthstrip
from .inference import download_model, install_model, run_inference

def main():
    parser = argparse.ArgumentParser(description="FLAMeS Inference CLI")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input directory containing NIfTI images (.nii.gz or .nii)")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output directory for segmentation masks")
    parser.add_argument("--model-cache", type=str, default=None, help="Directory to cache/store the model (default: <output>/flames_model)")
    parser.add_argument("--skip-preprocessing", action="store_true", help="Skip skull stripping (if inputs are already stripped)")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"], help="Device to use (cuda/cpu)")
    
    args = parser.parse_args()
    
    input_dir = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output)
    
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
        
    os.makedirs(output_dir, exist_ok=True)
    
    print("====================================")
    print("       FLAMeS Inference CLI         ")
    print("====================================")
    
    # Check GPU
    has_gpu = check_gpu()
    if args.device == "cuda" and not has_gpu:
        print("Switching to CPU mode as GPU is not available.")
        args.device = "cpu"

    # Setup Environment
    # nnUNet requires specific env vars. We'll set them relative to output/working directory 
    # to keep it self contained easily for the user without global pollution if possible.
    # Or maybe a dedicated workspaces dir. 
    # Let's use a subdirectory in output_dir for 'nnUNet_work_dir' to keep things organized.
    work_dir = os.path.join(output_dir, "work_dir")
    set_env_vars(work_dir)
    
    # 1. Preprocessing
    if args.skip_preprocessing:
        print("Skipping preprocessing as requested.")
        preprocessed_dir = input_dir
    else:
        print("\n[Stage 1/2] Preprocessing (Skull Stripping)...")
        # We save stripped images to a subdir in output
        preprocessed_dir = os.path.join(output_dir, "skull_stripped")
        batch_synthstrip(input_dir, preprocessed_dir, use_gpu=(args.device == "cuda"))
        
    # 2. Inference
    print("\n[Stage 2/2] Inference (Lesion Segmentation)...")
    
    # Model setup
    model_base = args.model_cache if args.model_cache else os.path.join(output_dir, "flames_model")
    model_zip = download_model(model_base)
    
    # We need to verify if the model is already installed in nnUNet structure.
    # nnUNet stores installed models in nnUNet_results.
    # We can perform installation safely; nnUNet handles existing models (might prompt? no, typically command line works)
    # The command `nnUNetv2_install_pretrained_model_from_zip` might fail if already exists or just overwrite.
    # Let's hope it checks. If not, we might check if dataset ID 004 exists in results.
    
    dataset_id = "Dataset004_WML"
    installed_path = os.path.join(os.environ["nnUNet_results"], dataset_id)
    if not os.path.exists(installed_path):
        install_model(model_zip)
    else:
        print(f"Model {dataset_id} appears to be installed.")

    # Run Prediction
    final_output_dir = os.path.join(output_dir, "segmentations")
    run_inference(preprocessed_dir, final_output_dir, device=args.device)
    
    print("\n====================================")
    print(f"Processing complete! Results saved to: {final_output_dir}")
    print("====================================")

if __name__ == "__main__":
    main()
