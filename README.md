# FLAMeS Inference

This package reduces the complexity of using FLAMeS, a model for multiple sclerosis lesion segmentation from a single FLAIR image, into one intuitive command.

[FLAMeS official website](https://zenodo.org/records/17955359]).

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

## Using Google Colab

If you use colab, check the "FLAMeS_Inference_in_Colab.ipynb" notebook for detailed instructions.

## Help

Run the following command to view all available options and capabilities:

```bash
flames-inference --help
```
