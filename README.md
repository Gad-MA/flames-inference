# FLAMeS Inference

FLAIR Lesion Analysis in Multiple Sclerosis inference pipeline.

## Installation

```bash
git clone https://github.com/Gad-MA/flames-inference.git
cd flames-inference
pip install -e .
```

## Usage

Place all the images you want to segment in a folder.

Make sure that all images follow the following naming format: `CASE_IDENTIFIER_0000.nii.gz`

Example input image names:
- `brain_001_0000.nii.gz`
- `brain_002_0000.nii.gz`

Then run the following commands:

```bash
export MPLBACKEND=Agg
flames-inference --input <input_folder_with_nifti_images> --output <output_folder>
```

## Help
```bash
flames-inference --help
```
