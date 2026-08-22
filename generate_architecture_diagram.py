#!/usr/bin/env python3
"""
Generate a professional, publication-quality System Architecture Diagram for EpigraphiX-AI
Matching the clean, colorful box-and-arrow flowchart style.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rectangle(draw, xy, corner_radius, fill, outline, width=3):
    """Draw a smooth rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=corner_radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, points, color=(35, 35, 35), width=3, arrow_size=18):
    """Draw orthogonal lines with a crisp directional arrowhead at the final segment."""
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)
    
    if arrow_size <= 0:
        return

    # Calculate arrowhead at final segment
    p_last = points[-1]
    p_prev = points[-2]
    dx = p_last[0] - p_prev[0]
    dy = p_last[1] - p_prev[1]
    angle = math.atan2(dy, dx)

    # Arrowhead polygon
    arrow_p1 = (
        p_last[0] - arrow_size * math.cos(angle - math.pi / 5.5),
        p_last[1] - arrow_size * math.sin(angle - math.pi / 5.5)
    )
    arrow_p2 = (
        p_last[0] - arrow_size * math.cos(angle + math.pi / 5.5),
        p_last[1] - arrow_size * math.sin(angle + math.pi / 5.5)
    )
    draw.polygon([p_last, arrow_p1, arrow_p2], fill=color)

def draw_centered_text(draw, box, lines, font_reg, font_bold, text_color=(25, 25, 25), line_spacing=10):
    """Draw multiple centered lines of text inside a box."""
    x0, y0, x1, y1 = box
    box_w = x1 - x0
    box_h = y1 - y0

    line_heights = []
    line_widths = []
    for text, is_bold in lines:
        f = font_bold if is_bold else font_reg
        bbox = draw.textbbox((0, 0), text, font=f)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        line_widths.append(w)
        line_heights.append(h)
    
    total_text_h = sum(line_heights) + (len(lines) - 1) * line_spacing
    cur_y = y0 + (box_h - total_text_h) / 2

    for idx, (text, is_bold) in enumerate(lines):
        f = font_bold if is_bold else font_reg
        w = line_widths[idx]
        cur_x = x0 + (box_w - w) / 2
        draw.text((cur_x, cur_y), text, fill=text_color, font=f)
        cur_y += line_heights[idx] + line_spacing

def generate_architecture_diagram():
    # 2x supersampling for razor-sharp vector-grade rasterization
    SCALE = 2
    W = 1600 * SCALE
    H = 960 * SCALE

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_path_bold = r"C:\Windows\Fonts\segoeuib.ttf"
    font_path_reg = r"C:\Windows\Fonts\segoeui.ttf"
    
    box_bold = ImageFont.truetype(font_path_bold, 20 * SCALE)
    box_reg = ImageFont.truetype(font_path_reg, 15 * SCALE)
    arrow_font = ImageFont.truetype(font_path_bold, 17 * SCALE)
    arrow_sub = ImageFont.truetype(font_path_reg, 14 * SCALE)

    # Pastel Color Palette matching reference style
    # USER box (Soft Pastel Blue)
    COLOR_BLUE_FILL = (220, 235, 252)
    COLOR_BLUE_BORDER = (120, 165, 230)
    
    # Pre-processing & Comparative (Soft Pastel Green)
    COLOR_GREEN_FILL = (215, 238, 218)
    COLOR_GREEN_BORDER = (115, 175, 105)
    
    # ML & Neural Modules (Warm Golden Yellow)
    COLOR_YELLOW_FILL = (255, 243, 205)
    COLOR_YELLOW_BORDER = (225, 185, 80)
    
    ARROW_COLOR = (30, 30, 30)
    TEXT_COLOR = (25, 25, 25)

    # Box Dimensions
    RADIUS = 18 * SCALE
    BORDER_WIDTH = 3 * SCALE
    LINE_WIDTH = 4 * SCALE
    ARROW_HEAD = 18 * SCALE

    # 1. USER Box (Left)
    user_box = [60 * SCALE, 440 * SCALE, 320 * SCALE, 570 * SCALE]

    # 2. Pre-processing Box (Top Center)
    prep_box = [420 * SCALE, 60 * SCALE, 860 * SCALE, 200 * SCALE]

    # 3. Traditional ML Module (Middle Left)
    trad_box = [460 * SCALE, 380 * SCALE, 840 * SCALE, 530 * SCALE]

    # 4. Neural Transformer & CNN Module (Middle Right)
    neural_box = [940 * SCALE, 380 * SCALE, 1340 * SCALE, 530 * SCALE]

    # 5. Comparative Analysis & Linguistic Decoder (Bottom Center)
    comp_box = [640 * SCALE, 690 * SCALE, 1160 * SCALE, 830 * SCALE]

    # Draw Boxes
    draw_rounded_rectangle(draw, user_box, RADIUS, COLOR_BLUE_FILL, COLOR_BLUE_BORDER, BORDER_WIDTH)
    draw_rounded_rectangle(draw, prep_box, RADIUS, COLOR_GREEN_FILL, COLOR_GREEN_BORDER, BORDER_WIDTH)
    draw_rounded_rectangle(draw, trad_box, RADIUS, COLOR_YELLOW_FILL, COLOR_YELLOW_BORDER, BORDER_WIDTH)
    draw_rounded_rectangle(draw, neural_box, RADIUS, COLOR_YELLOW_FILL, COLOR_YELLOW_BORDER, BORDER_WIDTH)
    draw_rounded_rectangle(draw, comp_box, RADIUS, COLOR_GREEN_FILL, COLOR_GREEN_BORDER, BORDER_WIDTH)

    # Box Text Contents
    draw_centered_text(draw, user_box, [
        ("USER / RESEARCHER", True),
        ("Historical Manuscript Upload", False)
    ], box_reg, box_bold)

    draw_centered_text(draw, prep_box, [
        ("Image Pre-Processing & Restoration", True),
        ("Fiber-Aware Inpainting (FANI 2.0) | Adaptive Sauvola", False),
        ("3D Surface Photometric Stereo (PTM)", False)
    ], box_reg, box_bold)

    draw_centered_text(draw, trad_box, [
        ("Traditional ML Space", True),
        ("Topological Betti Filtration (B0, B1)", False),
        ("SVM | Random Forest | k-NN | GNB", True)
    ], box_reg, box_bold)

    draw_centered_text(draw, neural_box, [
        ("Neural Vision Transformer", True),
        ("TrOCR Multi-Head Self-Attention", False),
        ("CNN Neural Lattice & Glyph Cuts", True)
    ], box_reg, box_bold)

    draw_centered_text(draw, comp_box, [
        ("Comparative Epigraphical Analysis", True),
        ("Sandhi Trie Lexicon | DP Levenshtein Alignment", False),
        ("Trilingual Translation & Vector PDF Report", True)
    ], box_reg, box_bold)

    # --- Draw Connecting Orthogonal Arrows ---

    # 1. USER -> Pre-processing
    user_center_x = (user_box[0] + user_box[2]) // 2
    prep_left_center = (prep_box[0], (prep_box[1] + prep_box[3]) // 2)
    
    draw_arrow(draw, [
        (user_center_x, user_box[1]),
        (user_center_x, prep_left_center[1]),
        prep_left_center
    ], ARROW_COLOR, LINE_WIDTH, ARROW_HEAD)
    
    # Label to the LEFT of the vertical line
    draw.text((user_center_x - 170 * SCALE, 280 * SCALE), "Palm-Leaf", fill=TEXT_COLOR, font=arrow_font)
    draw.text((user_center_x - 170 * SCALE, 305 * SCALE), "Manuscript Image", fill=(70, 70, 70), font=arrow_sub)

    # 2. Pre-processing -> Branch split -> (Traditional ML & Neural Transformer)
    prep_right_center = (prep_box[2], (prep_box[1] + prep_box[3]) // 2)
    trad_top_center = ((trad_box[0] + trad_box[2]) // 2, trad_box[1])
    neural_top_center = ((neural_box[0] + neural_box[2]) // 2, neural_box[1])
    split_x = (trad_top_center[0] + neural_top_center[0]) // 2 # 890 * SCALE
    split_y = 280 * SCALE

    # Main trunk from prep to split point
    draw_arrow(draw, [prep_right_center, (split_x, prep_right_center[1]), (split_x, split_y)], ARROW_COLOR, LINE_WIDTH, arrow_size=0)
    draw.text((prep_box[2] + 25 * SCALE, prep_right_center[1] - 32 * SCALE), "Pre-Processed & Enhanced Image", fill=TEXT_COLOR, font=arrow_font)

    # Branch down to Traditional ML
    draw_arrow(draw, [(split_x, split_y), (trad_top_center[0], split_y), trad_top_center], ARROW_COLOR, LINE_WIDTH, ARROW_HEAD)

    # Branch down to Neural Transformer
    draw_arrow(draw, [(split_x, split_y), (neural_top_center[0], split_y), neural_top_center], ARROW_COLOR, LINE_WIDTH, ARROW_HEAD)

    # 3. Traditional ML & Neural Transformer -> Comparative Analysis
    trad_bot_center = ((trad_box[0] + trad_box[2]) // 2, trad_box[3])
    neural_bot_center = ((neural_box[0] + neural_box[2]) // 2, neural_box[3])
    comp_top_center = ((comp_box[0] + comp_box[2]) // 2, comp_box[1])
    merge_y = 610 * SCALE

    # Drop from Trad ML
    draw_arrow(draw, [trad_bot_center, (trad_bot_center[0], merge_y), (comp_top_center[0], merge_y)], ARROW_COLOR, LINE_WIDTH, arrow_size=0)
    draw.text((trad_bot_center[0] - 220 * SCALE, trad_bot_center[1] + 22 * SCALE), "Accuracy & Betti Vector", fill=TEXT_COLOR, font=arrow_font)

    # Drop from Neural Transformer
    draw_arrow(draw, [neural_bot_center, (neural_bot_center[0], merge_y), (comp_top_center[0], merge_y)], ARROW_COLOR, LINE_WIDTH, arrow_size=0)
    draw.text((neural_bot_center[0] + 15 * SCALE, neural_bot_center[1] + 22 * SCALE), "Confidence & Attention Maps", fill=TEXT_COLOR, font=arrow_font)

    # Merge down into Comparative Analysis box
    draw_arrow(draw, [(comp_top_center[0], merge_y), comp_top_center], ARROW_COLOR, LINE_WIDTH, ARROW_HEAD)

    # 4. Comparative Analysis -> USER (Return Flow)
    comp_left_center = (comp_box[0], (comp_box[1] + comp_box[3]) // 2)
    return_y = 900 * SCALE
    turn_x = 420 * SCALE

    # Clean rectangular loop: Left from comp_box -> turn down to return_y -> left to user_center_x -> UP into user_box bottom
    draw_arrow(draw, [
        comp_left_center,
        (turn_x, comp_left_center[1]),
        (turn_x, return_y),
        (user_center_x, return_y),
        (user_center_x, user_box[3])
    ], ARROW_COLOR, LINE_WIDTH, ARROW_HEAD)

    # Return flow label placed above the return line with zero overlap
    label_text = "Dual-Pipeline Transcriptions & Vector PDF Evaluation Report"
    draw.text((turn_x + 25 * SCALE, return_y - 32 * SCALE), label_text, fill=TEXT_COLOR, font=arrow_font)

    # Resize with antialiasing for ultra-crisp output
    final_img = img.resize((1600, 960), Image.Resampling.LANCZOS)
    
    # Save locations
    downloads_path = os.path.expanduser(r"~\Downloads\epigraphix_ai_system_architecture.png")
    local_path = os.path.abspath("epigraphix_ai_system_architecture.png")
    paper_fig_path = os.path.abspath(os.path.join("paper_figures", "epigraphix_ai_system_architecture.png"))
    artifact_path = r"C:\Users\HP\.gemini\antigravity\brain\eea0873d-fb47-4568-adb1-9f3b449c3539\epigraphix_ai_system_architecture.png"

    final_img.save(downloads_path, dpi=(300, 300))
    final_img.save(local_path, dpi=(300, 300))
    if os.path.exists("paper_figures"):
        final_img.save(paper_fig_path, dpi=(300, 300))
    try:
        final_img.save(artifact_path, dpi=(300, 300))
    except Exception:
        pass

    print(f"[OK] Architecture image successfully updated:")
    print(f"     - Downloads : {downloads_path}")
    print(f"     - Project   : {local_path}")
    print(f"     - Artifacts : {artifact_path}")

if __name__ == "__main__":
    generate_architecture_diagram()
