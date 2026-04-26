# 🔍 Advanced Image Forgery Detection

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-19.2-61DAFB.svg?logo=react)
![Flask](https://img.shields.io/badge/Flask-3.1-000000.svg?logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green.svg?logo=opencv)

A robust, full-stack web application designed to automatically detect and highlight **Copy-Move Forgeries** in digital images. Built with a modern React frontend and a powerful Python/Flask backend powered by OpenCV.

## 📖 Overview

In the era of accessible digital manipulation tools, verifying the authenticity of an image is increasingly difficult. Copy-move forgery—where one region of an image is copied and pasted elsewhere within the same image to hide or duplicate objects—is one of the most common tampering techniques.

This application uses the **Scale-Invariant Feature Transform (SIFT)** and advanced displacement vector clustering to mathematically identify identical duplicated regions, even if they have been slightly altered, and highlights the tampered areas directly for the user.

## ✨ Key Features

- **High-Accuracy Forgery Detection:** Utilizes SIFT keypoint detection to find up to 5,000 distinct feature points per image.
- **Advanced Vector Clustering:** Reduces false positives by ensuring duplicated pixels move in the exact same spatial vector, distinguishing between natural repeating textures (like grass) and actual manipulated clones.
- **Real-Time Visualizations:** Automatically draws clear cyan connecting lines and red indicator dots between identical regions.
- **Modern User Interface:** A clean, responsive React frontend with intuitive drag-and-drop image uploading.
- **Fast & Scalable API:** Lightweight Flask backend with CORS support and Gunicorn capability for production deployment.

## 🛠️ Technology Stack

**Frontend**
- React 19 (via Vite)
- pure CSS for styling
- React Icons for iconography

**Backend**
- Python 3.8+
- Flask & Flask-CORS
- OpenCV (cv2) for Computer Vision algorithms
- NumPy for matrix and spatial math

## 🧠 How the Algorithm Works

1. **Grayscale Conversion:** The uploaded image is decoded and converted to grayscale for texture analysis.
2. **SIFT Feature Extraction:** The algorithm extracts high-contrast keypoints.
3. **Self-Matching:** Descriptors are matched against themselves using the Brute Force Matcher (L2 Norm).
4. **Lowe's Ratio Test & Spatial Thresholding:** Weak matches and points that are naturally too close to each other are discarded.
5. **Displacement Vector Clustering:** The `(dx, dy)` shifts of the remaining matches are calculated. If 4 or more matches share the exact same movement vector (within a 15-pixel tolerance), they are flagged as a confirmed copy-move forgery.

## 🚀 Installation & Setup

### Prerequisites
Make sure you have [Node.js](https://nodejs.org/) and [Python 3.8+](https://www.python.org/) installed on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Image-Forgery-Detection.git
cd Image-Forgery-Detection
```

### 2. Setup the Backend (Python/Flask)
Navigate to the backend directory and set up a virtual environment:
```bash
cd backend
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```
*The backend will now be running on `http://localhost:5000`*

### 3. Setup the Frontend (React/Vite)
Open a new terminal window, navigate to the frontend directory:
```bash
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
*The frontend will now be running on `http://localhost:5173` (or the port specified by Vite).*

## 💻 Usage

1. Open your browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
2. Click the upload zone or drag and drop an image you suspect has been tampered with.
3. Wait a few seconds while the backend processes the image using the SIFT algorithm.
4. The result will be displayed on screen. If a forgery is detected, the tampered regions will be visibly connected by lines.

## 🎓 Academic Alignment

This project practically implements core syllabus topics from modern **Computer Vision** curricula, specifically demonstrating mastery over:
- Feature Detection and Extraction
- Feature Descriptors
- Euclidean Distance Matching
- Algorithmic Optimization (Vector Clustering)

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
