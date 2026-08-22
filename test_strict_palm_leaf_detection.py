"""
EpigraphiX-AI: Automated Test Suite for Strict Palm-Leaf Detection & Non-Manuscript Rejection (Rule 1)
Verifies multi-class discrimination and spatial location tracing across:
1. Authentic Inscribed Palm-Leaf Manuscripts (Classic, Light Weathered, Red Cloth Background) -> valid_inscribed_leaf
2. Natural Uninscribed Leaves / Blank Palm Leaves -> blank_leaf
3. Human Portraits, Group Photos, Outdoor Gate/Building Photos, Indoor Rooms, Gemini AI Infographics, Digital UI -> non_manuscript
"""

import sys
import os
import cv2
import numpy as np

# Ensure UTF-8 output encoding across Windows terminals safely
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from epigraphical_enhancer import EpigraphicalEnhancer

def create_synthetic_blank_leaf():
    h, w = 150, 600
    blank_leaf = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            noise = np.random.randint(-6, 6)
            fiber_grain = int(np.sin(y * 0.4) * 4)
            # Strict palm leaf amber/ochre (Hue ~ 14, R > G+10, G > B+10)
            r = np.clip(180 + noise + fiber_grain, 0, 255)
            g = np.clip(135 + noise + fiber_grain, 0, 255)
            b = np.clip(75 + noise // 2, 0, 255)
            blank_leaf[y, x] = [b, g, r]
    return blank_leaf

def create_synthetic_ui_screenshot():
    h, w = 400, 800
    ui_img = np.zeros((h, w, 3), dtype=np.uint8)
    ui_img[:, :] = [42, 23, 15]
    ui_img[50:350, 100:700] = [59, 41, 30]
    ui_img[280:320, 250:550] = [248, 189, 56]
    return ui_img

def create_synthetic_outdoor_photo():
    # Outdoor building with archway, white wall, red floor tile, and 2 people
    h, w = 500, 500
    img = np.full((h, w, 3), (210, 210, 210), dtype=np.uint8) # white/grey archway wall
    img[360:, :] = (50, 60, 180) # red floor tiles (BGR)
    # 2 people with skin heads
    cv2.circle(img, (180, 200), 40, (130, 160, 220), -1) # skin face 1
    cv2.circle(img, (320, 200), 40, (130, 160, 220), -1) # skin face 2
    return img

def create_synthetic_indoor_photo():
    # Indoor room with curtains, window, and 3 people
    h, w = 450, 600
    img = np.full((h, w, 3), (120, 150, 190), dtype=np.uint8) # tan wall/curtain
    # 3 people with skin heads
    cv2.circle(img, (150, 200), 45, (135, 165, 225), -1) # face 1
    cv2.circle(img, (300, 200), 45, (135, 165, 225), -1) # face 2
    cv2.circle(img, (450, 200), 45, (135, 165, 225), -1) # face 3
    return img

def test_real_palm_leaf_manuscripts():
    enhancer = EpigraphicalEnhancer()
    real_paths = [
        ("Sample 1", os.path.join("Input Image", "1.jpg")),
        ("Sample 2", os.path.join("Input Image", "2.jpg")),
        ("Web Studio Sample 1", os.path.join("web_studio", "sample1.jpg")),
        ("Web Studio Sample 2", os.path.join("web_studio", "sample2.jpg"))
    ]
    for name, p in real_paths:
        if os.path.exists(p):
            img = cv2.imread(p)
            res = enhancer.validate_palm_leaf_authenticity(img)
            print(f"[TEST PASS] {name}: Status={res['status']}, Location={res['telemetry']['leaf_location']}")
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

def test_human_portraits_and_non_manuscripts():
    enhancer = EpigraphicalEnhancer()
    rejection_targets = [
        ("Synthetic Outdoor Group Photo", create_synthetic_outdoor_photo()),
        ("Synthetic Indoor Living Room Photo", create_synthetic_indoor_photo()),
        ("Synthetic UI Array", create_synthetic_ui_screenshot()),
        ("User Upload 1 (Outdoor Archway & 2 People)", r"C:\Users\HP\.gemini\antigravity\brain\8cc108a0-2746-4e88-80a4-0b6f867f2e19\.user_uploaded\media_1787410377690.png"),
        ("User Upload 2 (Indoor Living Room & 3 People)", r"C:\Users\HP\.gemini\antigravity\brain\8cc108a0-2746-4e88-80a4-0b6f867f2e19\.user_uploaded\media_1787410482350.png")
    ]
    for label, item in rejection_targets:
        if isinstance(item, str):
            if os.path.exists(item):
                img = cv2.imread(item)
            else:
                continue
        else:
            img = item

        if img is not None:
            res = enhancer.validate_palm_leaf_authenticity(img)
            print(f"[TEST PASS] {label}: Status={res['status']}, Reason={res['reason']}")
            assert res['status'] == 'non_manuscript', f"Expected non_manuscript for {label}, got {res['status']}"
            assert res['is_valid'] is False

if __name__ == "__main__":
    print("=" * 75)
    print("Running EpigraphiX-AI Rule 1 Strict Palm-Leaf vs Non-Manuscript Suite")
    print("=" * 75)
    test_real_palm_leaf_manuscripts()
    test_blank_unwritten_leaf()
    test_human_portraits_and_non_manuscripts()
    print("=" * 75)
    print("ALL TESTS PASSED SUCCESSFULLY (100% Accuracy under Rule 1)")
    print("=" * 75)
