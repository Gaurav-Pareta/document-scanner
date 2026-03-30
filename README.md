# 📄 Document Scanner and Enhancer         

A simple Computer Vision project that detects a document in an image, corrects its perspective, and converts it into a clean scanned version using OpenCV.
                   
---
                  
## 🎯 Overview                        

When documents are captured using a camera, they often appear tilted, distorted, or affected by shadows and background noise.
                     
This project solves that problem by:                             
                   
* Detecting the document automatically                   
* Correcting its perspective (like CamScanner)                     
* Enhancing it to produce a clean, readable output                          

---                   
                         
## ✨ Features
                            
* Automatic document detection
* Perspective correction (Homography)                                               
* Edge detection using Canny
* Contour detection for boundary extraction                     
* Image enhancement (adaptive threshold, grayscale, sharpen)                        
* Supports image and webcam input                             
* Saves output automatically
                          
---
                    
## 🛠️ Technologies Used                

* Python
* OpenCV
* NumPy                                    

---
                                               
## 📂 Project Structure

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

## ⚙️ Installation

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

## ▶️ Usage

### 🔹 Run with image
                                         
```
python main.py --image images/doc1.jpg                                    
```

### 🔹 Run with webcam

```
python main.py --webcam
```

---
                                  
## 🎨 Modes

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

## 🧠 How It Works

The system follows these steps:
                                     
1. Convert image to grayscale and apply blur
2. Detect edges using Canny
3. Find contours and select document
4. Apply perspective transform (homography)
5. Enhance image for better readability
                          
---

## 📊 Results
               
The system works well for:

* Flat documents
* Tilted documents
* Documents with shadows
* Documents on different backgrounds

The output is a clean, scan-like image.

---

## ⚠️ Limitations

* May fail if document edges are not clear
* Sensitive to poor lighting conditions                        
* Not suitable for extremely distorted images

---

## 🚀 Future Improvements

* GUI interface
* PDF export
* Better shadow removal
* Deep learning-based detection

---

## 📌 Conclusion
                                         
This project demonstrates how classical Computer Vision techniques can be used to build a real-world application like a document scanner efficiently without using heavy models.

---                                            
                                                  
## 📜 License

MIT
