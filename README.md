# Document Scanner and Enhancer

A command-line tool that uses classical computer vision (OpenCV) to find a document in a photo, apply a perspective correction (homography), and save an enhanced “scan” (adaptive threshold, grayscale, or sharpen).

Use this document if you have never seen the project before: it explains how to set up the environment, install dependencies, configure optional settings, and run everything from a terminal.

---

## Prerequisites

- **Python** 3.9 or newer (3.10+ recommended).
- **pip** (comes with Python on Windows/macOS; on Linux, install `python3-pip` if needed).
- A **terminal** (PowerShell, Command Prompt, or bash). All normal usage is driven by command-line arguments.
- **Optional:** a webcam only if you use `--webcam`. Image-only runs need no camera.

No separate database, API keys, or GUI installer are required.

---

## 1. Get the code

Clone the repository or extract the project folder. Open a terminal and go to the **repository root** (the folder that contains `main.py`, `requirements.txt`, and this `README.md`).

```bash
cd path/to/document_scanner
```

---

## 2. Virtual environment (recommended)

Isolating dependencies avoids conflicts with other Python projects.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see the virtual environment name in your shell prompt. To leave the environment later, run `deactivate`.

---

## 3. Install dependencies

With the virtual environment activated (if you use one):

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs **OpenCV** (`opencv-python`) and **NumPy**, which are required.

---

## 4. Configuration (optional)

Default behavior is controlled in `config.py` (blur sizes, Canny thresholds, output folder names, etc.). You do **not** need to change anything for a first run.

- Default output directory: `output/`
- Default output filename when using `--image`: `output/scan.png`

Override the output path with `-o` / `--output` as shown below.

---

## 5. Run the project (command line)

The entry point is `main.py`. Show all options:

```bash
python main.py -h
```

### 5.1 Process a single image (no GUI required)

Put an image under `images/` (sample files may include `image1.png`, `image2.png`, `image3.jpeg`). Run **without** `--visualize` so no display window is needed (suitable for automated or SSH environments):

```bash
python main.py --image images/image1.png --output output/scan.png --mode adaptive
```

**Enhancement modes** (`--mode`):

| Mode        | Description                          |
|------------|---------------------------------------|
| `adaptive` | Scan-like black and white (default)   |
| `grayscale`| Grayscale output                      |
| `sharpen`  | Color sharpen filter                  |

If your environment has a display and you want a side-by-side preview window:

```bash
python main.py --image images/image1.png --output output/scan.png --visualize
```

Close the preview window when finished; the saved file remains on disk.

### 5.2 Webcam mode (requires display and camera)

```bash
python main.py --webcam --mode adaptive
```

- Press **`s`** to capture the current frame, run the scanner, and save under `output/scan_YYYYMMDD_HHMMSS.png`.
- Press **`q`** to quit.

If you have multiple cameras, try another index:

```bash
python main.py --webcam --camera 1
```

---

## 6. Project layout

```
.
├── main.py          # CLI entry point
├── scanner.py       # Detection, warp, enhancement
├── utils.py         # I/O and visualization helpers
├── config.py        # Tunable constants
├── requirements.txt
├── images/          # Place input images here
└── output/          # Saved scans (created if missing)
```

---

## 7. Troubleshooting

| Issue | What to try |
|--------|----------------|
| `No document detected` | Use a photo where the full page edges are visible with decent contrast; avoid heavy glare. |
| `Image not found` | Check the path to `--image`; use quotes if the path contains spaces. |
| `Unable to access webcam` | Close other apps using the camera; try `--camera 0`, `1`, or `2`. |
| Import errors | Ensure the virtual environment is activated and `pip install -r requirements.txt` completed successfully. |

---

## Concepts used

- Grayscale, Gaussian blur, bilateral filtering  
- Canny edges, morphology, contour finding, quadrilateral approximation  
- Point ordering and homography (`getPerspectiveTransform`, `warpPerspective`)  
- Adaptive thresholding and simple sharpening  

---

## License

MIT
