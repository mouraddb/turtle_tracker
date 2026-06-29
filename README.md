# Turtle Tracker

Utilities and notebooks for turning extracted turtle pond frames into background-subtracted views and echogram-style summary images.

## Contents

- `echogram_tol.ipynb` - main thresholded echogram workflow. It samples evenly spaced frames to estimate the background, then streams frames one at a time to build `gifs/echogram_tol.png`.
- `echogram.ipynb` - non-thresholded echogram workflow using the same memory-friendly background sampling approach.
- `initial_detection.ipynb` - exploratory notebook for loading frames, subtracting the background, thresholding motion, and writing preview GIFs.
- `move_into_png_folder.py` - helper script that moves PNG frames from a recording folder into a `frames/` subfolder.
- `gifs/` - output directory for generated GIFs and echogram images.

## Expected Frame Layout

The notebooks expect a directory containing `.png` or `.jpg` frame files sorted by filename, for example:

```text
/Volumes/PortableSSD/tutrtletest/turtlepond_2026-06-29_111037/
  frame_002927_raw_rotated.png
  frame_002929_raw_rotated.png
  ...
```

Set `frame_dir` near the top of the notebook to the folder that contains the frame images.

## Setup

Use the existing `garmin-detect` environment, or install the notebook dependencies into your Python environment:

```bash
pip install numpy opencv-python matplotlib tqdm imageio jupyter
```

## Echogram Workflow

Open `echogram_tol.ipynb` and run the cells from top to bottom.

The main settings are:

```python
frame_dir = "/path/to/frame/folder"
num_frames = 11000
background_sample_count = 1000
frames_to_plot = 6
```

The notebook estimates the background from `background_sample_count` evenly spaced frames instead of loading every frame into memory. It then loops over the selected frames with a `tqdm` progress bar, subtracts the background, applies blur/thresholding, writes each echogram column, and discards the per-frame arrays.

Outputs are written under `gifs/`, including:

```text
gifs/echogram_tol.png
gifs/echogram.png
```

## Moving PNG Frames

If a recording folder contains PNG files directly and you want them inside a `frames/` subfolder:

```bash
python3 move_into_png_folder.py /path/to/recording-folder --dry-run
python3 move_into_png_folder.py /path/to/recording-folder
```

Use `--destination-dir /path/to/frames` to choose a custom destination.
