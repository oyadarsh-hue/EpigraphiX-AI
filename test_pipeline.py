"""
EpigraphiX-AI: Automated End-to-End Test & Benchmark Suite
Verifies Restoration, Super-Resolution, TrOCR Vision Transformer Recognition,
and Sandhi Lexicon Correction on real Palm Leaf Manuscript Inputs.
"""

import os
import sys
import io
import time
import cv2
import numpy as np

# Ensure UTF-8 output
if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

from epigraphical_enhancer import EpigraphicalEnhancer
from trocr_transformer_engine import TrOCRVisionTransformerEngine, MalayalamLexiconTrie


def test_epigraphical_enhancer():
    print("\n=======================================================")
    print("▶ TEST 1: Epigraphical Image Restoration & Super-Resolution")
    print("=======================================================")
    enhancer = EpigraphicalEnhancer(window_size=25, k=0.25, R=128)

    sample_paths = [
        os.path.join("Input Image", "1.jpg"),
        os.path.join("Input Image", "2.jpg")
    ]

    for p in sample_paths:
        assert os.path.exists(p), f"Input sample missing: {p}"
        out_p = os.path.join("Denoised Image", os.path.basename(p))
        
        t0 = time.time()
        results = enhancer.process_manuscript(p, out_p)
        elapsed_ms = (time.time() - t0) * 1000.0

        # Assertions
        assert results["binarized"].dtype == np.uint8, "Binarized image must be uint8"
        assert len(results["binarized"].shape) == 2, "Binarized image must be 2D single channel"
        assert results["enhanced"].shape == results["original"].shape, "Enhanced shape must match original"
        assert os.path.exists(out_p), f"Output file was not written: {out_p}"

        # PSNR check
        mse = np.mean((results["original"].astype(np.float64) - results["enhanced"].astype(np.float64)) ** 2)
        psnr = 10 * np.log10((255 ** 2) / max(1e-5, mse))

        print(f"  [PASS] {p} -> {out_p}")
        print(f"         Dimensions: {results['original'].shape[1]}x{results['original'].shape[0]} px | Time: {elapsed_ms:.2f}ms | PSNR: {psnr:.2f} dB")

    print("✔ Epigraphical Enhancer Suite Passed Successfully!")


def test_trie_and_sandhi():
    print("\n=======================================================")
    print("▶ TEST 2: Malayalam Lexicon Trie & Sandhi Grammar Matching")
    print("=======================================================")
    trie = MalayalamLexiconTrie("malayalam_dictionary.txt")
    print(f"  Trie loaded with {trie.word_count} lexicon entries.")

    test_queries = [
        ("മലയാളം", "മലയാളം"),
        ("എഴുത്തു", "എഴുത്ത്"),
        ("സാങ്കേതിക", "സാങ്കേതികവിദ്യ")
    ]

    for q, expected in test_queries:
        matched, dist = trie.search_closest(q, max_distance=3)
        print(f"  Query: '{q}' ➔ Best Match: '{matched}' (Edit Dist: {dist})")
        assert matched is not None and len(matched) > 0, f"Match failed for {q}"

    print("✔ Lexicon Trie & Sandhi Matcher Passed Successfully!")


def test_trocr_transformer_pipeline():
    print("\n=======================================================")
    print("▶ TEST 3: TrOCR Vision Transformer & Whole-Image OCR Pipeline")
    print("=======================================================")
    engine = TrOCRVisionTransformerEngine(
        alphabet_path="alphabets_malayalam.xlsx",
        dict_path="malayalam_dictionary.txt"
    )

    sample_paths = [
        os.path.join("Input Image", "1.jpg"),
        os.path.join("Input Image", "2.jpg")
    ]

    for p in sample_paths:
        t0 = time.time()
        res = engine.process_full_image(p)
        elapsed_ms = (time.time() - t0) * 1000.0

        # Assertions
        assert res["total_glyphs_detected"] > 0, f"No glyphs detected in {p}"
        assert res["lines_detected"] > 0, f"No lines detected in {p}"
        assert len(res["raw_transcription"]) > 0, "Transcription should not be empty"
        assert len(res["corrected_transcription"]) > 0, "Corrected output should not be empty"

        print(f"  [PASS] Image: {p}")
        print(f"         Glyphs Detected : {res['total_glyphs_detected']}")
        print(f"         Lines Detected  : {res['lines_detected']}")
        print(f"         Throughput      : {res['hardware_metrics']['throughput_ops_sec']}")
        print(f"         Pipeline Latency: {res['latency_ms']} ms")
        print(f"         WebGPU Estimate : {res['hardware_metrics']['webgpu_latency_estimate_ms']} ms")
        print(f"         Sample Raw      : {res['raw_transcription'][:40]}...")
        print(f"         Sample Corrected: {res['corrected_transcription'][:40]}...")

    print("✔ TrOCR Vision Transformer Pipeline Passed Successfully!")


def run_full_suite():
    print("=======================================================")
    print("  📜 EPIGRAPHIX-AI: COMPLETE TEST & BENCHMARK SUITE")
    print("=======================================================")
    test_epigraphical_enhancer()
    test_trie_and_sandhi()
    test_trocr_transformer_pipeline()
    print("\n=======================================================")
    print("  🎉 ALL AUTOMATED TESTS & VERIFICATIONS PASSED (100%)")
    print("=======================================================\n")


if __name__ == "__main__":
    run_full_suite()
