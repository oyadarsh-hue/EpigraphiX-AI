#!/usr/bin/env python3
"""
Generate publication-quality Black & White DFD Diagrams (Level 0, Level 1, Level 2) for EpigraphiX-AI
Matching classic academic textbook / research paper B&W formatting.
Features:
- Pure Black & White (White background and fill, Solid Black borders, lines, and text)
- Exact trigonometric circle boundary intersection (arrows touch circles with 0 gap / 0 overshoot)
- Centered arrow labels with zero overlap or word collision
- Overwrites all PNGs in Downloads, Project Root, and Paper Figures
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# =================================================================
# GEOMETRY & DRAWING HELPERS
# =================================================================

def draw_entity_box(draw, xy, name, subtitle=None, font_bold=None, font_reg=None, width=3):
    """
    Draws a standard classic DFD External Entity: rectangle with a vertical sub-divider line on the right/left.
    """
    x0, y0, x1, y1 = xy
    # Base white rectangle with black border
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(0, 0, 0), width=width)
    
    # Inner vertical sub-bar line (Yourdon / Gane-Sarson style)
    sub_bar_x = x1 - (x1 - x0) * 0.18
    draw.line([sub_bar_x, y0, sub_bar_x, y1], fill=(0, 0, 0), width=width)

    # Main text area
    text_w = sub_bar_x - x0
    bbox = draw.textbbox((0, 0), name, font=font_bold)
    nw = bbox[2] - bbox[0]
    nh = bbox[3] - bbox[1]

    if subtitle and font_reg:
        sbox = draw.textbbox((0, 0), subtitle, font=font_reg)
        sw = sbox[2] - sbox[0]
        sh = sbox[3] - sbox[1]
        total_h = nh + sh + 6
        cur_y = y0 + (y1 - y0 - total_h) / 2
        draw.text((x0 + (text_w - nw) / 2, cur_y), name, fill=(0, 0, 0), font=font_bold)
        draw.text((x0 + (text_w - sw) / 2, cur_y + nh + 6), subtitle, fill=(0, 0, 0), font=font_reg)
    else:
        cur_y = y0 + (y1 - y0 - nh) / 2
        draw.text((x0 + (text_w - nw) / 2, cur_y), name, fill=(0, 0, 0), font=font_bold)

def circle_boundary_at_y(center, radius, y, side='left'):
    """Returns the exact x on circle perimeter for a given y coordinate."""
    cx, cy = center
    dy = y - cy
    if abs(dy) > radius:
        return (cx - radius if side == 'left' else cx + radius, y)
    dx = math.sqrt(max(0, radius**2 - dy**2))
    x = cx - dx if side == 'left' else cx + dx
    return (x, y)

def circle_boundary_at_x(center, radius, x, side='top'):
    """Returns the exact y on circle perimeter for a given x coordinate."""
    cx, cy = center
    dx = x - cx
    if abs(dx) > radius:
        return (x, cy - radius if side == 'top' else cy + radius)
    dy = math.sqrt(max(0, radius**2 - dx**2))
    y = cy - dy if side == 'top' else cy + dy
    return (x, y)

def draw_dfd_process_bw(draw, center, radius, process_num, title_lines, font_num, font_reg, font_bold, width=3):
    """
    Draws a classic Black & White DFD process bubble (white circle, black border, horizontal dividing chord).
    """
    cx, cy = center
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]

    # White circle with black border
    draw.ellipse(bbox, fill=(255, 255, 255), outline=(0, 0, 0), width=width)

    # Top dividing chord line
    line_y = cy - radius * 0.45
    dy = cy - line_y
    dx = math.sqrt(max(0, radius**2 - dy**2))
    draw.line([cx - dx, line_y, cx + dx, line_y], fill=(0, 0, 0), width=width)

    # Process Number in top segment
    n_box = draw.textbbox((0, 0), str(process_num), font=font_num)
    nw = n_box[2] - n_box[0]
    nh = n_box[3] - n_box[1]
    num_y = (cy - radius + line_y) / 2 - nh / 2
    draw.text((cx - nw / 2, num_y), str(process_num), fill=(0, 0, 0), font=font_num)

    # Title lines centered in main body
    main_top = line_y
    main_bot = cy + radius * 0.88
    main_h = main_bot - main_top

    line_heights = []
    line_widths = []
    for text, is_bold in title_lines:
        f = font_bold if is_bold else font_reg
        t_box = draw.textbbox((0, 0), text, font=f)
        line_widths.append(t_box[2] - t_box[0])
        line_heights.append(t_box[3] - t_box[1])

    line_spacing = 6
    total_text_h = sum(line_heights) + (len(title_lines) - 1) * line_spacing
    cur_y = main_top + (main_h - total_text_h) / 2

    for idx, (text, is_bold) in enumerate(title_lines):
        f = font_bold if is_bold else font_reg
        w = line_widths[idx]
        draw.text((cx - w / 2, cur_y), text, fill=(0, 0, 0), font=f)
        cur_y += line_heights[idx] + line_spacing

def draw_data_store_bw(draw, xy, store_id, name, font_id, font_name, width=3):
    """Draws a classic Black & White DFD Data Store (open right rectangle with ID separator)."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    
    # Top, Bottom, and Left lines (Right is OPEN)
    draw.line([x0, y0, x1, y0], fill=(0, 0, 0), width=width)
    draw.line([x0, y1, x1, y1], fill=(0, 0, 0), width=width)
    draw.line([x0, y0, x0, y1], fill=(0, 0, 0), width=width)
    
    # ID vertical separator
    id_w = (y1 - y0) * 0.95
    draw.line([x0 + id_w, y0, x0 + id_w, y1], fill=(0, 0, 0), width=width)

    # Text
    ibox = draw.textbbox((0, 0), store_id, font=font_id)
    draw.text((x0 + (id_w - (ibox[2]-ibox[0]))/2, y0 + (y1-y0-(ibox[3]-ibox[1]))/2), store_id, fill=(0,0,0), font=font_id)

    nbox = draw.textbbox((0, 0), name, font=font_name)
    draw.text((x0 + id_w + 14, y0 + (y1-y0-(nbox[3]-nbox[1]))/2), name, fill=(0,0,0), font=font_name)

def draw_arrow(draw, points, color=(0, 0, 0), width=3, arrow_size=18):
    """Draw orthogonal lines with a solid black arrowhead touching the destination."""
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)
    
    if arrow_size <= 0:
        return

    p_last = points[-1]
    p_prev = points[-2]
    dx = p_last[0] - p_prev[0]
    dy = p_last[1] - p_prev[1]
    angle = math.atan2(dy, dx)

    arrow_p1 = (
        p_last[0] - arrow_size * math.cos(angle - math.pi / 5.5),
        p_last[1] - arrow_size * math.sin(angle - math.pi / 5.5)
    )
    arrow_p2 = (
        p_last[0] - arrow_size * math.cos(angle + math.pi / 5.5),
        p_last[1] - arrow_size * math.sin(angle + math.pi / 5.5)
    )
    draw.polygon([p_last, arrow_p1, arrow_p2], fill=color)

def draw_centered_arrow_label(draw, x_start, x_end, y_pos, lines, font_bold, font_sub=None, line_spacing=4):
    """Draws multiple lines of text perfectly horizontally centered between x_start and x_end."""
    mid_x = (x_start + x_end) / 2
    
    line_heights = []
    line_widths = []
    for text, is_bold in lines:
        f = font_bold if is_bold else font_sub
        bbox = draw.textbbox((0, 0), text, font=f)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])
    
    cur_y = y_pos
    for idx, (text, is_bold) in enumerate(lines):
        f = font_bold if is_bold else font_sub
        w = line_widths[idx]
        draw.text((mid_x - w / 2, cur_y), text, fill=(0, 0, 0), font=f)
        cur_y += line_heights[idx] + line_spacing

# =================================================================
# 1. DFD LEVEL 0 (Context Level Diagram - Pure Black & White)
# =================================================================
def generate_dfd_level_0():
    SCALE = 2
    W = 1500 * SCALE
    H = 650 * SCALE

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22 * SCALE)
    font_reg = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16 * SCALE)
    font_num = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24 * SCALE)
    arrow_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17 * SCALE)
    arrow_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14 * SCALE)

    # Title
    title_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26 * SCALE)
    draw.text((60 * SCALE, 35 * SCALE), "DFD Level 0: Context Level Diagram", fill=(0, 0, 0), font=title_font)

    # External Entity: USER (Left)
    user_box = [80 * SCALE, 210 * SCALE, 360 * SCALE, 450 * SCALE]
    draw_entity_box(draw, user_box, "USER", "Epigraphist / Researcher", font_bold, font_reg, width=3 * SCALE)

    # Central Process Bubble: 0 (Right)
    proc_center = (1120 * SCALE, 330 * SCALE)
    proc_radius = 175 * SCALE
    draw_dfd_process_bw(draw, proc_center, proc_radius, "0", [
        ("EPIGRAPHIX-AI", True),
        ("Neural Palm-Leaf OCR &", False),
        ("Intelligence Suite", True)
    ], font_num, font_reg, font_bold, width=3 * SCALE)

    # Exact Circle Intersections
    top_y = 265 * SCALE
    bot_y = 395 * SCALE
    
    circle_in_top = circle_boundary_at_y(proc_center, proc_radius, top_y, side='left')
    circle_out_bot = circle_boundary_at_y(proc_center, proc_radius, bot_y, side='left')

    # Top Arrow: USER -> Process
    draw_arrow(draw, [(user_box[2], top_y), circle_in_top], (0, 0, 0), 3 * SCALE, 18 * SCALE)
    # Centered text in middle of the gap (NO overlap!)
    draw_centered_arrow_label(draw, user_box[2], circle_in_top[0], top_y - 50 * SCALE, [
        ("Required Format and Palm-Leaf Manuscript Scans", True),
        ("(Thaliyola Images & Recognition Parameters)", False)
    ], arrow_font, arrow_sub)

    # Bottom Arrow: Process -> USER
    draw_arrow(draw, [circle_out_bot, (user_box[2], bot_y)], (0, 0, 0), 3 * SCALE, 18 * SCALE)
    # Centered text in middle of the gap (NO overlap!)
    draw_centered_arrow_label(draw, user_box[2], circle_out_bot[0], bot_y + 12 * SCALE, [
        ("Recognized Text, Trilingual Translation & Vector PDF Reports", True),
        ("(Malayalam, English, Hindi Transcriptions & Gauges)", False)
    ], arrow_font, arrow_sub)

    final_img = img.resize((1500, 650), Image.Resampling.LANCZOS)
    
    p1 = os.path.expanduser(r"~\Downloads\dfd_level_0.png")
    p2 = os.path.abspath("dfd_level_0.png")
    p3 = r"C:\Users\HP\.gemini\antigravity\brain\eea0873d-fb47-4568-adb1-9f3b449c3539\dfd_level_0.png"
    paper_p = os.path.abspath(os.path.join("paper_figures", "dfd_level_0.png"))

    final_img.save(p1, dpi=(300, 300))
    final_img.save(p2, dpi=(300, 300))
    if os.path.exists("paper_figures"): final_img.save(paper_p, dpi=(300, 300))
    try: final_img.save(p3, dpi=(300, 300))
    except Exception: pass
    print(f"[OK] B&W DFD Level 0 saved to {p1}")

# =================================================================
# 2. DFD LEVEL 1 (Process Decomposition Diagram - Pure Black & White)
# =================================================================
def generate_dfd_level_1():
    SCALE = 2
    W = 1650 * SCALE
    H = 1000 * SCALE

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 19 * SCALE)
    font_reg = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14 * SCALE)
    font_num = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20 * SCALE)
    arrow_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 15 * SCALE)
    arrow_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 12 * SCALE)

    # Title
    title_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26 * SCALE)
    draw.text((60 * SCALE, 35 * SCALE), "DFD Level 1: System Process Decomposition", fill=(0, 0, 0), font=title_font)

    # Entity: USER (Left)
    user_box = [60 * SCALE, 440 * SCALE, 260 * SCALE, 570 * SCALE]
    draw_entity_box(draw, user_box, "USER", "Researcher", font_bold, font_reg, width=3 * SCALE)

    # Process 1.0 (Top Center-Left)
    p1_c = (520 * SCALE, 250 * SCALE); p1_r = 125 * SCALE
    draw_dfd_process_bw(draw, p1_c, p1_r, "1.0", [
        ("Image Pre-Processing", True),
        ("& Inpainting", True),
        ("(FANI 2.0 / Sauvola)", False)
    ], font_num, font_reg, font_bold, width=3 * SCALE)

    # Process 2.0 (Bottom Center-Left)
    p2_c = (520 * SCALE, 680 * SCALE); p2_r = 125 * SCALE
    draw_dfd_process_bw(draw, p2_c, p2_r, "2.0", [
        ("Topological Feature", True),
        ("Extraction", True),
        ("(Betti Loops B0, B1)", False)
    ], font_num, font_reg, font_bold, width=3 * SCALE)

    # Process 3.0 (Top Right)
    p3_c = (1080 * SCALE, 250 * SCALE); p3_r = 125 * SCALE
    draw_dfd_process_bw(draw, p3_c, p3_r, "3.0", [
        ("TrOCR & ML Decision", True),
        ("Classification", True),
        ("(Transformers / SVM)", False)
    ], font_num, font_reg, font_bold, width=3 * SCALE)

    # Process 4.0 (Bottom Right)
    p4_c = (1080 * SCALE, 680 * SCALE); p4_r = 125 * SCALE
    draw_dfd_process_bw(draw, p4_c, p4_r, "4.0", [
        ("Linguistic Decoding", True),
        ("& Report Generation", True),
        ("(Sandhi Trie / PDF)", False)
    ], font_num, font_reg, font_bold, width=3 * SCALE)

    # Data Store D2: Model Checkpoints
    d2_box = [1330 * SCALE, 220 * SCALE, 1600 * SCALE, 280 * SCALE]
    draw_data_store_bw(draw, d2_box, "D2", "Trained Model Weights", font_num, font_reg, width=3 * SCALE)

    # Data Store D1: Dictionary Lexicon
    d1_box = [1330 * SCALE, 650 * SCALE, 1600 * SCALE, 710 * SCALE]
    draw_data_store_bw(draw, d1_box, "D1", "Malayalam Trie Lexicon", font_num, font_reg, width=3 * SCALE)

    # --- Arrows with Exact Boundary Touching ---
    # 1. USER -> 1.0
    user_top_c = ((user_box[0] + user_box[2]) // 2, user_box[1])
    p1_in_left = circle_boundary_at_y(p1_c, p1_r, p1_c[1], side='left')
    draw_arrow(draw, [user_top_c, (user_top_c[0], p1_c[1]), p1_in_left], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw.text((user_top_c[0] + 15 * SCALE, p1_c[1] - 30 * SCALE), "Raw Manuscript Scan", fill=(0, 0, 0), font=arrow_font)

    # 2. 1.0 -> 2.0 (Down)
    p1_out_bot = circle_boundary_at_x(p1_c, p1_r, p1_c[0], side='bottom')
    p2_in_top = circle_boundary_at_x(p2_c, p2_r, p2_c[0], side='top')
    draw_arrow(draw, [p1_out_bot, p2_in_top], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw.text((p1_c[0] + 15 * SCALE, 450 * SCALE), "Denoised Binarized Image", fill=(0, 0, 0), font=arrow_font)

    # 3. 1.0 -> 3.0 (Horizontal across top)
    p1_out_right = circle_boundary_at_y(p1_c, p1_r, p1_c[1], side='right')
    p3_in_left = circle_boundary_at_y(p3_c, p3_r, p3_c[1], side='left')
    draw_arrow(draw, [p1_out_right, p3_in_left], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw_centered_arrow_label(draw, p1_out_right[0], p3_in_left[0], p1_c[1] - 30 * SCALE, [
        ("Segmented Glyph Cuts", True)
    ], arrow_font)

    # 4. 2.0 -> 3.0 (Orthogonal curve into bottom-left of 3.0)
    p2_out_right = circle_boundary_at_y(p2_c, p2_r, p2_c[1], side='right')
    target_3_y = p3_c[1] + 60 * SCALE
    p3_in_botleft = circle_boundary_at_y(p3_c, p3_r, target_3_y, side='left')
    turn_x = 800 * SCALE
    draw_arrow(draw, [p2_out_right, (turn_x, p2_c[1]), (turn_x, target_3_y), p3_in_botleft], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw.text((660 * SCALE, 690 * SCALE), "Betti Vectors (B0, B1)", fill=(0, 0, 0), font=arrow_font)

    # 5. D2 -> 3.0 (Model weights into 3.0 right edge)
    p3_in_right = circle_boundary_at_y(p3_c, p3_r, d2_box[1] + 30 * SCALE, side='right')
    draw_arrow(draw, [(d2_box[0], d2_box[1] + 30 * SCALE), p3_in_right], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((d2_box[0] - 110 * SCALE, d2_box[1] + 35 * SCALE), "Model Weights", fill=(0, 0, 0), font=arrow_sub)

    # 6. 3.0 -> 4.0 (Down)
    p3_out_bot = circle_boundary_at_x(p3_c, p3_r, p3_c[0], side='bottom')
    p4_in_top = circle_boundary_at_x(p4_c, p4_r, p4_c[0], side='top')
    draw_arrow(draw, [p3_out_bot, p4_in_top], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw.text((p3_c[0] + 15 * SCALE, 450 * SCALE), "Raw Glyph Predictions & Attention", fill=(0, 0, 0), font=arrow_font)

    # 7. D1 -> 4.0 (Lexicon into 4.0 right edge)
    p4_in_right = circle_boundary_at_y(p4_c, p4_r, d1_box[1] + 30 * SCALE, side='right')
    draw_arrow(draw, [(d1_box[0], d1_box[1] + 30 * SCALE), p4_in_right], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((d1_box[0] - 110 * SCALE, d1_box[1] + 35 * SCALE), "Grammar Rules", fill=(0, 0, 0), font=arrow_sub)

    # 8. 4.0 -> USER (Bottom return line)
    p4_out_left = circle_boundary_at_y(p4_c, p4_r, p4_c[1], side='left')
    user_bot_c = ((user_box[0] + user_box[2]) // 2, user_box[3])
    ret_y = 920 * SCALE
    draw_arrow(draw, [
        p4_out_left,
        (p4_out_left[0] - 50 * SCALE, p4_out_left[1]),
        (p4_out_left[0] - 50 * SCALE, ret_y),
        (user_bot_c[0], ret_y),
        user_bot_c
    ], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw.text((320 * SCALE, ret_y - 28 * SCALE), "Transcribed Text, Trilingual Translation & Vector PDF Report", fill=(0, 0, 0), font=arrow_font)

    final_img = img.resize((1650, 1000), Image.Resampling.LANCZOS)
    
    p1 = os.path.expanduser(r"~\Downloads\dfd_level_1.png")
    p2 = os.path.abspath("dfd_level_1.png")
    p3 = r"C:\Users\HP\.gemini\antigravity\brain\eea0873d-fb47-4568-adb1-9f3b449c3539\dfd_level_1.png"
    paper_p = os.path.abspath(os.path.join("paper_figures", "dfd_level_1.png"))

    final_img.save(p1, dpi=(300, 300))
    final_img.save(p2, dpi=(300, 300))
    if os.path.exists("paper_figures"): final_img.save(paper_p, dpi=(300, 300))
    try: final_img.save(p3, dpi=(300, 300))
    except Exception: pass
    print(f"[OK] B&W DFD Level 1 saved to {p1}")

# =================================================================
# 3. DFD LEVEL 2 (Detailed Sub-Process Decomposition - Pure Black & White)
# =================================================================
def generate_dfd_level_2():
    SCALE = 2
    W = 1800 * SCALE
    H = 1100 * SCALE

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17 * SCALE)
    font_reg = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13 * SCALE)
    font_num = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18 * SCALE)
    arrow_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14 * SCALE)
    arrow_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 11 * SCALE)

    # Title
    title_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26 * SCALE)
    draw.text((60 * SCALE, 35 * SCALE), "DFD Level 2: Detailed Process Decomposition", fill=(0, 0, 0), font=title_font)

    # USER Box (Left)
    user_box = [50 * SCALE, 500 * SCALE, 220 * SCALE, 610 * SCALE]
    draw_entity_box(draw, user_box, "USER", "Manuscript", font_bold, font_reg, width=3 * SCALE)

    # --- ROW 1: Preprocessing Sub-Processes ---
    p11_c = (420 * SCALE, 220 * SCALE); r11 = 95 * SCALE
    draw_dfd_process_bw(draw, p11_c, r11, "1.1", [("FANI 2.0", True), ("Inpainting", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    p12_c = (760 * SCALE, 220 * SCALE); r12 = 95 * SCALE
    draw_dfd_process_bw(draw, p12_c, r12, "1.2", [("Adaptive Sauvola", True), ("Binarization", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    p13_c = (1100 * SCALE, 220 * SCALE); r13 = 95 * SCALE
    draw_dfd_process_bw(draw, p13_c, r13, "1.3", [("Multi-Row Glyph", True), ("Segmentation", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    # --- ROW 2: Recognition Sub-Processes ---
    p21_c = (480 * SCALE, 550 * SCALE); r21 = 95 * SCALE
    draw_dfd_process_bw(draw, p21_c, r21, "2.1", [("Betti Topology", True), ("Filtration (B0,B1)", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    p22_c = (820 * SCALE, 550 * SCALE); r22 = 95 * SCALE
    draw_dfd_process_bw(draw, p22_c, r22, "2.2", [("TrOCR Vision", True), ("Transformer", True)], font_num, font_reg, font_bold, width=3 * SCALE)

    p23_c = (1160 * SCALE, 550 * SCALE); r23 = 95 * SCALE
    draw_dfd_process_bw(draw, p23_c, r23, "2.3", [("5-Model ML & CNN", True), ("Decision Space", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    # Data Store D2: Model Checkpoints (Right of 2.3)
    d2_box = [1440 * SCALE, 520 * SCALE, 1740 * SCALE, 580 * SCALE]
    draw_data_store_bw(draw, d2_box, "D2", "TrOCR / SVM Checkpoints", font_num, font_reg, width=3 * SCALE)

    # --- ROW 3: Post-Processing Sub-Processes ---
    p31_c = (480 * SCALE, 870 * SCALE); r31 = 95 * SCALE
    draw_dfd_process_bw(draw, p31_c, r31, "3.1", [("Sandhi Trie & DP", True), ("Levenshtein", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    p32_c = (820 * SCALE, 870 * SCALE); r32 = 95 * SCALE
    draw_dfd_process_bw(draw, p32_c, r32, "3.2", [("Trilingual Semantic", True), ("Translation", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    p33_c = (1160 * SCALE, 870 * SCALE); r33 = 95 * SCALE
    draw_dfd_process_bw(draw, p33_c, r33, "3.3", [("Vector PDF & GUI", True), ("Report Generator", False)], font_num, font_reg, font_bold, width=3 * SCALE)

    # Data Store D1: Sandhi Trie Lexicon (Right of 3.3)
    d1_box = [1440 * SCALE, 840 * SCALE, 1740 * SCALE, 900 * SCALE]
    draw_data_store_bw(draw, d1_box, "D1", "Malayalam Dictionary Trie", font_num, font_reg, width=3 * SCALE)

    # --- Precise Connecting Arrows ---
    # USER -> 1.1
    user_top_c = ((user_box[0] + user_box[2]) // 2, user_box[1])
    p11_in_left = circle_boundary_at_y(p11_c, r11, p11_c[1], side='left')
    draw_arrow(draw, [user_top_c, (user_top_c[0], p11_c[1]), p11_in_left], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((user_top_c[0] + 10 * SCALE, p11_c[1] - 25 * SCALE), "Raw Scan", fill=(0, 0, 0), font=arrow_font)

    # 1.1 -> 1.2
    p11_out_r = circle_boundary_at_y(p11_c, r11, p11_c[1], side='right')
    p12_in_l = circle_boundary_at_y(p12_c, r12, p12_c[1], side='left')
    draw_arrow(draw, [p11_out_r, p12_in_l], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p11_out_r[0] + 35 * SCALE, p11_c[1] - 22 * SCALE), "Denoised", fill=(0, 0, 0), font=arrow_sub)

    # 1.2 -> 1.3
    p12_out_r = circle_boundary_at_y(p12_c, r12, p12_c[1], side='right')
    p13_in_l = circle_boundary_at_y(p13_c, r13, p13_c[1], side='left')
    draw_arrow(draw, [p12_out_r, p13_in_l], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p12_out_r[0] + 35 * SCALE, p12_c[1] - 22 * SCALE), "Binarized", fill=(0, 0, 0), font=arrow_sub)

    # 1.3 -> 2.1 (Glyph cuts)
    p13_out_bot1 = circle_boundary_at_x(p13_c, r13, p13_c[0] - 40 * SCALE, side='bottom')
    p21_in_top = circle_boundary_at_x(p21_c, r21, p21_c[0], side='top')
    draw_arrow(draw, [
        p13_out_bot1,
        (p13_out_bot1[0], 380 * SCALE),
        (p21_c[0], 380 * SCALE),
        p21_in_top
    ], (0, 0, 0), 2 * SCALE, 14 * SCALE)
    draw.text((p21_c[0] + 15 * SCALE, 390 * SCALE), "Glyph Cuts", fill=(0, 0, 0), font=arrow_sub)

    # 1.3 -> 2.2 (Word strips)
    p13_out_bot2 = circle_boundary_at_x(p13_c, r13, p13_c[0] + 10 * SCALE, side='bottom')
    p22_in_top = circle_boundary_at_x(p22_c, r22, p22_c[0], side='top')
    draw_arrow(draw, [
        p13_out_bot2,
        (p13_out_bot2[0], 430 * SCALE),
        (p22_c[0], 430 * SCALE),
        p22_in_top
    ], (0, 0, 0), 2 * SCALE, 14 * SCALE)
    draw.text((p22_c[0] + 15 * SCALE, 440 * SCALE), "Word Strips", fill=(0, 0, 0), font=arrow_sub)

    # 2.1 -> 2.2 (Betti to TrOCR fusion)
    p21_out_r = circle_boundary_at_y(p21_c, r21, p21_c[1], side='right')
    p22_in_l = circle_boundary_at_y(p22_c, r22, p22_c[1], side='left')
    draw_arrow(draw, [p21_out_r, p22_in_l], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p21_out_r[0] + 20 * SCALE, p21_c[1] - 22 * SCALE), "Betti Vectors", fill=(0, 0, 0), font=arrow_sub)

    # 2.2 -> 2.3 (Attention tokens to ML decision)
    p22_out_r = circle_boundary_at_y(p22_c, r22, p22_c[1], side='right')
    p23_in_l = circle_boundary_at_y(p23_c, r23, p23_c[1], side='left')
    draw_arrow(draw, [p22_out_r, p23_in_l], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p22_out_r[0] + 15 * SCALE, p22_c[1] - 22 * SCALE), "Attention Tokens", fill=(0, 0, 0), font=arrow_sub)

    # D2 -> 2.3 (Model weights into 2.3 right edge)
    p23_in_r = circle_boundary_at_y(p23_c, r23, d2_box[1] + 30 * SCALE, side='right')
    draw_arrow(draw, [(d2_box[0], d2_box[1] + 30 * SCALE), p23_in_r], (0, 0, 0), 2 * SCALE, 12 * SCALE)

    # 2.3 -> 3.1 (Characters down to Sandhi)
    p23_out_bot = circle_boundary_at_x(p23_c, r23, p23_c[0], side='bottom')
    p31_in_top = circle_boundary_at_x(p31_c, r31, p31_c[0], side='top')
    draw_arrow(draw, [
        p23_out_bot,
        (p23_c[0], 710 * SCALE),
        (p31_c[0], 710 * SCALE),
        p31_in_top
    ], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p31_c[0] + 60 * SCALE, 720 * SCALE), "Raw Character Sequences & Probabilities", fill=(0, 0, 0), font=arrow_font)

    # 3.1 -> 3.2 (Corrected text to translation)
    p31_out_r = circle_boundary_at_y(p31_c, r31, p31_c[1], side='right')
    p32_in_l = circle_boundary_at_y(p32_c, r32, p32_c[1], side='left')
    draw_arrow(draw, [p31_out_r, p32_in_l], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p31_out_r[0] + 15 * SCALE, p31_c[1] - 22 * SCALE), "Corrected Malayalam", fill=(0, 0, 0), font=arrow_sub)

    # 3.2 -> 3.3 (Translation to Report)
    p32_out_r = circle_boundary_at_y(p32_c, r32, p32_c[1], side='right')
    p33_in_l = circle_boundary_at_y(p33_c, r33, p33_c[1], side='left')
    draw_arrow(draw, [p32_out_r, p33_in_l], (0, 0, 0), 3 * SCALE, 14 * SCALE)
    draw.text((p32_out_r[0] + 20 * SCALE, p32_c[1] - 22 * SCALE), "Trilingual Text", fill=(0, 0, 0), font=arrow_sub)

    # D1 -> 3.1 (Dictionary into Sandhi Trie)
    p31_in_bot = circle_boundary_at_x(p31_c, r31, p31_c[0] + 40 * SCALE, side='bottom')
    draw_arrow(draw, [
        (d1_box[0], d1_box[1] + 30 * SCALE),
        (1340 * SCALE, d1_box[1] + 30 * SCALE),
        (1340 * SCALE, 990 * SCALE),
        (p31_c[0] + 40 * SCALE, 990 * SCALE),
        p31_in_bot
    ], (0, 0, 0), 2 * SCALE, 12 * SCALE)
    draw.text((1350 * SCALE, 960 * SCALE), "Sandhi Rules", fill=(0, 0, 0), font=arrow_sub)

    # 3.3 -> USER (Return Flow)
    p33_out_bot = circle_boundary_at_x(p33_c, r33, p33_c[0], side='bottom')
    ret_y = 1040 * SCALE
    user_bot_c = ((user_box[0] + user_box[2]) // 2, user_box[3])
    draw_arrow(draw, [
        p33_out_bot,
        (p33_c[0], ret_y),
        (user_bot_c[0], ret_y),
        user_bot_c
    ], (0, 0, 0), 3 * SCALE, 16 * SCALE)
    draw.text((320 * SCALE, ret_y - 28 * SCALE), "Final Transcriptions, Trilingual Translations & Vector PDF Evaluation Report", fill=(0, 0, 0), font=arrow_font)

    final_img = img.resize((1800, 1100), Image.Resampling.LANCZOS)
    
    p1 = os.path.expanduser(r"~\Downloads\dfd_level_2.png")
    p2 = os.path.abspath("dfd_level_2.png")
    p3 = r"C:\Users\HP\.gemini\antigravity\brain\eea0873d-fb47-4568-adb1-9f3b449c3539\dfd_level_2.png"
    paper_p = os.path.abspath(os.path.join("paper_figures", "dfd_level_2.png"))

    final_img.save(p1, dpi=(300, 300))
    final_img.save(p2, dpi=(300, 300))
    if os.path.exists("paper_figures"): final_img.save(paper_p, dpi=(300, 300))
    try: final_img.save(p3, dpi=(300, 300))
    except Exception: pass
    print(f"[OK] B&W DFD Level 2 saved to {p1}")

def main():
    print("Generating Academic B&W DFD Diagrams for EpigraphiX-AI...")
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_dfd_level_2()
    print("All B&W DFD Diagrams successfully overwritten in Downloads!")

if __name__ == "__main__":
    main()
