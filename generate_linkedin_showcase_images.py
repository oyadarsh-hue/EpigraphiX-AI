"""
Generates 3 Ultra-High-Resolution Single-Frame Index/Dashboard Showcase PNGs in C:\\Users\\HP\\Downloads\\
1. EpigraphiX_AI_Index_Showcase.png
2. AssentTag_Index_Showcase.png
3. Deciphera_Index_Showcase.png
"""

import os
import sys
import io
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

downloads_dir = r"C:\Users\HP\Downloads"

# -------------------------------------------------------------
# 1. HTML Showcase for EpigraphiX-AI (Unified 1920x1080 Frame)
# -------------------------------------------------------------
epigraphix_showcase_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EpigraphiX-AI - Palm-Leaf Epigraphical OCR Studio</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
  body { background: radial-gradient(circle at 50% 10%, #0d1527, #030712); color: #f8fafc; padding: 16px; width: 1920px; height: 1080px; overflow: hidden; }
  
  .header { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(14px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 12px 24px; margin-bottom: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.6); }
  .logo-group { display: flex; align-items: center; gap: 14px; }
  .logo-icon { width: 38px; height: 38px; background: linear-gradient(135deg, #0284c7, #38bdf8); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
  .title-h1 { font-size: 20px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
  .subtitle { font-size: 11.5px; color: #94a3b8; margin-top: 1px; }
  .badges { display: flex; gap: 8px; }
  .badge { font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 20px; display: flex; align-items: center; gap: 6px; }
  .badge-active { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
  .badge-engine { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  
  .grid-container { display: grid; grid-template-columns: 1.15fr 1fr; gap: 12px; height: calc(1080px - 95px); }
  .panel { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
  .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(148, 163, 184, 0.1); padding-bottom: 8px; }
  .panel-title { font-size: 14px; font-weight: 700; color: #e2e8f0; display: flex; align-items: center; gap: 8px; }
  
  /* Left Panel: Image Inspector & Bounding Boxes */
  .manuscript-viewport { position: relative; width: 100%; height: 260px; background: #070b14; border-radius: 8px; overflow: hidden; border: 1px solid rgba(56, 189, 248, 0.2); display: flex; align-items: center; justify-content: center; }
  .manuscript-canvas { width: 100%; height: 100%; }
  
  .metrics-pill-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
  .metric-pill { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 8px; padding: 8px; text-align: center; }
  .mp-val { font-size: 16px; font-weight: 800; color: #38bdf8; }
  .mp-lbl { font-size: 9.5px; color: #94a3b8; text-transform: uppercase; margin-top: 2px; }

  /* 5-Model 2D Decision Manifold Graph */
  .manifold-box { background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.18); border-radius: 10px; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
  .manifold-grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 12px; align-items: center; }
  .graph-canvas { height: 210px; width: 100%; background: #030712; border-radius: 6px; border: 1px solid rgba(148, 163, 184, 0.15); }
  .bench-table { width: 100%; border-collapse: collapse; font-size: 10.5px; }
  .bench-table th { text-align: left; padding: 5px; color: #94a3b8; border-bottom: 1px solid rgba(148, 163, 184, 0.15); font-size: 9.5px; text-transform: uppercase; }
  .bench-table td { padding: 5px; border-bottom: 1px solid rgba(148, 163, 184, 0.08); color: #cbd5e1; }
  
  /* Right Panel: Extraction & Multilingual Translation */
  .extract-banner { display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 12px 18px; }
  .ext-box h5 { font-size: 10px; color: #94a3b8; text-transform: uppercase; }
  .ext-box .word { font-size: 22px; font-weight: 800; color: #34d399; margin-top: 2px; }
  .ext-arrow { font-size: 20px; color: #38bdf8; font-weight: bold; }
  
  .bridge-card { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
  .bridge-grid { display: grid; grid-template-columns: 1fr 1.3fr 1fr; gap: 8px; }
  .bg-item { background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 6px; }
  .bg-lbl { font-size: 9.5px; color: #38bdf8; font-weight: 600; text-transform: uppercase; }
  .bg-val { font-size: 13px; font-weight: 700; color: #f8fafc; margin-top: 3px; line-height: 1.3; }

  /* Benchmark Gauges */
  .gauges-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  .gauge-card { background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 8px; padding: 10px; text-align: center; }
  .gauge-circle { width: 44px; height: 44px; border-radius: 50%; border: 3px solid #38bdf8; display: flex; align-items: center; justify-content: center; margin: 0 auto 4px; font-size: 12px; font-weight: 800; color: #ffffff; }
  .gauge-lbl { font-size: 9px; color: #94a3b8; text-transform: uppercase; }
</style>
</head>
<body>

<div class="header">
  <div class="logo-group">
    <div class="logo-icon">📜</div>
    <div>
      <div class="title-h1">Palm-Leaf Epigraphical OCR Studio (EpigraphiX-AI)</div>
      <div class="subtitle">SOTA Vision Transformer (TrOCR) • O(1) Sauvola Binarization • 5-Model Decision Manifold • Multilingual Epigraphical Bridge</div>
    </div>
  </div>
  <div class="badges">
    <div class="badge badge-active">● Rule 1 Authenticator: Verified Inscribed Leaf</div>
    <div class="badge badge-engine">⚡ WebGPU Engine Active (46.8ms)</div>
  </div>
</div>

<div class="grid-container">
  <!-- Left Panel -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">🖼️ Image Inspector & Multi-Layer Glyph Segmentation</div>
      <span style="font-size: 10.5px; color: #34d399; font-weight: 600;">62 Character Glyphs • 5 Baselines Detected</span>
    </div>

    <!-- Manuscript Strip View with Bounding Boxes -->
    <div class="manuscript-viewport">
      <svg width="100%" height="100%" viewBox="0 0 800 240">
        <!-- Palm leaf substrate background -->
        <rect x="0" y="0" width="800" height="240" fill="#2d1b08"/>
        <!-- Texture striations -->
        <line x1="0" y1="40" x2="800" y2="40" stroke="#452a0e" stroke-width="1"/>
        <line x1="0" y1="80" x2="800" y2="80" stroke="#452a0e" stroke-width="1"/>
        <line x1="0" y1="120" x2="800" y2="120" stroke="#452a0e" stroke-width="1"/>
        <line x1="0" y1="160" x2="800" y2="160" stroke="#452a0e" stroke-width="1"/>
        <line x1="0" y1="200" x2="800" y2="200" stroke="#452a0e" stroke-width="1"/>
        
        <!-- Engraved Ancient Glyphs -->
        <g fill="none" stroke="#eab308" stroke-width="2.5" stroke-linecap="round" opacity="0.95">
          <!-- Row 1: Malayalam Glyphs -->
          <path d="M40,55 Q60,35 80,55 Q100,75 120,55"/>
          <circle cx="155" cy="55" r="14"/>
          <path d="M190,45 Q210,65 230,45 T260,65"/>
          <path d="M290,40 L310,70 M310,40 L290,70"/>
          <path d="M340,45 Q360,65 380,45"/>
          <circle cx="420" cy="55" r="12"/>
          <path d="M455,45 Q480,70 505,45"/>
          <path d="M535,40 L565,70"/>
          <circle cx="600" cy="55" r="14"/>
          <path d="M635,45 Q660,65 685,45"/>
          <path d="M715,40 Q735,70 755,45"/>

          <!-- Row 2 -->
          <path d="M45,130 Q70,105 95,130 T135,130"/>
          <circle cx="170" cy="130" r="13"/>
          <path d="M205,120 Q230,145 255,120"/>
          <path d="M290,115 L320,145 M320,115 L290,145"/>
          <circle cx="360" cy="130" r="12"/>
          <path d="M395,120 Q420,145 445,120"/>
          <circle cx="485" cy="130" r="14"/>
          <path d="M520,120 Q545,145 570,120"/>
          <path d="M605,115 L635,145"/>
          <circle cx="675" cy="130" r="13"/>
          <path d="M710,120 Q735,145 760,120"/>

          <!-- Row 3 -->
          <path d="M50,195 Q75,175 100,195"/>
          <circle cx="140" cy="195" r="14"/>
          <path d="M180,185 Q205,210 230,185"/>
          <circle cx="270" cy="195" r="12"/>
          <path d="M310,185 Q335,210 360,185"/>
          <path d="M400,180 L430,210"/>
          <circle cx="470" cy="195" r="13"/>
          <path d="M510,185 Q535,210 560,185"/>
          <circle cx="600" cy="195" r="12"/>
          <path d="M640,185 Q665,210 690,185"/>
        </g>

        <!-- Segmented Bounding Boxes -->
        <rect x="30" y="30" width="105" height="48" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
        <rect x="140" y="30" width="130" height="48" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
        <rect x="275" y="30" width="115" height="48" fill="none" stroke="#10b981" stroke-width="2"/>
        <text x="278" y="24" fill="#10b981" font-size="10" font-weight="bold">കരുണ (98.2%)</text>
        <rect x="395" y="30" width="120" height="48" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
        <rect x="520" y="30" width="170" height="48" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
      </svg>
    </div>

    <!-- Metrics Row -->
    <div class="metrics-pill-row">
      <div class="metric-pill">
        <div class="mp-val">0</div>
        <div class="mp-lbl">Levenshtein Dist</div>
      </div>
      <div class="metric-pill">
        <div class="mp-val">98.2%</div>
        <div class="mp-lbl">Match Confidence</div>
      </div>
      <div class="metric-pill">
        <div class="mp-val">0</div>
        <div class="mp-lbl">Substitutions</div>
      </div>
      <div class="metric-pill">
        <div class="mp-val">0</div>
        <div class="mp-lbl">Insertions</div>
      </div>
      <div class="metric-pill">
        <div class="mp-val">0</div>
        <div class="mp-lbl">Deletions</div>
      </div>
    </div>

    <!-- 5-Model 2D Decision Manifold -->
    <div class="manifold-box">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:12px; font-weight:700; color:#e2e8f0;">⚡ 5-Model SOTA Decision Manifold & Betti Invariants (β₀, β₁)</span>
        <span style="font-size:10px; color:#38bdf8; font-weight:600;">Active: Support Vector Machine (RBF)</span>
      </div>

      <div class="manifold-grid">
        <div class="graph-canvas">
          <svg width="100%" height="100%" viewBox="0 0 320 200">
            <!-- Grid Lines -->
            <line x1="30" y1="20" x2="30" y2="180" stroke="#1e293b" stroke-width="1"/>
            <line x1="30" y1="180" x2="300" y2="180" stroke="#1e293b" stroke-width="1"/>
            <line x1="30" y1="100" x2="300" y2="100" stroke="#334155" stroke-dasharray="2,2"/>
            <line x1="165" y1="20" x2="165" y2="180" stroke="#334155" stroke-dasharray="2,2"/>
            
            <!-- Non-Linear Decision Hyperplane (SVM RBF) -->
            <path d="M30,140 Q120,40 180,95 T300,60" fill="none" stroke="#38bdf8" stroke-width="2.5"/>
            
            <!-- Class 1 Data Points (Blue Circles) -->
            <circle cx="70" cy="155" r="4" fill="#38bdf8"/><circle cx="95" cy="165" r="4" fill="#38bdf8"/>
            <circle cx="120" cy="140" r="4" fill="#38bdf8"/><circle cx="150" cy="160" r="4" fill="#38bdf8"/>
            <circle cx="210" cy="145" r="4" fill="#38bdf8"/><circle cx="250" cy="120" r="4" fill="#38bdf8"/>

            <!-- Class 2 Data Points (Amber Squares) -->
            <rect x="75" y="45" width="7" height="7" fill="#f59e0b"/><rect x="110" y="30" width="7" height="7" fill="#f59e0b"/>
            <rect x="150" y="55" width="7" height="7" fill="#f59e0b"/><rect x="210" y="40" width="7" height="7" fill="#f59e0b"/>
            <rect x="260" y="35" width="7" height="7" fill="#f59e0b"/><rect x="280" y="50" width="7" height="7" fill="#f59e0b"/>
          </svg>
        </div>

        <table class="bench-table">
          <thead>
            <tr><th>Model</th><th>Accuracy</th><th>Latency</th></tr>
          </thead>
          <tbody>
            <tr style="background:rgba(56,189,248,0.15); font-weight:bold; color:#38bdf8;"><td>SVM (Hyperplane)</td><td>98.8%</td><td>1.2 ms</td></tr>
            <tr><td>Random Forest (100)</td><td>97.5%</td><td>2.4 ms</td></tr>
            <tr><td>k-NN (Mahalanobis)</td><td>96.2%</td><td>1.8 ms</td></tr>
            <tr><td>Gaussian Naive Bayes</td><td>93.4%</td><td>0.8 ms</td></tr>
            <tr><td>CNN Neural Lattice</td><td>99.1%</td><td>4.6 ms</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Right Panel -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">📖 Dynamic Word Extraction & Multilingual Epigraphical Exegesis</div>
      <span style="font-size: 10.5px; color: #38bdf8;">Trie Lexicon: 340 Entries</span>
    </div>

    <!-- Recognized Term Banner -->
    <div class="extract-banner">
      <div class="ext-box">
        <h5>Raw Inscription Sequence</h5>
        <div class="word" style="color:#eab308; font-size:18px;">ക-രു-ണ (Mode 0: Pristine)</div>
      </div>
      <div class="ext-arrow">➔</div>
      <div class="ext-box">
        <h5>Meaningful Word Match</h5>
        <div class="word">കരുണ (Karuṇa)</div>
      </div>
    </div>

    <!-- Multilingual Semantic Bridge -->
    <div class="bridge-card">
      <div style="font-size:12px; font-weight:700; color:#e2e8f0;">🌐 Multilingual Epigraphical Semantic Bridge</div>
      <div class="bridge-grid">
        <div class="bg-item">
          <div class="bg-lbl">Old vs New Literature</div>
          <div class="bg-val" style="color:#38bdf8;">കാരുണ്യഭാവം ➔ കരുണ</div>
          <div style="font-size:10px; color:#94a3b8; margin-top:2px;">Genre: Spiritual Ethics</div>
        </div>
        <div class="bg-item">
          <div class="bg-lbl">English Meaning & Exegesis</div>
          <div class="bg-val" style="font-size:11.5px; color:#34d399;">Profound compassionate grace and empathetic benevolence for all beings.</div>
        </div>
        <div class="bg-item">
          <div class="bg-lbl">Hindi Meaning (Devanagari)</div>
          <div class="bg-val" style="color:#f59e0b;">करुणा (सहानुभूति एवं दयाभाव)</div>
        </div>
      </div>
    </div>

    <!-- Palaeographic Chronometry & Vedic Accent -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
      <div class="bg-item" style="border:1px solid rgba(56,189,248,0.2);">
        <div class="bg-lbl">⏳ Palaeographic Age (PCC-CSAE)</div>
        <div class="bg-val" style="color:#38bdf8;">10th – 12th Century CE (Chera Era)</div>
        <div style="font-size:10px; color:#94a3b8;">Ductus: Middle Vatteluttu</div>
      </div>
      <div class="bg-item" style="border:1px solid rgba(56,189,248,0.2);">
        <div class="bg-lbl">🎵 Vedic Meter / Accent (Web Audio)</div>
        <div class="bg-val" style="color:#a855f7;">Anustubh Meter (136.1 Hz Ohm)</div>
        <div style="font-size:10px; color:#94a3b8;">Audio Synthesis Active</div>
      </div>
    </div>

    <!-- Accuracy & Performance Scorecard -->
    <div class="panel-header" style="margin-top:4px;">
      <div class="panel-title">📊 System Benchmark & Verification Scorecard</div>
    </div>

    <div class="gauges-row">
      <div class="gauge-card">
        <div class="gauge-circle" style="border-color:#10b981;">98.8%</div>
        <div class="gauge-lbl">Word Accuracy (WAR)</div>
      </div>
      <div class="gauge-card">
        <div class="gauge-circle" style="border-color:#38bdf8;">99.2%</div>
        <div class="gauge-lbl">Character Accuracy</div>
      </div>
      <div class="gauge-card">
        <div class="gauge-circle" style="border-color:#a855f7;">0.8%</div>
        <div class="gauge-lbl">Character Error (CER)</div>
      </div>
      <div class="gauge-card">
        <div class="gauge-circle" style="border-color:#f59e0b;">1.2%</div>
        <div class="gauge-lbl">Word Error (WER)</div>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

# -------------------------------------------------------------
# 2. HTML Showcase for AssentTag (1920x1080 Frame)
# -------------------------------------------------------------
assenttag_showcase_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AssentTag - Biometric Privacy & Dynamic Consent Studio</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
  body { background: radial-gradient(circle at 50% 10%, #0f172a, #020617); color: #f8fafc; padding: 16px; width: 1920px; height: 1080px; overflow: hidden; }
  
  .header { display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(14px); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 12px; padding: 12px 24px; margin-bottom: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
  .logo-group { display: flex; align-items: center; gap: 14px; }
  .logo-icon { width: 38px; height: 38px; background: linear-gradient(135deg, #0284c7, #0d9488); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
  .title-h1 { font-size: 20px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
  .subtitle { font-size: 11.5px; color: #94a3b8; margin-top: 1px; }
  .badges { display: flex; gap: 8px; }
  .badge { font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 20px; display: flex; align-items: center; gap: 6px; }
  .badge-active { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
  .badge-gdpr { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
  
  .grid-container { display: grid; grid-template-columns: 1.15fr 1fr; gap: 12px; height: calc(1080px - 95px); }
  .panel { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
  .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(148, 163, 184, 0.1); padding-bottom: 8px; }
  .panel-title { font-size: 14px; font-weight: 700; color: #e2e8f0; display: flex; align-items: center; gap: 8px; }
  
  /* Left Panel: Camera Stream & Landmarking */
  .feed-container { position: relative; width: 100%; height: 490px; background: #000000; border-radius: 8px; overflow: hidden; border: 1px solid rgba(148, 163, 184, 0.2); display: flex; align-items: center; justify-content: center; }
  
  .controls-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  .metric-card { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 8px; padding: 10px; text-align: center; }
  .metric-val { font-size: 16px; font-weight: 800; color: #38bdf8; }
  .metric-lbl { font-size: 9.5px; color: #94a3b8; margin-top: 2px; text-transform: uppercase; }

  /* Right Panel: Biometric Embedding & Consent Engine */
  .card-box { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
  .card-title { font-size: 12px; font-weight: 700; color: #cbd5e1; }
  
  .embedding-bar-container { display: flex; gap: 2px; height: 38px; align-items: flex-end; background: rgba(15, 23, 42, 0.6); padding: 4px; border-radius: 6px; }
  .emb-bar { flex: 1; background: linear-gradient(to top, #0284c7, #38bdf8); border-radius: 1px; }
  
  .veil-status-box { background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 8px; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between; }
  .veil-text h4 { font-size: 12.5px; color: #60a5fa; }
  .veil-text p { font-size: 10.5px; color: #94a3b8; }
  .btn-veil { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 700; font-size: 11px; cursor: pointer; }

  .audit-table { width: 100%; border-collapse: collapse; font-size: 10.5px; }
  .audit-table th { text-align: left; padding: 6px 8px; color: #94a3b8; border-bottom: 1px solid rgba(148, 163, 184, 0.15); font-size: 9.5px; text-transform: uppercase; }
  .audit-table td { padding: 6px 8px; border-bottom: 1px solid rgba(148, 163, 184, 0.08); color: #cbd5e1; }
</style>
</head>
<body>

<div class="header">
  <div class="logo-group">
    <div class="logo-icon">🛡️</div>
    <div>
      <div class="title-h1">AssentTag — Biometric Privacy & Dynamic Consent Platform</div>
      <div class="subtitle">Real-Time Facial Detection • ResNet-34 128D Embeddings • Automated Selective Blurring • GDPR Article 6 Compliant</div>
    </div>
  </div>
  <div class="badges">
    <div class="badge badge-gdpr">🔒 GDPR Privacy-by-Default</div>
    <div class="badge badge-active">● Biometric Engine Active</div>
  </div>
</div>

<div class="grid-container">
  <!-- Left Panel -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">📷 Real-Time Video Ingestion & Selective "The Veil" Blurring</div>
      <span style="font-size: 10.5px; color: #34d399; font-weight: 600;">Dlib 68-Point Landmarking Active</span>
    </div>
    
    <div class="feed-container">
      <svg width="100%" height="100%" viewBox="0 0 800 480" style="background:#0a0f1d;">
        <rect x="0" y="0" width="800" height="480" fill="#0b1329"/>
        <circle cx="280" cy="220" r="140" fill="#1e293b" opacity="0.4"/>
        <circle cx="560" cy="240" r="130" fill="#1e293b" opacity="0.4"/>
        
        <!-- Person 1: Consented User (Adarsh S) -->
        <circle cx="280" cy="180" r="65" fill="#334155"/>
        <rect x="200" y="100" width="160" height="200" rx="10" fill="none" stroke="#10b981" stroke-width="2.5" stroke-dasharray="6,3"/>
        <rect x="195" y="75" width="170" height="22" rx="4" fill="#10b981"/>
        <text x="202" y="90" fill="#022c22" font-size="11" font-weight="bold">✓ CONSENTED (Adarsh S - ID: 894)</text>
        <circle cx="260" cy="170" r="3" fill="#34d399"/><circle cx="300" cy="170" r="3" fill="#34d399"/>
        <path d="M265,200 Q280,215 295,200" fill="none" stroke="#34d399" stroke-width="2"/>
        
        <!-- Person 2: Unconsented Bystander (Auto-Blurred) -->
        <g filter="blur(16px)">
          <circle cx="560" cy="190" r="60" fill="#475569"/>
        </g>
        <rect x="485" y="115" width="150" height="190" rx="10" fill="rgba(239, 68, 68, 0.12)" stroke="#ef4444" stroke-width="2.5"/>
        <rect x="480" y="90" width="160" height="22" rx="4" fill="#ef4444"/>
        <text x="488" y="105" fill="#ffffff" font-size="11" font-weight="bold">🔒 UNCONSENTED (Bystander #2)</text>
        <text x="500" y="215" fill="#fca5a5" font-size="13" font-weight="bold">THE VEIL ACTIVE</text>
      </svg>
    </div>
    
    <div class="controls-row">
      <div class="metric-card">
        <div class="metric-val">128D</div>
        <div class="metric-lbl">ResNet Vector</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">&lt; 8.4 ms</div>
        <div class="metric-lbl">Cache Latency</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">d = 0.38</div>
        <div class="metric-lbl">Euclidean (Thresh: 0.60)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">100.0%</div>
        <div class="metric-lbl">GDPR Art. 6</div>
      </div>
    </div>
  </div>

  <!-- Right Panel -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">🧠 Deep Metric Learning & Consent Orchestration Engine</div>
      <span style="font-size: 10.5px; color: #38bdf8;">Django & MySQL 3NF Backend</span>
    </div>

    <!-- 128D Embedding Visualizer -->
    <div class="card-box">
      <div class="card-title">ResNet-34 128-Dimensional Biometric Embedding Manifold</div>
      <div class="embedding-bar-container">
        <div class="emb-bar" style="height:80%;"></div><div class="emb-bar" style="height:45%;"></div>
        <div class="emb-bar" style="height:90%;"></div><div class="emb-bar" style="height:60%;"></div>
        <div class="emb-bar" style="height:30%;"></div><div class="emb-bar" style="height:75%;"></div>
        <div class="emb-bar" style="height:100%;"></div><div class="emb-bar" style="height:55%;"></div>
        <div class="emb-bar" style="height:85%;"></div><div class="emb-bar" style="height:40%;"></div>
        <div class="emb-bar" style="height:70%;"></div><div class="emb-bar" style="height:95%;"></div>
        <div class="emb-bar" style="height:50%;"></div><div class="emb-bar" style="height:65%;"></div>
        <div class="emb-bar" style="height:80%;"></div><div class="emb-bar" style="height:90%;"></div>
        <div class="emb-bar" style="height:35%;"></div><div class="emb-bar" style="height:88%;"></div>
        <div class="emb-bar" style="height:72%;"></div><div class="emb-bar" style="height:60%;"></div>
        <div class="emb-bar" style="height:92%;"></div><div class="emb-bar" style="height:48%;"></div>
        <div class="emb-bar" style="height:84%;"></div><div class="emb-bar" style="height:76%;"></div>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:10px; color:#94a3b8;">
        <span>Normalized L2 Feature Tensor (128 Coordinates)</span>
        <span style="color:#38bdf8; font-weight:700;">Triplet Loss Margin: α = 0.20</span>
      </div>
    </div>

    <!-- The Veil Consent Controller -->
    <div class="veil-status-box">
      <div class="veil-text">
        <h4>Dynamic Unblur Request ("The Veil")</h4>
        <p>Real-time push consent notification sent to Bystander #2 for identity unlock.</p>
      </div>
      <button class="btn-veil">⚡ Send Consent Push</button>
    </div>

    <!-- Audit Log -->
    <div class="card-box" style="flex:1;">
      <div class="card-title">🔐 Cryptographic Consent & Audit Verification Log</div>
      <table class="audit-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Subject</th>
            <th>Action Performed</th>
            <th>Metric / Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>22:04:18</td>
            <td>User #894 (Adarsh S)</td>
            <td>Biometric Descriptors Match</td>
            <td><span style="color:#34d399; font-weight:700;">VERIFIED (d=0.38)</span></td>
          </tr>
          <tr>
            <td>22:04:18</td>
            <td>Bystander #2</td>
            <td>Gaussian Blur Mask Applied</td>
            <td><span style="color:#ef4444; font-weight:700;">BLURRED (Kernel 25x25)</span></td>
          </tr>
          <tr>
            <td>22:04:19</td>
            <td>System Audit</td>
            <td>GDPR Art. 6 Audit Trail Logged</td>
            <td><span style="color:#38bdf8; font-weight:700;">SHA-256 SECURED</span></td>
          </tr>
          <tr>
            <td>22:04:20</td>
            <td>Django Cache</td>
            <td>In-Memory Descriptors Refreshed</td>
            <td><span style="color:#a855f7; font-weight:700;">LATENCY: 7.8 ms</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

</body>
</html>
"""

# -------------------------------------------------------------
# 3. HTML Showcase for Deciphera (1920x1080 Frame)
# -------------------------------------------------------------
deciphera_showcase_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Deciphera - Epigraphical Archival & Multi-Scale Transliteration Suite</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
  body { background: radial-gradient(circle at 50% 10%, #1e1b4b, #0f172a); color: #f8fafc; padding: 16px; width: 1920px; height: 1080px; overflow: hidden; }
  
  .header { display: flex; justify-content: space-between; align-items: center; background: rgba(30, 27, 75, 0.7); backdrop-filter: blur(14px); border: 1px solid rgba(165, 180, 252, 0.2); border-radius: 12px; padding: 12px 24px; margin-bottom: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
  .logo-group { display: flex; align-items: center; gap: 14px; }
  .logo-icon { width: 38px; height: 38px; background: linear-gradient(135deg, #6366f1, #a855f7); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
  .title-h1 { font-size: 20px; font-weight: 700; color: #ffffff; }
  .subtitle { font-size: 11.5px; color: #c7d2fe; margin-top: 1px; }
  .badges { display: flex; gap: 8px; }
  .badge { font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 20px; }
  .badge-active { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.4); }
  
  .grid-container { display: grid; grid-template-columns: 1.15fr 1fr; gap: 12px; height: calc(1080px - 95px); }
  .panel { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(16px); border: 1px solid rgba(165, 180, 252, 0.15); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
  .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(165, 180, 252, 0.15); padding-bottom: 8px; }
  .panel-title { font-size: 14px; font-weight: 700; color: #e2e8f0; display: flex; align-items: center; gap: 8px; }
  
  .stone-view { width: 100%; height: 490px; background: #090d16; border-radius: 8px; border: 1px solid rgba(165, 180, 252, 0.2); display: flex; flex-direction: column; padding: 14px; gap: 10px; }
  .stone-canvas { flex: 1; background: #181c2b; border-radius: 8px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
  
  .translit-card { background: rgba(30, 27, 75, 0.5); border: 1px solid rgba(165, 180, 252, 0.2); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
  .translit-row { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 8px; background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 6px; }
  .t-box { text-align: center; }
  .t-label { font-size: 9.5px; color: #a5b4fc; text-transform: uppercase; font-weight: 600; }
  .t-val { font-size: 15px; font-weight: 700; color: #ffffff; margin-top: 2px; }
  
  .timeline { display: flex; justify-content: space-between; position: relative; padding: 12px 10px; background: rgba(30, 27, 75, 0.4); border-radius: 8px; }
  .epoch-node { text-align: center; position: relative; z-index: 2; }
  .epoch-dot { width: 12px; height: 12px; border-radius: 50%; background: #6366f1; margin: 0 auto 4px; box-shadow: 0 0 8px #6366f1; }
  .epoch-active { background: #38bdf8; box-shadow: 0 0 12px #38bdf8; }
  .epoch-title { font-size: 10.5px; font-weight: 700; color: #f8fafc; }
  .epoch-dates { font-size: 8.5px; color: #94a3b8; }
</style>
</head>
<body>

<div class="header">
  <div class="logo-group">
    <div class="logo-icon">📜</div>
    <div>
      <div class="title-h1">Deciphera — Epigraphical Archival & Multi-Scale Transliteration Suite</div>
      <div class="subtitle">Multi-Scale Retinex Enhancement • Brahmi/Grantha/Vatteluttu Phoneme Transliteration • Dynasty Chronometry Mapping</div>
    </div>
  </div>
  <div class="badges">
    <div class="badge badge-active">● Corpus Transliteration Engine: Active</div>
  </div>
</div>

<div class="grid-container">
  <!-- Left Panel -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">🏛️ Multi-Scale Retinex & Morphological Top-Hat Binarization</div>
      <span style="font-size: 10.5px; color: #38bdf8; font-weight: 600;">Chera Dynasty Stone Epigraph #104</span>
    </div>

    <div class="stone-view">
      <div class="stone-canvas">
        <svg width="100%" height="100%" viewBox="0 0 700 360">
          <rect x="20" y="20" width="660" height="320" rx="12" fill="#1c2438" stroke="#4338ca" stroke-width="2"/>
          <text x="50" y="65" fill="#a5b4fc" font-size="13" font-weight="bold">ANCIENT STONE EPIGRAPHICAL INSCRIPTION (MSRCR ENHANCED)</text>
          
          <g fill="none" stroke="#38bdf8" stroke-width="3" stroke-linecap="round">
            <path d="M60,140 Q90,100 120,140 T180,140"/>
            <circle cx="230" cy="140" r="22"/>
            <path d="M280,115 L320,165 M320,115 L280,165"/>
            <path d="M370,120 Q410,170 450,120"/>
            <path d="M500,115 Q520,140 500,165 Q540,165 560,115"/>
            <circle cx="610" cy="140" r="18"/>
            
            <path d="M60,240 Q100,200 140,240 Q180,280 220,240"/>
            <path d="M270,220 L330,220 M300,220 L300,265"/>
            <circle cx="380" cy="240" r="20"/>
            <path d="M430,215 Q470,265 510,215"/>
            <path d="M560,215 L620,265"/>
          </g>
          
          <rect x="50" y="95" width="140" height="75" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,2"/>
          <rect x="210" y="95" width="130" height="75" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,2"/>
          <rect x="355" y="95" width="120" height="75" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,2"/>
          <rect x="490" y="95" width="145" height="75" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,2"/>
        </svg>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:10.5px; color:#cbd5e1;">
        <span>Filter: <b>Multi-Scale Retinex (MSRCR) + Top-Hat Binarization</b></span>
        <span style="color:#34d399; font-weight:700;">PSNR: 24.8 dB • Contrast Gain: +340%</span>
      </div>
    </div>
  </div>

  <!-- Right Panel -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">🌐 Multi-Script Epigraphical Transliteration Matrix</div>
      <span style="font-size: 10.5px; color: #a855f7;">ISO-15919 Standard</span>
    </div>

    <div class="translit-card">
      <div class="translit-row">
        <div class="t-box">
          <div class="t-label">Vatteluttu Phoneme</div>
          <div class="t-val" style="color:#38bdf8;">𑌕𑌰𑌣𑌾</div>
        </div>
        <div class="t-box">
          <div class="t-label">Unicode Malayalam</div>
          <div class="t-val" style="color:#34d399;">കരുണ (Karuṇa)</div>
        </div>
        <div class="t-box">
          <div class="t-label">Devanagari Sanskrit</div>
          <div class="t-val" style="color:#f59e0b;">करुणा</div>
        </div>
      </div>

      <div class="translit-row">
        <div class="t-box">
          <div class="t-label">Grantha Script</div>
          <div class="t-val" style="color:#38bdf8;">𑌅𑌕𑍍𑌷𑌰𑌮𑍍</div>
        </div>
        <div class="t-box">
          <div class="t-label">Unicode Malayalam</div>
          <div class="t-val" style="color:#34d399;">അക്ഷരം (Akṣaram)</div>
        </div>
        <div class="t-box">
          <div class="t-label">Devanagari Sanskrit</div>
          <div class="t-val" style="color:#f59e0b;">अक्षरम्</div>
        </div>
      </div>
    </div>

    <div class="panel-header" style="margin-top:2px;">
      <div class="panel-title">⏳ Palaeographic Dynasty Chronometry Mapping</div>
    </div>
    
    <div class="timeline">
      <div class="epoch-node">
        <div class="epoch-dot"></div>
        <div class="epoch-title">Early Brahmi</div>
        <div class="epoch-dates">3rd c. BCE – 2nd c. CE</div>
      </div>
      <div class="epoch-node">
        <div class="epoch-dot"></div>
        <div class="epoch-title">Early Grantha</div>
        <div class="epoch-dates">5th c. – 8th c. CE</div>
      </div>
      <div class="epoch-node">
        <div class="epoch-dot epoch-active"></div>
        <div class="epoch-title" style="color:#38bdf8;">Vatteluttu (Chera)</div>
        <div class="epoch-dates">9th c. – 12th c. CE</div>
      </div>
      <div class="epoch-node">
        <div class="epoch-dot"></div>
        <div class="epoch-title">Arya Ezhuthu</div>
        <div class="epoch-dates">16th c. CE – Present</div>
      </div>
    </div>

    <div class="translit-card" style="flex:1;">
      <div style="font-size:11.5px; font-weight:700; color:#e2e8f0;">🏛️ Historical Exegesis & Inscription Classification</div>
      <p style="font-size:10.5px; color:#94a3b8; line-height:1.4;">
        <b>Ductus Classification:</b> Second Chera Dynasty (Kulasekhara Period, Mahodaya Puram).<br/>
        <b>Epigraphical Theme:</b> Royal Land Endowment Grant & Temple Votive Inscription.<br/>
        <b>Phonological Features:</b> Archaic alveolar rhotic nasalization with Grantha Sanskrit compound integration.
      </p>
    </div>
  </div>
</div>

</body>
</html>
"""

def generate_all_showcase_images():
    os.makedirs(downloads_dir, exist_ok=True)
    
    epi_html_path = os.path.abspath("epigraphix_showcase.html")
    assent_html_path = os.path.abspath("assenttag_showcase.html")
    deciphera_html_path = os.path.abspath("deciphera_showcase.html")

    with open(epi_html_path, "w", encoding="utf-8") as f:
        f.write(epigraphix_showcase_html)
    with open(assent_html_path, "w", encoding="utf-8") as f:
        f.write(assenttag_showcase_html)
    with open(deciphera_html_path, "w", encoding="utf-8") as f:
        f.write(deciphera_showcase_html)

    out_epi = os.path.join(downloads_dir, "EpigraphiX_AI_Index_Showcase.png")
    out_assent = os.path.join(downloads_dir, "AssentTag_Index_Showcase.png")
    out_deciphera = os.path.join(downloads_dir, "Deciphera_Index_Showcase.png")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. EpigraphiX-AI
        print("Capturing EpigraphiX-AI Index Showcase...")
        page_epi = browser.new_page(viewport={"width": 1920, "height": 1080})
        page_epi.goto("file:///" + epi_html_path.replace("\\", "/"))
        page_epi.wait_for_timeout(500)
        page_epi.screenshot(path=out_epi, full_page=False)
        print(f"Generated: {out_epi}")

        # 2. AssentTag
        print("Capturing AssentTag Index Showcase...")
        page_assent = browser.new_page(viewport={"width": 1920, "height": 1080})
        page_assent.goto("file:///" + assent_html_path.replace("\\", "/"))
        page_assent.wait_for_timeout(500)
        page_assent.screenshot(path=out_assent, full_page=False)
        print(f"Generated: {out_assent}")

        # 3. Deciphera
        print("Capturing Deciphera Index Showcase...")
        page_dec = browser.new_page(viewport={"width": 1920, "height": 1080})
        page_dec.goto("file:///" + deciphera_html_path.replace("\\", "/"))
        page_dec.wait_for_timeout(500)
        page_dec.screenshot(path=out_deciphera, full_page=False)
        print(f"Generated: {out_deciphera}")

        browser.close()

    # Clean up temporary HTML files
    for tmp in [epi_html_path, assent_html_path, deciphera_html_path]:
        if os.path.exists(tmp):
            os.remove(tmp)

    print("\nSUCCESS: All 3 LinkedIn Media Showcase PNGs generated in Downloads!")

if __name__ == "__main__":
    generate_all_showcase_images()
