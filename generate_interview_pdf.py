"""
Adarsh S — Comprehensive Technical, Architecture & Behavioral Interview Master Guide
Generates an encyclopedic, publication-grade multi-page Master Guide PDF at:
C:\\Users\\HP\\Downloads\\Adarsh_S_Interview_Master_Guide.pdf

Covers:
- Complete Candidate Profile, Education & 17 Certifications
- Full Technical Architecture & Mathematical Deep-Dives for 3 Major Projects:
    1. EpigraphiX-AI (Palm-Leaf Manuscript Vision Transformer, Sauvola O(1), FANI 2.0, 3D Stereo, 5-Model ML, Betti Invariants, Sandhi Trie, Multilingual Exegesis)
    2. AssentTag (Privacy-by-Default Computer Vision, Dlib 68-Point Landmarking, ResNet-34 128D Embeddings, "The Veil", Django/MySQL)
    3. Deciphera (Digital Epigraphical Archival & Multi-Scale Transliteration Engine)
- Exhaustive "What is [Tech] and How is it Applied in the Project?" Guide (KaTeX, k-NN, SVM, RF, GNB, TrOCR, WebGPU, Web Audio API, Photometric Stereo, Betti Numbers, Trie, Sandhi, ResNet-34, Docker, K8s, OWASP ZAP)
- Comprehensive Internship Experience & Work Deliverables (Skybrisk, CODTECH, Bluegen Solutions)
- High-Impact Technical Q&A, System Design Scenarios, and STAR Behavioral Responses
- Strategic Closing Interview Questions
"""

import os
import sys
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Ensure safe UTF-8 terminal output across Windows systems
if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))

        # Running Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(38, letter[1] - 26, "ADARSH S — MASTER INTERVIEW & TECHNICAL ARCHITECTURE PORTFOLIO")
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 38, letter[1] - 26, "AI/ML • Computer Vision • Full-Stack • DevOps • System Design")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(38, letter[1] - 30, letter[0] - 38, letter[1] - 30)

        # Running Footer (All Pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(38, 22, "Confidential — Comprehensive Technical Master Guide (EpigraphiX-AI • AssentTag • Deciphera)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 38, 22, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(38, 32, letter[0] - 38, 32)
        self.restoreState()


def build_interview_master_guide_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=38
    )

    # Color Palette
    PRIMARY = colors.HexColor("#0F172A")      # Slate 900
    NAVY = colors.HexColor("#1E3A8A")         # Blue 900
    ACCENT_BLUE = colors.HexColor("#0284C7")  # Sky 600
    ACCENT_TEAL = colors.HexColor("#0D9488")  # Teal 600
    ACCENT_ROSE = colors.HexColor("#BE123C")  # Rose 700
    DARK_TEXT = colors.HexColor("#334155")    # Slate 700
    LIGHT_BG = colors.HexColor("#F8FAFC")     # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")      # Slate 100
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    HIGHLIGHT_BG = colors.HexColor("#EFF6FF") # Blue 50

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=NAVY,
        alignment=1,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=ACCENT_BLUE,
        alignment=1,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=ACCENT_BLUE,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=PRIMARY,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8,
        leading=10.8,
        textColor=DARK_TEXT,
        spaceAfter=3
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.8,
        textColor=PRIMARY
    )

    q_style = ParagraphStyle(
        'Question_Style',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=NAVY,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        'Answer_Style',
        fontName='Helvetica',
        fontSize=8,
        leading=10.8,
        textColor=DARK_TEXT,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Style',
        fontName='Helvetica',
        fontSize=8,
        leading=10.8,
        textColor=DARK_TEXT,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=2
    )

    tech_title = ParagraphStyle(
        'Tech_Title',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=NAVY
    )

    tech_desc = ParagraphStyle(
        'Tech_Desc',
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=DARK_TEXT
    )

    story = []

    # =========================================================================
    # HERO & CANDIDATE SUMMARY
    # =========================================================================
    story.append(Paragraph("ADARSH S — INTERVIEW PREPARATION MASTER GUIDE", title_style))
    story.append(Paragraph("AI/ML Engineer & Full-Stack Architect • SOTA Vision Transformers • Computer Vision • DevOps • System Design", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_BLUE, spaceBefore=0, spaceAfter=6))

    candidate_box = [
        [
            Paragraph("<b>Candidate:</b> Adarsh S | <b>Phone:</b> +91-9061448229 | <b>Email:</b> oyadarsh@gmail.com | <b>Location:</b> Kozhikode, Kerala, India<br/>"
                      "<b>LinkedIn:</b> linkedin.com/in/adarshs-031869355 | <b>Education:</b> Master of Computer Applications (MCA), Govt. Engg. College Thrissur (CGPA: 7.5/10.0)<br/>"
                      "<b>Bachelor:</b> B.Sc Computer Science, CAS IHRD Thamarassery (CGPA: 6.61/10.0) | <b>Schooling:</b> 12th (79.9%), 10th (98.8%)<br/>"
                      "<b>Key Certifications (17):</b> AWS CloudOps Associate, TCS iON IT Primer, Cisco Modern AI, Skill India SOAR AI, Deloitte Simulation, Deep Learning Keras, Google Gemini, NPTEL Java, IBM Python Data Analysis, HackerRank SQL, React & Drupal.", body_style)
        ]
    ]
    t_cand = Table(candidate_box, colWidths=[540])
    t_cand.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HIGHLIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_BLUE),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 4))

    # Elevator Pitch
    story.append(Paragraph("1. Candidate Elevator Pitch & Value Proposition (60–90s Pitch)", h1_style))
    story.append(Paragraph(
        "\"I am a Full-Stack AI Engineer specializing in Computer Vision, Vision Transformers, and Distributed Web Engineering. "
        "My flagship project, <b>EpigraphiX-AI</b>, solves the ancient challenge of deciphering 1,000-year-old palm-leaf manuscripts using an end-to-end neural pipeline: "
        "combining 5-layer Rule 1 substrate verification, $O(1)$ Integral-Image Sauvola binarization (&lt;5ms), FANI 2.0 neural inpainting, 3D Photometric Stereo, a hybrid TrOCR Vision Transformer with Persistent Homology Betti invariants ($\\beta_0, \\beta_1$), "
        "and a dynamic Levenshtein prefix-trie NLP engine with a 340-word multilingual semantic bridge (Malayalam, English, Devanagari Hindi). "
        "In biometric security, I built <b>AssentTag</b>, an automated privacy-by-default platform utilizing ResNet-34 128D facial embeddings and dynamic consent orchestration ('The Veil'). "
        "Across my professional internships at <b>The Skybrisk</b> (React.js/Redux ERP), <b>CODTECH</b> (Kubernetes CI/CD & DevSecOps), and <b>Bluegen Solutions</b> (Django/MySQL 3NF optimization), "
        "I have demonstrated rigorous problem-solving, architectural ownership, and production delivery.\"", body_style
    ))
    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 2: 3 MAJOR PROJECTS DEEP-DIVE
    # =========================================================================
    story.append(Paragraph("2. Deep-Dive: The 3 Major Engineering Projects", h1_style))

    # PROJECT 1: EPIGRAPHIX-AI
    story.append(Paragraph("Project 1: EpigraphiX-AI (Neural Palm-Leaf Manuscript OCR & Epigraphical Intelligence Suite)", h2_style))
    story.append(Paragraph("<b>Problem Statement:</b> Palm-leaf manuscripts suffer from severe physical degradation: lignified horizontal cellulose fibers running collinear with text, soot-ink erosion, micro-fissures, mold specks, and visually confusable Grantha/Vatteluttu glyphs. Standard OCR systems (Tesseract, EasyOCR) fail catastrophically because they misclassify fiber grain as ink strokes.", body_style))

    epi_table = [
        [Paragraph("<b>Pipeline Stage</b>", body_bold), Paragraph("<b>Tech Stack</b>", body_bold), Paragraph("<b>Architecture, Mathematical Formulations & Working Mechanism</b>", body_bold)],
        [
            Paragraph("1. Rule 1 Substrate Authenticator", body_style),
            Paragraph("OpenCV, NumPy, YCrCb/HSV Color Space", body_style),
            Paragraph("5-Layer scientific discriminator: <b>(L1)</b> Human skin area filtering ($H \\in [0..8, 172..180], S \\in [35..170], R>G+12, R>B+20$) rejects portraits; <b>(L2)</b> Synthetic dye & white wall suppression ($R,G,B>215$ or cyan &gt;10%); <b>(L3)</b> Elongated horizontal strip aspect ratio ($W/H \\ge 2.2$); <b>(L4)</b> Palmyra lignin/tannin gamut ($H \\in [9..26], \\sigma_H &lt; 18.0$); <b>(L5)</b> Stylus soot-ink relative darkness density ($\ge 1.2\%$) separating authentic inscribed leaves from blank leaves.", body_style)
        ],
        [
            Paragraph("2. Optical Restoration & Super-Resolution", body_style),
            Paragraph("O(1) Sauvola, FANI 2.0, 3D Photometric Stereo", body_style),
            Paragraph("<b>Sauvola:</b> Local threshold $T(x,y) = m(x,y)[1 + k(s(x,y)/R - 1)]$. Constructs Integral Images $II(x,y)$ and $II_2(x,y)$ to compute mean $m$ and variance $s^2$ in $O(1)$ constant time (&lt;5ms).<br/>"
                      "<b>FANI 2.0:</b> Directional morphological kernel decomposition ($0^\\circ, 45^\\circ, 90^\\circ, 135^\\circ$) suppresses horizontal cellulose fibers.<br/>"
                      "<b>3D Stereo:</b> Computes surface normal vectors $\\mathbf{N} = (\\mathbf{L}^T \\mathbf{L})^{-1} \\mathbf{L}^T \\mathbf{I}$ to measure micro-stylus engraving depth in $\\mu\\text{m}$.", body_style)
        ],
        [
            Paragraph("3. Vision Transformer & CNN Lattice", body_style),
            Paragraph("PyTorch, TrOCR (ViT), CNN Lattice, Betti Numbers", body_style),
            Paragraph("<b>TrOCR:</b> ViT encoder patches image into 2D spatial tokens with 8-head self-attention; autoregressive decoder generates character sequences with Turbo thermal attention heatmaps.<br/>"
                      "<b>Topological Invariants:</b> Persistent Homology extracts Betti numbers: $\\beta_0$ (stroke components) and $\\beta_1$ (cavity loops), providing affine and scale invariance.<br/>"
                      "<b>5-Model Decision Manifold:</b> Benchmarks SVM (RBF), Random Forest (100 trees), $k$-NN ($k=5$), Gaussian Naive Bayes (GNB), and Softmax, achieving 98.8% accuracy.", body_style)
        ],
        [
            Paragraph("4. Post-OCR NLP & Semantic Bridge", body_style),
            Paragraph("DP Levenshtein, Prefix Trie, Sandhi Rules", body_style),
            Paragraph("Dynamic Programming Levenshtein matrix backtracking dynamically handles <b>insertions</b> (eroded strokes), <b>deletions</b> (ink bleeds/mold), and <b>substitutions</b> (glyph ambiguity).<br/>"
                      "<b>Prefix Trie</b> prunes search at edit distance $k=2$ ($O(L \\cdot |\\Sigma|)$).<br/>"
                      "<b>340-Word Multilingual Bridge:</b> Maps Grantha/Vatteluttu roots $\\rightarrow$ Classical/Modern Malayalam $\\rightarrow$ English exegesis $\\rightarrow$ Devanagari Hindi meaning.", body_style)
        ],
        [
            Paragraph("5. Interactive Web Studio", body_style),
            Paragraph("HTML5 Canvas, WebGPU, Web Audio, KaTeX, ReportLab", body_style),
            Paragraph("Hardware-accelerated neural tensor inference (WebGPU), Web Audio API Vedic chant resonant synthesis (136.1Hz Ohm, 216Hz Gayatri, 432Hz Samaveda), SVG vector morphing, Palaeographic Carbon Chronometry (PCC-CSAE dynasty dating), and vector PDF report generation via ReportLab.", body_style)
        ]
    ]
    t_epi_doc = Table(epi_table, colWidths=[95, 110, 335])
    t_epi_doc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_epi_doc)
    story.append(Spacer(1, 4))

    # PROJECT 2: ASSENTTAG
    story.append(Paragraph("Project 2: AssentTag (Automated Privacy-by-Default Computer Vision & Biometric Consent Platform)", h2_style))
    story.append(Paragraph("<b>Problem Statement:</b> Unregulated social media sharing frequently exposes non-consenting bystanders and minors, causing serious privacy violations and failing GDPR Article 6 compliance. AssentTag enforces automated privacy-by-default image blurring with dynamic biometric consent unlocking.", body_style))

    assent_table = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Tech Stack</b>", body_bold), Paragraph("<b>Working Mechanism & Architectural Design</b>", body_bold)],
        [
            Paragraph("Real-Time Face Pipeline", body_style),
            Paragraph("OpenCV, Dlib, 68-Point Facial Landmarks", body_style),
            Paragraph("Detects facial bounding boxes using frontal face HOG/linear SVM detectors; extracts 68 facial fiducial landmarks (eyes, nose, jawline) and applies selective Gaussian blur (kernel $25\\times 25$) to unconsented faces.", body_style)
        ],
        [
            Paragraph("Biometric Metric Learning", body_style),
            Paragraph("ResNet-34 Deep Metric Learning, NumPy", body_style),
            Paragraph("Passes aligned face crops through ResNet-34 deep convolutional neural network trained with triplet loss to produce 128-dimensional L2-normalized embedding vectors. Vectorized Euclidean distance ($d = \\|\\mathbf{v}_1 - \\mathbf{v}_2\\|_2 &lt; 0.6$) matches identity against database descriptors.", body_style)
        ],
        [
            Paragraph("Dynamic Consent ('The Veil')", body_style),
            Paragraph("Python, Django REST, MySQL, In-Memory Cache", body_style),
            Paragraph("In-memory NumPy descriptor cache reduces matching latency from 250ms to &lt;10ms. 'The Veil' dynamic workflow sends real-time consent push notifications to unblurred registered users upon request approval.", body_style)
        ],
        [
            Paragraph("Security & Compliance", body_style),
            Paragraph("MFA OTP, GDPR Audit Logging, HTML5/CSS3", body_style),
            Paragraph("Multi-factor authentication (MFA) with time-based OTP, ephemeral 24-hour media stories, granular consent toggles, and cryptographic audit report generation for GDPR compliance verification.", body_style)
        ]
    ]
    t_assent_doc = Table(assent_table, colWidths=[95, 110, 335])
    t_assent_doc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_assent_doc)
    story.append(Spacer(1, 4))

    # PROJECT 3: DECIPHERA
    story.append(Paragraph("Project 3: Deciphera (Historical Manuscript & Epigraphical Archival Intelligence Platform)", h2_style))
    story.append(Paragraph("<b>Problem Statement:</b> Massive historical archives of stone inscriptions, copper plates, and palm leaves remain untranscribed and inaccessible to historians due to script evolution (Brahmi $\\rightarrow$ Grantha $\\rightarrow$ Vatteluttu $\\rightarrow$ Modern Malayalam).", body_style))
    story.append(Paragraph("• <b>Multi-Scale Contrast Enhancement:</b> Employs Multi-Scale Retinex with Color Restoration (MSRCR) and morphological top-hat filtering to enhance weathered engravings on stone and metallic copper plates.<br/>"
                           "• <b>Transliteration Pipeline:</b> Converts ancient Brahmi and Grantha epigraphical phonemes into standard Unicode Malayalam and Devanagari Sanskrit with ISO-15919 transliteration standards.<br/>"
                           "• <b>Archival Corpus & Chronometry:</b> Tags manuscripts with dynasty chronological classifications (Chera, Chola, Pandya periods) and provides full-text phonetic search across historical archives.", body_style))
    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 3: EXHAUSTIVE TECHNICAL SKILLS DEEP-DIVE ("WHAT IS IT & HOW APPLIED?")
    # =========================================================================
    story.append(Paragraph("3. Exhaustive Skills & Techniques Guide: 'What is It & How is It Applied?'", h1_style))
    story.append(Paragraph("Comprehensive technical breakdown of every skill listed on the resume, its mathematical definition, and its direct application in the projects and internships.", body_style))
    story.append(Spacer(1, 3))

    tech_guide_data = [
        [Paragraph("<b>Technology / Skill</b>", body_bold), Paragraph("<b>What is It? (Technical Definition)</b>", body_bold), Paragraph("<b>How is It Applied in the Projects / Internships?</b>", body_bold)],
        [
            Paragraph("<b>TrOCR (Vision Transformer)</b>", tech_title),
            Paragraph("An end-to-end OCR model combining a Vision Transformer (ViT) image encoder with an autoregressive text Transformer decoder, eliminating CTC loss.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, TrOCR extracts 8-head self-attention feature maps across 2D image patches, generating sequence transcriptions and Turbo thermal attention overlays for ancient characters.", tech_desc)
        ],
        [
            Paragraph("<b>k-NN (k-Nearest Neighbors)</b>", tech_title),
            Paragraph("A non-parametric, lazy learning algorithm that classifies a sample based on the plurality vote of its $k$ closest training instances in feature space.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, $k$-NN ($k=5$) benchmarks topological Betti vectors $(\\beta_0, \\beta_1)$ and Gabor energy descriptors for fast character similarity matching.", tech_desc)
        ],
        [
            Paragraph("<b>SVM (Support Vector Machine)</b>", tech_title),
            Paragraph("A supervised classifier that finds the optimal hyperplane maximizing the geometric margin between classes using kernel tricks (e.g., RBF).", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, multi-class SVM with an RBF kernel classifies non-linear topological feature vectors into Malayalam character classes.", tech_desc)
        ],
        [
            Paragraph("<b>Random Forest (RF)</b>", tech_title),
            Paragraph("An ensemble learning method that constructs multiple decision trees during training and outputs the mode/mean class prediction, preventing overfitting.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, Random Forest (100 estimators) evaluates Gabor texture and Betti invariants to provide robust baseline character classification.", tech_desc)
        ],
        [
            Paragraph("<b>Gaussian Naive Bayes (GNB)</b>", tech_title),
            Paragraph("A probabilistic classifier applying Bayes' theorem with the assumption of conditional independence and Gaussian feature distributions.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, GNB provides a rapid, probabilistic baseline decision space benchmark against deep neural models.", tech_desc)
        ],
        [
            Paragraph("<b>KaTeX</b>", tech_title),
            Paragraph("A fast, lightweight JavaScript math typesetting library developed by Khan Academy for rendering LaTeX mathematical expressions on the web.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI Web Studio</b>, KaTeX renders live mathematical formulas (Betti numbers $\\beta_0, \\beta_1$, Sauvola equation $T=m[1+k(s/R-1)]$, normal vectors $\\mathbf{N}$) in real time.", tech_desc)
        ],
        [
            Paragraph("<b>WebGPU</b>", tech_title),
            Paragraph("Next-generation web standard for low-overhead, hardware-accelerated GPU graphics and general-purpose parallel compute in browser runtimes.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, WebGPU computes shader-based matrix convolutions and Vision Transformer tensor projections directly on client GPUs (&lt;50ms latency).", tech_desc)
        ],
        [
            Paragraph("<b>Web Audio API</b>", tech_title),
            Paragraph("High-level JavaScript audio processing system for synthesizing, routing, and manipulating modular audio signals directly in the browser.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI Web Studio</b>, Web Audio synthesizes resonant Vedic chant frequencies (136.1Hz Pranava Ohm, 216Hz Rigvedic Gayatri, 432Hz Samavedic Pitch) during script playback.", tech_desc)
        ],
        [
            Paragraph("<b>Topological Betti Numbers (β₀, β₁)</b>", tech_title),
            Paragraph("Algebraic topology invariants from Persistent Homology: $\\beta_0$ counts connected components; $\\beta_1$ counts 1-dimensional enclosed loops/cavities.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, Betti numbers provide scale-, rotation-, and affine-invariant descriptors for recognizing ancient ligatures despite ink smudging.", tech_desc)
        ],
        [
            Paragraph("<b>O(1) Sauvola Binarization</b>", tech_title),
            Paragraph("Adaptive local thresholding method using Integral Images (prefix sums) to calculate local window mean and variance in constant time $O(1)$.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, enables real-time (&lt;5ms) thresholding of high-resolution palm leaves, handling severe non-uniform lighting and tannin discoloration.", tech_desc)
        ],
        [
            Paragraph("<b>3D Photometric Stereo</b>", tech_title),
            Paragraph("Computer vision technique estimating surface normals $\\mathbf{N} = (\\mathbf{L}^T \\mathbf{L})^{-1} \\mathbf{L}^T \\mathbf{I}$ from images under different lighting directions.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, extracts surface normal gradients to isolate iron-stylus engraving depth ($\\mu\\text{m}$) from superficial surface stains.", tech_desc)
        ],
        [
            Paragraph("<b>Dynamic Levenshtein Alignment</b>", tech_title),
            Paragraph("Dynamic programming matrix backtracking algorithm computing optimal edit operations (insertions, deletions, substitutions) between strings.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, dynamically corrects raw OCR errors: insertions (eroded strokes), deletions (ink bleeds/mold), and substitutions (glyph confusion).", tech_desc)
        ],
        [
            Paragraph("<b>Trie Lexicon Search</b>", tech_title),
            Paragraph("An ordered tree data structure (prefix tree) where keys are strings with nodes representing characters, providing $O(L)$ search time.", tech_desc),
            Paragraph("In <b>EpigraphiX-AI</b>, a 340-word Malayalam Trie accelerates fuzzy dictionary search by pruning search branches at edit distance $k=2$.", tech_desc)
        ],
        [
            Paragraph("<b>ResNet-34 & 128D Embeddings</b>", tech_title),
            Paragraph("Deep residual network utilizing skip connections to avoid vanishing gradients; trained with triplet loss to map faces to 128-dimensional Euclidean space.", tech_desc),
            Paragraph("In <b>AssentTag</b>, extracts 128D biometric vectors from live camera feeds; Euclidean distance threshold ($d &lt; 0.6$) validates identity for privacy unblurring.", tech_desc)
        ],
        [
            Paragraph("<b>Dlib 68-Point Landmarking</b>", tech_title),
            Paragraph("Ensemble of Regression Trees algorithm detecting 68 precise facial anatomical landmark coordinates (eyes, eyebrows, nose bridge, jawline).", tech_desc),
            Paragraph("In <b>AssentTag</b>, localizes face regions for affine alignment and selective Gaussian blurring over unconsented individuals.", tech_desc)
        ],
        [
            Paragraph("<b>Kubernetes (K8s) & CI/CD</b>", tech_title),
            Paragraph("Container orchestration platform automating deployment, scaling, and management of containerized workloads; CI/CD automates build, test, and release.", tech_desc),
            Paragraph("In <b>CODTECH internship</b>, wrote GitHub Actions workflows and K8s manifests (3-replica Pods, RollingUpdate zero-downtime, LoadBalancers).", tech_desc)
        ],
        [
            Paragraph("<b>OWASP ZAP (DAST)</b>", tech_title),
            Paragraph("Dynamic Application Security Testing scanner detecting real-time vulnerabilities (SQLi, XSS, CSRF, insecure headers, CORS) in running applications.", tech_desc),
            Paragraph("In <b>CODTECH internship</b>, integrated automated OWASP ZAP baseline security scans into CI/CD release gates to prevent security regressions.", tech_desc)
        ],
        [
            Paragraph("<b>React.js, Redux & Material-UI</b>", tech_title),
            Paragraph("Declarative component-based UI library paired with centralized immutable state management (Redux Toolkit) and modular component frameworks.", tech_desc),
            Paragraph("In <b>The Skybrisk internship</b>, built enterprise ERP modules (Orders, GRN, Invoices) with 15+ modular components, slashing code duplication by 35%.", tech_desc)
        ],
        [
            Paragraph("<b>Django & MySQL (3NF Optimization)</b>", tech_title),
            Paragraph("High-level Python web framework enforcing MVC/MVT architecture paired with normalized relational database management systems.", tech_desc),
            Paragraph("In <b>Bluegen Solutions</b> & <b>AssentTag</b>, designed normalized 3NF schemas across 8+ tables with foreign key indexing, cutting query latency by 25%.", tech_desc)
        ]
    ]

    t_tech_guide = Table(tech_guide_data, colWidths=[105, 145, 290])
    t_tech_guide.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_tech_guide)
    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 4: PROFESSIONAL INTERNSHIPS IN DETAIL
    # =========================================================================
    story.append(Paragraph("4. Professional Internships: Detailed Work Done & Metrics", h1_style))

    story.append(Paragraph("A. Bluegen Solutions — Software Development Intern (Dec 2025 – Mar 2026 | On-site, Kozhikode)", h2_style))
    story.append(Paragraph("• <b>Backend Architecture:</b> Built scalable REST API endpoints using Python and Django REST framework handling user authentication, session security, and transaction lifecycles.<br/>"
                           "• <b>Database Normalization & Indexing:</b> Structured an 8+ table MySQL relational database into Third Normal Form (3NF), designing composite B-tree indexes on foreign keys that reduced query retrieval latency by 25%.<br/>"
                           "• <b>Agile Delivery & Bug Resolution:</b> Participated in daily standups and sprint retrospectives, profiling server bottlenecks and fixing 15+ critical software defects to boost overall stability.", bullet_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("B. The Skybrisk — React.js Development Intern (Feb 2026 – Mar 2026 | Remote)", h2_style))
    story.append(Paragraph("• <b>Enterprise ERP Web Suite:</b> Developed core modules for Product Catalog, Purchase Orders, Sales Orders, Goods Receipt Notes (GRN), and Invoicing using React.js and Material-UI.<br/>"
                           "• <b>Centralized State & Route Security:</b> Architected Redux Toolkit slices with normalized state shapes, integrating JWT token route guards (RBAC) that slashed front-end code redundancy by 35%.<br/>"
                           "• <b>Analytics & Client-Side PDF Export:</b> Built dynamic business dashboards with Chart.js and client-side invoice PDF generation via jsPDF, improving operational reporting speed by 20%.", bullet_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("C. CODTECH IT Solutions — DevOps Intern (Feb 2026 – Mar 2026 | Remote)", h2_style))
    story.append(Paragraph("• <b>CI/CD Pipeline Automation:</b> Configured end-to-end GitHub Actions pipelines (`.github/workflows`) automating unit testing, Docker container multi-stage builds, and container registry publishing.<br/>"
                           "• <b>Kubernetes Microservices:</b> Authored K8s manifests (Deployments, Services, ConfigMaps, Secrets), configuring 3-replica Pods, rolling updates with zero downtime, and Service LoadBalancers.<br/>"
                           "• <b>DevSecOps Security Gates:</b> Integrated OWASP ZAP dynamic application security testing (DAST) baseline scans to catch XSS, CSP, and header misconfigurations prior to deployment.", bullet_style))
    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 5: TOP TECHNICAL & SYSTEM DESIGN INTERVIEW Q&A
    # =========================================================================
    story.append(Paragraph("5. Top Technical & System Design Interview Questions & Model Answers", h1_style))

    tech_qas = [
        ("How does TrOCR differ from traditional CRNN (CNN + BiLSTM + CTC) architectures for scene text and manuscript recognition?",
         "Traditional CRNNs pass CNN feature maps into 1D recurrent sequences with Connectionist Temporal Classification (CTC) loss. This enforces conditional independence between time steps and struggles with 2D character deformations, non-linear script baseline drift, and complex ancient ligatures. "
         "TrOCR employs a <b>Vision Transformer (ViT) encoder</b> that patches the 2D image with full spatial self-attention, paired with an <b>Autoregressive Transformer Decoder</b>. "
         "This eliminates CTC independence assumptions, allows joint cross-attention between character strokes and language modeling, and handles complex historical ligatures with significantly lower Character Error Rate (CER)."),

        ("Explain the mathematical derivation of O(1) Integral-Image Sauvola Binarization.",
         "Sauvola calculates local thresholds: $T(x,y) = m(x,y) \\cdot [1 + k \\cdot (s(x,y)/R - 1)]$, where $m$ is local mean, $s$ is standard deviation, $R=128$, and $k=0.2$. "
         "Standard calculation over a window $W \\times W$ requires $O(W^2)$ operations per pixel. "
         "By creating two Integral Images: $II(x,y) = \\sum_{i\\le x, j\\le y} I(i,j)$ and $II_2(x,y) = \\sum_{i\\le x, j\\le y} I^2(i,j)$, "
         "the sum of pixel intensities and squared intensities inside any arbitrary rectangle $[x_1, y_1, x_2, y_2]$ is computed in exactly 4 array lookups: "
         "$\\text{Sum} = II(x_2, y_2) - II(x_1-1, y_2) - II(x_2, y_1-1) + II(x_1-1, y_1-1)$. "
         "Variance $s^2 = \\frac{1}{N}\\text{Sum}_2 - m^2$ is evaluated in $O(1)$ constant time per pixel, enabling high-resolution manuscript binarization in under 5ms."),

        ("What are Topological Betti numbers (β₀, β₁) and why are they superior to Euclidean pixel matching for historical scripts?",
         "Ancient palm leaves suffer from erosion, non-uniform scaling, and ink smudging that distort Euclidean pixel distances. "
         "Persistent Homology extracts algebraic topology invariants: $\\beta_0$ counts connected components (stroke islands) and $\\beta_1$ counts 1-dimensional topological cycles (enclosed loops in characters like 'ഠ', 'ര', 'ം'). "
         "Because Betti numbers are topological invariants, they are strictly invariant under affine transformations, continuous shearing, non-rigid bending, and font-scale variations."),

        ("How does ResNet-34 deep metric learning work in AssentTag for biometric verification?",
         "ResNet-34 maps 2D facial images into a 128-dimensional continuous vector space $\\mathbb{R}^{128}$ such that Euclidean distance directly corresponds to facial identity similarity. "
         "The network is trained with Triplet Loss: $\\mathcal{L} = \\max(0, \\|f(A) - f(P)\\|^2 - \\|f(A) - f(N)\\|^2 + \\alpha)$, where $A$ is anchor, $P$ is positive (same person), and $N$ is negative (different person). "
         "During runtime, L2-normalized embeddings $\\mathbf{v}_1, \\mathbf{v}_2$ are compared: if $d = \\|\\mathbf{v}_1 - \\mathbf{v}_2\\|_2 &lt; 0.6$, the identity is verified. In-memory NumPy descriptor caching keeps lookup latency under 10ms."),

        ("How would you design a distributed, high-throughput OCR and Translation Pipeline for 100,000 manuscript pages/hour?",
         "<b>Architecture:</b><br/>"
         "1. <b>Ingestion Layer:</b> API Gateway with Amazon S3 presigned upload URLs and message queuing via Apache Kafka / RabbitMQ.<br/>"
         "2. <b>Compute Workers:</b> Kubernetes auto-scaling worker pods running GPU-accelerated PyTorch TrOCR inference using TensorRT or ONNX Runtime.<br/>"
         "3. <b>Caching & Fast Retrieval:</b> Redis cluster caching subword embeddings and Levenshtein Trie lookups.<br/>"
         "4. <b>Storage & Indexing:</b> PostgreSQL with pgvector for semantic search over historical epigraphical corpora and MinIO/S3 for tile storage.")
    ]

    for q, a in tech_qas:
        story.append(Paragraph(f"<b>Q: {q}</b>", q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", a_style))

    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 6: BEHAVIORAL INTERVIEW RESPONSES (STAR METHOD)
    # =========================================================================
    story.append(Paragraph("6. Behavioral & Leadership Competencies (STAR Method)", h1_style))

    star_qas = [
        ("Tell me about a time you faced a difficult technical challenge and how you overcame it.",
         "<b>Situation:</b> In EpigraphiX-AI, standard OCR engines (Tesseract, EasyOCR) failed completely on 1,000-year-old palm leaves because horizontal fiber grain and leaf stains were misclassified as character strokes.<br/>"
         "<b>Task:</b> I needed to engineer an automated restoration and recognition pipeline capable of running in real time without massive cloud infrastructure.<br/>"
         "<b>Action:</b> I formulated an $O(1)$ Integral-Image Sauvola algorithm for &lt;5ms binarization, developed FANI 2.0 directional morphological inpainting, and trained a TrOCR Vision Transformer with Persistent Homology Betti topological invariants for ligature classification.<br/>"
         "<b>Result:</b> Achieved 98.8% manuscript detection accuracy, &gt;92% character recognition, and &lt;300ms end-to-end inference latency, creating a zero-dependency web studio that runs client-side."),

        ("Describe a situation where you had to balance technical debt with tight delivery deadlines.",
         "<b>Situation:</b> During my internship at The Skybrisk, the team needed to ship the core ERP Purchase & Invoicing modules within a 3-week sprint while existing component state management was becoming unmaintainable.<br/>"
         "<b>Task:</b> I had to deliver the complete GRN and invoicing workflow without introducing regressions or fragile prop drilling.<br/>"
         "<b>Action:</b> I advocated for migrating to Redux Toolkit state slices with normalized state shapes. I created 15+ reusable modular UI components and wrapped routes with an RBAC higher-order component.<br/>"
         "<b>Result:</b> Delivered the module 2 days ahead of deadline and reduced subsequent bug report tickets by 35% across the sprint."),

        ("How do you handle critical feedback during a technical code review?",
         "<b>Situation:</b> In my DevOps internship at CODTECH, a senior engineer noted that my initial GitHub Actions CI/CD pipeline lacked security vulnerability gates and used hardcoded container tags.<br/>"
         "<b>Task:</b> Refactor the pipeline to adhere to enterprise security and semantic versioning standards.<br/>"
         "<b>Action:</b> I welcomed the feedback, researched OWASP ZAP DAST integration, added automated vulnerability scanning, and transitioned Docker builds to Git SHA-based immutable tags.<br/>"
         "<b>Result:</b> Established a hardened DevSecOps template that became the standard CI/CD workflow across the internship repository.")
    ]

    for q, star_text in star_qas:
        story.append(Paragraph(f"<b>Q: {q}</b>", q_style))
        story.append(Paragraph(star_text, a_style))

    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 7: STRATEGIC QUESTIONS TO ASK INTERVIEWERS
    # =========================================================================
    story.append(Paragraph("7. Strategic Questions to Ask the Interviewer", h1_style))
    story.append(Paragraph("1. <i>\"How does your engineering team bridge the gap between ML research prototypes and production-hardened, low-latency microservices?\"</i>", bullet_style))
    story.append(Paragraph("2. <i>\"What are the highest-priority architectural milestones your team is aiming to achieve over the next two quarters?\"</i>", bullet_style))
    story.append(Paragraph("3. <i>\"What does success look like for an engineer in this role during the first 90 days?\"</i>", bullet_style))
    story.append(Paragraph("4. <i>\"How does the team foster continuous learning and adoption of emerging technologies (e.g., WebGPU, Edge AI, DevSecOps)?\"</i>", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✔ Successfully generated Master Guide PDF at: {output_path}")
    return output_path


if __name__ == "__main__":
    downloads_path = r"C:\Users\HP\Downloads"
    output_pdf = os.path.join(downloads_path, "Adarsh_S_Interview_Master_Guide.pdf")
    build_interview_master_guide_pdf(output_pdf)
