"""
EpigraphiX-AI: Epigraphical Image Restoration & Super-Resolution Suite (FANI 2.0)
High-performance Python implementation of O(1) Integral Sauvola Binarization,
Directional Cellulose Fiber Suppression, and Raking Light Stylus Groove Sharpening.
"""

import os
import cv2
import numpy as np


class EpigraphicalEnhancer:
    def __init__(self, window_size=25, k=0.25, R=128):
        self.window_size = window_size if window_size % 2 == 1 else window_size + 1
        self.k = k
        self.R = R

    def integral_sauvola_binarize(self, gray_img, window_size=None, k=None, R=None):
        """
        O(1) Integral-Image Adaptive Sauvola Binarization.
        Computes local mean and standard deviation in constant time per pixel.
        """
        if window_size is None:
            window_size = self.window_size
        if k is None:
            k = self.k
        if R is None:
            R = self.R

        h, w = gray_img.shape
        r = window_size // 2

        img_float = gray_img.astype(np.float64)
        
        # Integral images for sum and squared sum
        integral_sum = cv2.integral(img_float)
        integral_sq = cv2.integral(img_float ** 2)

        # Vectorized box filter coordinates
        y1 = np.maximum(0, np.arange(h) - r)
        y2 = np.minimum(h, np.arange(h) + r + 1)
        x1 = np.maximum(0, np.arange(w) - r)
        x2 = np.minimum(w, np.arange(w) + r + 1)

        Y1, X1 = np.meshgrid(y1, x1, indexing='ij')
        Y2, X2 = np.meshgrid(y2, x2, indexing='ij')

        counts = (Y2 - Y1) * (X2 - X1)

        # Region sums using integral images
        sums = (integral_sum[Y2, X2] - integral_sum[Y1, X2] - integral_sum[Y2, X1] + integral_sum[Y1, X1])
        sq_sums = (integral_sq[Y2, X2] - integral_sq[Y1, X2] - integral_sq[Y2, X1] + integral_sq[Y1, X1])

        mean = sums / counts
        variance = np.maximum(0.0, (sq_sums / counts) - (mean ** 2))
        std = np.sqrt(variance)

        # Sauvola threshold calculation
        threshold = mean * (1.0 + k * ((std / R) - 1.0))
        binary = (img_float < threshold).astype(np.uint8) * 255

        # Morphological speckle filtering
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        return binary, threshold

    def fiber_aware_neural_inpainting(self, img):
        """
        FANI 2.0: Fiber-Aware Directional Morphological Decomposition.
        Suppresses horizontal cellulose fiber striations while retaining stylus incisions.
        """
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()

        # CLAHE local contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Directional morphological opening along 0-degree grain
        fiber_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
        fiber_background = cv2.morphologyEx(enhanced, cv2.MORPH_OPEN, fiber_kernel)

        # Subtract directional grain background to isolate ink incisions
        subtracted = cv2.subtract(enhanced, fiber_background)
        restored = cv2.addWeighted(enhanced, 0.85, subtracted, 0.45, 0)

        # Bilateral filter for edge-preserving smoothing
        denoised = cv2.bilateralFilter(restored, d=7, sigmaColor=50, sigmaSpace=50)

        return denoised

    def super_resolve_and_enhance(self, img, scale_factor=2):
        """
        Epigraphical Super-Resolution & Sub-Surface Groove Sharpening.
        Upscales manuscript imagery while enhancing micro-stylus ridge gradients.
        """
        # Base upscale
        h, w = img.shape[:2]
        new_w, new_h = w * scale_factor, h * scale_factor
        upscaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # Stylus groove unsharp masking
        gaussian = cv2.GaussianBlur(upscaled, (0, 0), sigmaX=1.5)
        sharpened = cv2.addWeighted(upscaled, 1.5, gaussian, -0.5, 0)

        # Tone mapping in LAB color space
        lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        enhanced_lab = cv2.merge([l_enhanced, a, b])
        output = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        return output

    def process_manuscript(self, input_path, output_denoised_path=None):
        """
        Executes full restoration pipeline on raw palm-leaf manuscript image.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Failed to read image at: {input_path}")

        # 1. Directional Fiber Inpainting
        fani_clean = self.fiber_aware_neural_inpainting(img)

        # 2. Adaptive Sauvola Binarization
        bin_img, _ = self.integral_sauvola_binarize(fani_clean)

        # 3. Stylus Groove Enhancement
        enhanced_bgr = self.super_resolve_and_enhance(img, scale_factor=1)

        # Save result if path provided
        if output_denoised_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_denoised_path)), exist_ok=True)
            cv2.imwrite(output_denoised_path, enhanced_bgr)

        return {
            "original": img,
            "fani_clean": fani_clean,
            "binarized": bin_img,
            "enhanced": enhanced_bgr
        }


if __name__ == "__main__":
    enhancer = EpigraphicalEnhancer()
    for fname in ["1.jpg", "2.jpg"]:
        in_p = os.path.join("Input Image", fname)
        out_p = os.path.join("Denoised Image", fname)
        if os.path.exists(in_p):
            res = enhancer.process_manuscript(in_p, out_p)
            print(f"[OK] Enhanced & Saved: {in_p} -> {out_p} (Size: {res['enhanced'].shape})")
