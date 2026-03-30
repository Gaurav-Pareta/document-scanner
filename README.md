# 📄 Document Scanner and Enhancer

A simple Computer Vision project that detects a document in an image, corrects its perspective, and converts it into a clean scanned version using OpenCV.

---

## 🎯 What This Project Does

* Detects a document from an image or webcam
* Fixes perspective (like CamScanner)
* Enhances the output (black & white, grayscale, sharpen)
* Saves the final scanned image

---

## ⚙️ Requirements

* Python 3.9 or above
* pip (Python package manager)
* Terminal / Command Prompt

---

## 📥 Installation

### 1. Open project folder

```bash
cd document_scanner
```

### 2. (Optional but recommended) Create virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

##  How to Run

### 🔹 Run with Image

```bash
python main.py --image images/image1.png
```

### 🔹 Save Output with Custom Name

```bash
python main.py --image images/image1.png --output output/scan.png
```

### 🔹 Choose Enhancement Mode

```bash
python main.py --image images/image1.png --mode adaptive
```

---

## Available Modes

| Mode      | Description                  |
| --------- | ---------------------------- |
| adaptive  | Black & white scan (default) |
| grayscale | Gray image                   |
| sharpen   | Sharpened color image        |

---

## Webcam Mode (Optional)

```bash
python main.py --webcam
```

Controls:

* Press **S** → Capture and scan
* Press **Q** → Quit

---

## 📂 Project Structure

```
document_scanner/
│
├── main.py          # Runs the program
├── scanner.py       # Core logic
├── utils.py         # Helper functions
├── config.py        # Parameters
├── images/          # Input images
└── output/          # Saved results
```

---

## ⚠️ Common Issues

**1. No document detected**

* Use clear images
* Ensure full document is visible

**2. Image not loading**

* Check file path
* Use correct file name

**3. Webcam not working**

* Close other apps using camera
* Try different camera index

---

## Concepts Used

* Image preprocessing (grayscale, blur)
* Edge detection (Canny)
* Contour detection
* Perspective transform (Homography)
* Image enhancement (thresholding, sharpening)

---

## Output

The scanned image will be saved in:

```
output/
```

---

## Summary

This project demonstrates how classical computer vision techniques can be used to build a real-world application like a document scanner without using heavy deep learning models.

---

## 📜 License

MIT
