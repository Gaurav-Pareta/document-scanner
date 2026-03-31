# 📄 Scanner and Enhancer of documents

This is an easy Computer Vision project. The project automatically finds a document inside an image, corrects the perspective of that document so that it will look like a clean scanned document, and produces that result using OpenCV. 

---

## Overview

Many times, when you take a photo of a document with your camera, it ends up being skewed/twisted, warped, or has shadows or background noise in it after you take a shot.

This project will help to eliminate those issues with the following capabilities:

* is able to find and identify the document from the image.
* will allow you to adjust the perspective of the document in the same way as CamScanner would do.
* is capable of enhancing the image produced of the document to create a clean and legible image. 

---

## Features 

* automatically finds a document in an image.
* will allow you to correct artificial perspective (homography).
* will allow you to use Canny edge detection to find the edges of the document.
* contour detection can be used to extract outlines/boundaries of the document. 
* enhancing the document image can be accomplished through the use of adaptive thresholding, grayscale, sharpening, and/or various other techniques.
* takes pictures from either an image file or from a webcam.
* automatically saves a copy of the output document image. 

---

## Technologies Used 

* Python
* OpenCV
* NumPy
                                               
## Project Structure

```
document_scanner/
│
├── main.py          # Entry point
├── scanner.py       # Core logic
├── utils.py         # Helper functions                                        
├── config.py        # Parameters
├── images/          # Input images
└── output/          # Saved results
```

---                 

## Installation

### 1. Clone the repository                                                                  

```
git clone https://github.com/your-username/document-scanner.git
cd document-scanner
```

### 2. Install dependencies

```
pip install opencv-python numpy                                
```

---

## Usage

### 🔹 Run with image
                                         
```
python main.py --image images/doc1.jpg                                    
```

### 🔹 Run with webcam

```
python main.py --webcam
```

---
                                  
## Modes

| Mode      | Description                  |
| --------- | ---------------------------- |
| adaptive  | Black & white scan (default) |
| grayscale | Gray image                   |
| sharpen   | Sharpened image              |                          

Example:
                                     
```
python main.py --image images/doc1.jpg --mode adaptive
```

---

## The Workings of the System
The system has a number of steps to create the scanned image:

1) Convert image to greyscale and smooth (blur) the image.
2) Use the Canny edge detector to detect edges in the image.
3) Find the contours of the image so that we can select the document.
4) Apply a perspective transformation to the document (homography).
5) Enhance the document to ensure it is more readable.

---

## Output
Documents that the system will work on well:

* Flat documents
* Tilted documents
* Documents with shadows
* Documents with different background

Results produced by the system are clean, scanned-like images.

---

## Limitations

The system may not perform well when:

* The edge of the document is not clear to the camera.
* The lighting is poor.
* The documents are highly distorted.

---

## Future Improvements

Some future changes will include:

* A Graphical User Interface (GUI)
* Ability to export to PDF
* Better shadow removal
* Using deep learning models to detect the documents.

---

## Conclusion

In conclusion, this project demonstrates the ability to create a working application for scanning documents using classical Computer Vision techniques, using lightweight models.

---

## 📜 License

MIT
