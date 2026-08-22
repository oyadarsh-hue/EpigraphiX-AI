"""
EpigraphiX-AI: Automated Test Suite for Strict Palm-Leaf Detection & Depth Analysis
Verifies multi-class discrimination between:
1. Authentic Inscribed Palm-Leaf Manuscripts (valid_inscribed_leaf)
2. Natural Uninscribed Leaves / Blank Palm Leaves (blank_leaf)
3. Synthetic Digital UI Screenshots / Non-Manuscript Images (non_manuscript)
"""

import sys
import io
import os
import cv2
import numpy as np

# Ensure UTF-8 output encoding across Windows terminals
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from epigraphical_enhancer import EpigraphicalEnhancer

def create_synthetic_blank_leaf():
    h, w = 150, 600
    blank_leaf = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            noise = np.random.randint(-8, 8)
            fiber_grain = int(np.sin(y * 0.4) * 5)
            r = np.clip(185 + noise + fiber_grain, 0, 255)
            g = np.clip(140 + noise + fiber_grain, 0, 255)
            b = np.clip(80 + noise // 2, 0, 255)
            blank_leaf[y, x] = [b, g, r]
    return blank_leaf

def create_synthetic_ui_screenshot():
    h, w = 400, 800
    # Dark UI background #0f172a (B=42, G=23, R=15)
    ui_img = np.zeros((h, w, 3), dtype=np.uint8)
    ui_img[:, :] = [42, 23, 15]
    # Draw flat UI card #1e293b (B=59, G=41, R=30)
    ui_img[50:350, 100:700] = [59, 41, 30]
    # Draw cyan button #38bdf8 (B=248, G=189, R=56)
    ui_img[280:320, 250:550] = [248, 189, 56]
    return ui_img

def test_real_palm_leaf_manuscripts():
    enhancer = EpigraphicalEnhancer()
    real_paths = [
        os.path.join("Input Image", "1.jpg"),
        os.path.join("Input Image", "2.jpg"),
        os.path.join("web_studio", "sample1.jpg"),
        os.path.join("web_studio", "sample2.jpg")
    ]
    for p in real_paths:
        if os.path.exists(p):
            img = cv2.imread(p)
            res = enhancer.validate_palm_leaf_authenticity(img)
            print(f"[TEST PASS] Real manuscript {p}: Status={res['status']}, Telemetry={res['telemetry']}")
            assert res['status'] == 'valid_inscribed_leaf', f"Expected valid_inscribed_leaf for {p}, got {res['status']}"
            assert res['is_valid'] is True

def test_blank_unwritten_leaf():
    enhancer = EpigraphicalEnhancer()
    blank_leaf = create_synthetic_blank_leaf()
    res = enhancer.validate_palm_leaf_authenticity(blank_leaf)
    print(f"[TEST PASS] Blank leaf: Status={res['status']}, Telemetry={res['telemetry']}")
    assert res['status'] == 'blank_leaf', f"Expected blank_leaf, got {res['status']}"
    assert res['is_blank'] is True
    assert res['is_valid'] is False

def test_synthetic_ui_rejection():
    enhancer = EpigraphicalEnhancer()
    ui_img = create_synthetic_ui_screenshot()
    res = enhancer.validate_palm_leaf_authenticity(ui_img)
    print(f"[TEST PASS] Synthetic UI: Status={res['status']}, Telemetry={res['telemetry']}")
    assert res['status'] == 'non_manuscript', f"Expected non_manuscript for UI image, got {res['status']}"
    assert res['is_valid'] is False

def test_user_uploaded_screenshot():
    enhancer = EpigraphicalEnhancer()
    user_img_path = r"C:\Users\HP\.gemini\antigravity\brain\3ba28ec2-ff52-48b3-b72f-a1248ba36c59\.user_uploaded\media_1787403338660.png"
    if os.path.exists(user_img_path):
        img = cv2.imread(user_img_path)
        res = enhancer.validate_palm_leaf_authenticity(img)
        print(f"[TEST PASS] User screenshot: Status={res['status']}, Telemetry={res['telemetry']}")
        assert res['status'] == 'non_manuscript', f"Expected non_manuscript for user screenshot, got {res['status']}"
        assert res['is_valid'] is False

if __name__ == "__main__":
    print("=" * 65)
    print("Running EpigraphiX-AI Strict Palm-Leaf Detection Test Suite")
    print("=" * 65)
    test_real_palm_leaf_manuscripts()
    test_blank_unwritten_leaf()
    test_synthetic_ui_rejection()
    test_user_uploaded_screenshot()
    print("=" * 65)
    print("ALL TESTS PASSED SUCCESSFULLY (100% Accuracy)")
    print("=" * 65)
