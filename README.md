# 📜 EpigraphiX-AI: Neural Palm-Leaf Manuscript OCR & Epigraphical Intelligence Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MATLAB](https://img.shields.io/badge/MATLAB-R2021+-e16724?logo=mathworks&logoColor=white)](https://www.mathworks.com/products/matlab.html)

**EpigraphiX-AI** is an end-to-end State-of-the-Art (SOTA) **Epigraphical Computer Vision & Document Intelligence Platform** designed to restore, segment, transcribe, and evaluate severely degraded historical Malayalam and Grantha palm-leaf manuscripts (*Thaliyola*).

---

## 🔬 Key Features & Scientific Innovations

1. **Fiber-Aware Neural Inpainting (FANI 2.0)**: Directional morphological decomposition suppresses high-frequency cellulose fiber striations while preserving micro-stylus ink incisions.
2. **Epigraphical Super-Resolution (Real-ESRGAN / DI)**: High-frequency sub-band unsharp masking and stylus groove sharpening for heavily degraded palm leaves.
3. **O(1) Integral-Image Adaptive Sauvola Binarization**: High-speed local thresholding running in $<5\text{ms}$.
4. **TrOCR Vision Transformer & Multi-Head Self-Attention**: Transformer-based sequence recognition and attention heatmap extraction over ancient Grantha & Malayalam ligatures.
5. **Persistent Homology Betti Filtration (PHT-BF)**: Tracks topological loop invariants ($\beta_0, \beta_1$) to preserve ligature holes and Euler characteristics.
6. **3D Surface Photometric Stereo (PTM)**: Interactive raking-light simulation to inspect stylus physical groove depths.
7. **Adaptive Multi-Row Glyph & Word Segmentation**: Identifies natural text baseline lines and extracts character cuts and word envelopes.
8. **5-Model SOTA ML Decision Space & CNN Neural Lattice**: Support Vector Machine (SVM), Gaussian Naive Bayes (GNB), Random Forest (100 Trees), k-NN, and CNN Neural Lattice.
9. **Linguistic Decoder & Sandhi Grammar Trie**: DP Levenshtein alignment with Malayalam Trie lexicon search and trilingual semantic translation (Old/New Malayalam, English, Hindi).
10. **High-Resolution Vector PDF Report Export**: Generates printable evaluation reports with scorecard gauges and multi-model decision boundary charts.

---

## 🚀 Quick Start Guide

### 1. Running the Automated Python Pipeline & Test Suite
```bash
# Run full automated verification on sample palm-leaf manuscripts
python test_pipeline.py

# Run standalone TrOCR Vision Transformer Engine
python trocr_transformer_engine.py

# Run Epigraphical Restoration & Super-Resolution
python epigraphical_enhancer.py
```

### 2. Running the Web Studio Interface
1. Navigate to the web studio:
   ```bash
   cd web_studio
   ```
2. Start the local server:
   ```bash
   python -m http.server 8080
   ```
3. Open your browser at `http://localhost:8080`

---

## 🛠️ Tech Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas API (Pixel-Level Processing), Modern Glassmorphic CSS3, SVG Morphing.
- **Backend & Tooling**: Python 3.9+, OpenCV, NumPy, Scipy, ReportLab, Node.js Sandbox Test Suite, MATLAB Engine.
- **Deep Learning & Algorithms**: TrOCR Vision Transformer Attention, Sauvola Integral Adaptive Binarization, FANI 2.0 Inpainting, Wagner-Fischer DP Trie Alignment, Persistent Homology Betti Topology, PTM Photometric Stereo.

---

## 👨‍💻 Author

- **ADARSH S** — [@oyadarsh-hue](https://github.com/oyadarsh-hue)
