import os
import glob
import subprocess
import torch
from pathlib import Path

def download_synthstrip(output_dir):
    """Downloads mri_synthstrip script and weights."""
    synthstrip_dir = os.path.join(output_dir, "synthstrip")
    os.makedirs(synthstrip_dir, exist_ok=True)
    
    script_url = "https://raw.githubusercontent.com/freesurfer/freesurfer/dev/mri_synthstrip/mri_synthstrip"
    model_url = "https://surfer.nmr.mgh.harvard.edu/docs/synthstrip/requirements/synthstrip.1.pt"
    
    script_path = os.path.join(synthstrip_dir, "mri_synthstrip")
    model_path = os.path.join(synthstrip_dir, "synthstrip.1.pt")
    
    if not os.path.exists(script_path):
        print("Downloading mri_synthstrip...")
        subprocess.run(["wget", "-O", script_path, script_url], check=True)
    
    if not os.path.exists(model_path):
        print("Downloading synthstrip.1.pt...")
        subprocess.run(["wget", "-O", model_path, model_url], check=True)
        
    return script_path, model_path

def batch_synthstrip(input_dir, output_dir, use_gpu=True):
    """
    Runs SynthStrip on all NIfTI files in a directory.
    """
    # Ensure dependencies available
    synthstrip_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # package root roughly
    # Actually let's put synthstrip in the current working dir or a user specified resource dir
    # For now, let's put it in the output_dir parent or similar to keep it self contained per run, 
    # or better: a cache dir. For simplicity based on notebook, it used local dir.
    
    # We will use the output directory's parent for tools if not specified, 
    # or just use a dedicated tools folder in the output workspace.
    tools_dir = os.path.join(output_dir, "tools")
    script_path, model_path = download_synthstrip(tools_dir)

    if use_gpu:
        if not torch.cuda.is_available():
            print("⚠️ Warning: GPU requested but not available. Falling back to CPU for skull stripping.")
            use_gpu = False

    os.makedirs(output_dir, exist_ok=True)
    files = glob.glob(os.path.join(input_dir, "*.nii.gz"))
    
    if not files:
        # Try .nii if .nii.gz not found
        files = glob.glob(os.path.join(input_dir, "*.nii"))

    print(f"Processing {len(files)} files for Skull Stripping from '{input_dir}'...")

    for f in files:
        filename = os.path.basename(f)
        # Output filename as per notebook: stripped{filename} or we can keep it clean
        # Notebook used: strippedpatient...
        output_filename = f"stripped_{filename}"
        output_path = os.path.join(output_dir, output_filename)

        cmd = [
            "python", script_path,
            "-i", f,
            "-o", output_path,
            "--model", model_path,
            "--no-csf"
        ]

        if use_gpu:
            cmd.append("--gpu")

        try:
            print(f"Skull stripping {filename}...")
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Saved at {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error on {filename}: {e.stderr.decode()}")
            
    return output_dir
