# 📜 EpigraphiX-AI: Neural Palm-Leaf Manuscript OCR & Epigraphical Intelligence Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MATLAB](https://img.shields.io/badge/MATLAB-R2021+-e16724?logo=mathworks&logoColor=white)](https://www.mathworks.com/products/matlab.html)

**EpigraphiX-AI** is an end-to-end State-of-the-Art (SOTA) **Epigraphical Computer Vision & Document Intelligence Platform** designed to restore, segment, transcribe, and evaluate severely degraded historical Malayalam and Grantha palm-leaf manuscripts (*Thaliyola*).

---

## 🔬 Key Features & Scientific Innovations

1. **Fiber-Aware Neural Inpainting (FANI)**: Detects and suppresses high-frequency cellulose fiber striations while preserving micro-stylus ink incisions.
2. **O(1) Integral-Image Adaptive Sauvola Binarization**: High-speed local thresholding running in $<5\text{ms}$.
3. **3D Surface Photometric Stereo (PTM)**: Interactive raking-light simulation to inspect stylus physical groove depths.
4. **Persistent Homology Betti Filtration (PHT-BF)**: Tracks topological loop invariants ($\beta_0, \beta_1$) to preserve ancient Grantha ligature loops.
5. **Adaptive Multi-Row Glyph & Word Segmentation**: Identifies natural text baseline lines and extracts character cuts and word envelopes.
6. **5-Model SOTA ML Decision Space**: Real-time 2D epigraphical feature extraction (Horizontal Projection Variance & Loop Curvature Entropy) evaluated across:
   - **Support Vector Machine (SVM)**
   - **Gaussian Naive Bayes (GNB)**
   - **Random Forest (100 Trees)**
   - **k-Nearest Neighbors (k-NN)**
   - **CNN Neural Lattice**
7. **Linguistic Decoder & Sandhi Grammar Engine**: DP Levenshtein alignment with Malayalam Trie lexicon search and trilingual semantic translation (Old/New Malayalam, English, Hindi).
8. **High-Resolution Vector PDF Report Export**: Generates printable evaluation reports with scorecard gauges and multi-model decision boundary charts.

---

## 🚀 Quick Start Guide

### Running the Web Studio Interface
1. Clone the repository:
   ```bash
   git clone https://github.com/oyadarsh-hue/EpigraphiX-AI.git
   cd EpigraphiX-AI/web_studio
   ```
2. Start the local server:
   ```bash
   python -m http.server 8080
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

---

## 🛠️ Tech Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas API (Pixel-Level Processing), Modern Glassmorphic CSS3, SVG Morphing.
- **Backend & Tooling**: Python 3 HTTP Microservices, Node.js Sandbox Test Suite, MATLAB Engine.
- **Algorithms**: Sauvola Adaptive Binarization, Sobel Vector Operators, Wagner-Fischer DP Alignment, Persistent Homology, PTM Photometric Stereo.

---

## 👨‍💻 Author

- **ADARSH S** — [@oyadarsh-hue](https://github.com/oyadarsh-hue)
