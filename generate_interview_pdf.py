"""
Adarsh S — Comprehensive Technical & Behavioral Interview Master Guide
Generates a publication-grade, multi-page Master PDF guide containing:
- Complete Technical Profiles & Candidate Elevating Summary
- EpigraphiX-AI SOTA Architecture (TrOCR Transformer, FANI 2.0, Betti Invariants, Sandhi Trie, Multilingual Translation)
- AssentTag Biometric Privacy Architecture (128D ResNet Embeddings, The Veil, GDPR)
- Full-Stack, Cloud & DevOps Engineering Internships (Skybrisk, CODTECH, Bluegen)
- In-Depth SOTA Deep Learning, Computer Vision, Algorithms, NLP & System Design Q&A
- Rigorous Behavioral & Leadership Scenarios (STAR Method)
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
        self.setFillColor(colors.HexColor("#475569"))

        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, letter[1] - 28, "ADARSH S — INTERVIEW PREPARATION MASTER GUIDE & TECHNICAL PORTFOLIO")
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 40, letter[1] - 28, "AI/ML • Computer Vision • Full-Stack • DevOps")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(40, letter[1] - 33, letter[0] - 40, letter[1] - 33)

        # Footer (All Pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 24, "Confidential — Prepared for High-Impact Technical, System Design & Leadership Rounds")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 24, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(40, 34, letter[0] - 40, 34)
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Premium Professional Palette
    PRIMARY = colors.HexColor("#0F172A")    # Slate 900
    NAVY = colors.HexColor("#1E3A8A")       # Blue 900
    ACCENT_BLUE = colors.HexColor("#0284C7")# Sky 600
    ACCENT_TEAL = colors.HexColor("#0D9488")# Teal 600
    ACCENT_ROSE = colors.HexColor("#BE123C")# Rose 700
    DARK_TEXT = colors.HexColor("#334155")  # Slate 700
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")    # Slate 100
    BORDER_COLOR = colors.HexColor("#CBD5E1")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY,
        alignment=1,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=ACCENT_BLUE,
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=ACCENT_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT,
        spaceAfter=3
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=PRIMARY
    )

    q_style = ParagraphStyle(
        'Question_Style',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=NAVY,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        'Answer_Style',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Style',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    star_label = ParagraphStyle(
        'STAR_Label',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT,
        leftIndent=10,
        spaceAfter=2
    )

    callout_style = ParagraphStyle(
        'Callout_Style',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=NAVY
    )

    story = []

    # ==========================================
    # HEADER & HERO SECTION
    # ==========================================
    story.append(Paragraph("ADARSH S — INTERVIEW PREPARATION MASTER GUIDE", title_style))
    story.append(Paragraph("AI/ML Engineer & Full-Stack Architect • SOTA Vision Transformers • DevOps • Biometric Privacy", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_BLUE, spaceBefore=0, spaceAfter=8))

    # Executive Overview Box
    exec_summary_data = [
        [
            Paragraph("<b>Target Roles:</b> AI/ML Engineer, Full-Stack Developer, Computer Vision Specialist, DevOps / Cloud Engineer.<br/>"
                      "<b>Core Strengths:</b> Vision Transformers (TrOCR, MH-SAM), $O(1)$ Integral Computer Vision Algorithms, Deep Metric Learning (ResNet-34 128D), Dynamic Programming Levenshtein NLP, MERN & Django Distributed Systems, Kubernetes CI/CD.", body_style)
        ]
    ]
    t_exec = Table(exec_summary_data, colWidths=[534])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 6))

    # ==========================================
    # SECTION 1: ELEVATOR PITCH & VALUE PROPOSITION
    # ==========================================
    story.append(Paragraph("1. Candidate Elevator Pitch & Value Proposition", h1_style))
    story.append(Paragraph(
        "<b>Script (60-90s Delivery):</b><br/>"
        "\"I am a Full-Stack AI Engineer specializing in Computer Vision, Deep Learning, and Distributed Web Platforms. "
        "My flagship project, <b>EpigraphiX-AI</b>, addresses the 1,000-year-old challenge of deciphering degraded palm-leaf manuscripts. "
        "I engineered an $O(1)$ Integral-Image Sauvola restoration pipeline, built a <b>TrOCR Vision Transformer sequence recognition engine</b> with multi-head attention stroke heatmaps, "
        "and formulated an NLP Sandhi prefix-trie corrector reducing Word Error Rate by 15% with real-time Malayalam-English-Hindi semantic translation. "
        "In biometric security, I built <b>AssentTag</b>, a privacy-by-default platform utilizing ResNet-34 128D facial embeddings and dynamic consent orchestration ('The Veil'). "
        "Across my professional internships at <b>The Skybrisk</b> (MERN/Redux ERP), <b>CODTECH</b> (Kubernetes CI/CD), and <b>Bluegen Solutions</b> (Django/MySQL), "
        "I have consistently delivered scalable, secure, and production-tested systems.\"", body_style
    ))
    story.append(Spacer(1, 6))

    # ==========================================
    # SECTION 2: EPIGRAPHIX-AI DEEP-DIVE
    # ==========================================
    story.append(Paragraph("2. Deep-Dive: EpigraphiX-AI (SOTA Palm-Leaf Manuscript Vision & NLP)", h1_style))
    story.append(Paragraph("<b>System Overview:</b> High-performance paleographic transcription and super-resolution engine for ancient Indic/Malayalam palm-leaf manuscripts using Vision Transformers, Betti Topological Invariants, and Trie Lexical decoders.", body_style))
    story.append(Spacer(1, 4))

    epigraphix_table_data = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Technologies Used</b>", body_bold), Paragraph("<b>Engineering Highlights & Mathematical Formulations</b>", body_bold)],
        [
            Paragraph("Restoration & Super-Resolution", body_style),
            Paragraph("OpenCV, FANI 2.0, Sauvola Binarization", body_style),
            Paragraph("Engineered $O(1)$ Integral-Image Sauvola Binarization ($T = m[1 + k(s/R - 1)]$) achieving &lt;5ms latency. FANI 2.0 uses directional morphological kernels (0°, 45°, 90°, 135°) to suppress cellulose grain noise while preserving stylus incisions.", body_style)
        ],
        [
            Paragraph("TrOCR Vision Transformer", body_style),
            Paragraph("PyTorch, ViT Encoder, Transformer Decoder, MH-SAM", body_style),
            Paragraph("Vision Transformer generates multi-head self-attention feature maps across 8 heads. Computes dynamic 5-stop Turbo thermal density overlays, token sequence connection arcs, and character centroid halos.", body_style)
        ],
        [
            Paragraph("Topological Feature Space", body_style),
            Paragraph("Persistent Homology, Betti Numbers ($\\beta_0, \\beta_1$)", body_style),
            Paragraph("Extracts non-Euclidean topological invariants: $\\beta_0$ (connected stroke components) and $\\beta_1$ (cavity loops). Provides scale/rotation invariance for ancient ligature classification.", body_style)
        ],
        [
            Paragraph("NLP Sandhi Decoder & Semantic Bridge", body_style),
            Paragraph("DP Levenshtein Trie, Unicode Phonetics, ISO-15919", body_style),
            Paragraph("Prefix-Trie dynamic programming decodes Sandhi (സന്ധി) splits/merges. Multilingual semantic bridge converts Malayalam terms into Old Classical, Modern, English, and Devanagari Hindi translations.", body_style)
        ],
        [
            Paragraph("Web Studio Client", body_style),
            Paragraph("HTML5 Canvas, ES6+, WebGPU / WASM Ready", body_style),
            Paragraph("Zero-click responsive client-side image processing. Dynamic character crop galleries, live 5-model ML decision space (CNN, SVM, RF, k-NN, GNB), and instant PDF vector reporting.", body_style)
        ]
    ]
    t_epi = Table(epigraphix_table_data, colWidths=[110, 125, 299])
    t_epi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_epi)
    story.append(Spacer(1, 6))

    # ==========================================
    # SECTION 3: ASSENTTAG DEEP-DIVE
    # ==========================================
    story.append(Paragraph("3. Deep-Dive: AssentTag (Biometric Privacy & Consent Management)", h1_style))
    story.append(Paragraph("<b>System Overview:</b> Privacy-by-Default Computer Vision & Biometric Consent platform designed to automatically blur non-consenting individuals in shared media and orchestrate dynamic unblurring (\"The Veil\").", body_style))
    story.append(Spacer(1, 4))

    assenttag_table = [
        [Paragraph("<b>Layer</b>", body_bold), Paragraph("<b>Tech Stack</b>", body_bold), Paragraph("<b>Core Architecture & GDPR Compliance</b>", body_bold)],
        [
            Paragraph("Face Pipeline & Landmarks", body_style),
            Paragraph("OpenCV, Dlib, 68-Point Facial Landmarks", body_style),
            Paragraph("Real-time bounding box extraction and selective Gaussian blurring over unconsented faces while keeping consented users pristine.", body_style)
        ],
        [
            Paragraph("Biometric Metric Learning", body_style),
            Paragraph("ResNet-34 Deep Metric Learning", body_style),
            Paragraph("Extracts 128-dimensional L2-normalized embedding vectors; vectorized Euclidean distance ($d &lt; 0.6$) matches registered identity descriptors.", body_style)
        ],
        [
            Paragraph("Backend & Dynamic Consent", body_style),
            Paragraph("Python, Django, MySQL, In-Memory Caching", body_style),
            Paragraph("In-memory NumPy descriptor cache reduces matching latency from 250ms to &lt;10ms. 'The Veil' dynamic workflow sends push requests to grant real-time unblurring.", body_style)
        ]
    ]
    t_assent = Table(assenttag_table, colWidths=[110, 125, 299])
    t_assent.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_assent)
    story.append(Spacer(1, 6))

    # ==========================================
    # SECTION 4: PROFESSIONAL INTERNSHIP EXPERIENCE
    # ==========================================
    story.append(Paragraph("4. Professional Experience & Industry Internships", h1_style))

    # Skybrisk
    story.append(Paragraph("A. The Skybrisk — React.js Development Intern (Feb 2026 – Mar 2026)", h2_style))
    story.append(Paragraph("• <b>Enterprise ERP Architecture:</b> Built end-to-end workflows for Product Catalog, Purchase/Sales Orders, GRN, and Automated Invoicing.", bullet_style))
    story.append(Paragraph("• <b>State Management & Security:</b> Designed Redux Toolkit slices with signed JWT authentication and granular Role-Based Access Control (Admin, Sales, Purchase, Inventory).", bullet_style))
    story.append(Paragraph("• <b>Analytics & Export:</b> Integrated dynamic Chart.js reporting and client-side jsPDF invoice rendering, accelerating report generation by 20%.", bullet_style))

    # CODTECH
    story.append(Paragraph("B. CODTECH IT Solutions — DevOps Intern (Feb 2026 – Mar 2026)", h2_style))
    story.append(Paragraph("• <b>CI/CD Pipeline Automation:</b> Built automated GitHub Actions workflows (`.github/workflows`) for linting, testing, Docker image building, and multi-stage container push.", bullet_style))
    story.append(Paragraph("• <b>Kubernetes Orchestration:</b> Deployed containerized microservices on K8s with 3 replica pods, RollingUpdate zero-downtime deployments, and LoadBalancer services.", bullet_style))
    story.append(Paragraph("• <b>DevSecOps & DAST:</b> Embedded OWASP ZAP dynamic security scanning into release pipelines to identify CSP, CORS, and header vulnerabilities before production release.", bullet_style))

    # Bluegen
    story.append(Paragraph("C. Bluegen Solutions — Software Development Intern (Dec 2025 – Mar 2026)", h2_style))
    story.append(Paragraph("• <b>RESTful Backend:</b> Engineered scalable Django REST framework endpoints handling user sessions, authentication, and core transaction lifecycles.", bullet_style))
    story.append(Paragraph("• <b>Database Optimization:</b> Normalized MySQL schema across 8+ tables into 3NF with foreign-key composite indexing, cutting query latency by 25%.", bullet_style))

    story.append(Spacer(1, 6))

    # ==========================================
    # SECTION 5: COMPREHENSIVE TECHNICAL INTERVIEW QUESTIONS & MODEL ANSWERS
    # ==========================================
    story.append(Paragraph("5. Comprehensive Technical Q&A (Deep Learning, Vision, NLP, Architecture)", h1_style))

    qa_sections = [
        # CATEGORY A: VISION TRANSFORMERS & DEEP LEARNING
        ("Category A: Vision Transformers & Deep Learning Architecture", [
            ("How does TrOCR differ from traditional CRNN (CNN + BiLSTM + CTC) architectures for scene text and manuscript recognition?",
             "Traditional CRNNs rely on convolutional feature maps fed into 1D recurrent sequences with Connectionist Temporal Classification (CTC) loss. This struggles with 2D character deformations, non-linear text flow, and long-range dependencies in historical scripts. "
             "TrOCR employs a <b>Vision Transformer (ViT) encoder</b> that patches the 2D image into flattened spatial tokens with self-attention across both horizontal and vertical axes, paired with an <b>Autoregressive Transformer Decoder</b>. "
             "This eliminates CTC independence assumptions, allows joint multi-modal cross-attention between character strokes and language modeling, and handles complex historical ligatures with significantly lower character error rate (CER)."),

            ("What is Multi-Head Self-Attention (MH-SAM) and how did you extract stroke attention heatmaps?",
             "Multi-Head Self-Attention computes $A_h = \\text{softmax}(Q_h K_h^T / \\sqrt{d_k}) V_h$ across $H=8$ parallel representation subspaces. "
             "To generate the visual attention heatmap, I extracted cross-attention weights from Layer 12 of the transformer decoder corresponding to active token generation steps. "
             "These weights are projected back onto spatial image coordinates via 2D Gaussian splatting ($\\sigma = 0.85 \\cdot \\text{bbox}$) combined with Sobel incision gradients, and rendered using a 5-stop Turbo thermal gradient (Indigo -> Cyan -> Green -> Amber -> Crimson)."),

            ("What is the vanishing gradient problem and how does ResNet solve it?",
             "In deep networks, gradients backpropagated via the chain rule multiply through many activation derivatives. For sigmoid/tanh or deep weight matrices with eigenvalues &lt; 1, gradients decay exponentially toward zero, preventing early layers from learning. "
             "ResNet introduces <b>residual skip connections</b>: $y = F(x, \\{W_i\\}) + x$. The derivative is $\\frac{\\partial \\mathcal{E}}{\\partial x} = \\frac{\\partial \\mathcal{E}}{\\partial y} \\left(\\frac{\\partial F}{\\partial x} + 1\\right)$. "
             "The constant '$+1$' term guarantees that gradients propagate directly to earlier layers without vanishing, allowing networks with 34, 50, or 152 layers to converge cleanly.")
        ]),

        # CATEGORY B: COMPUTER VISION, RESTORATION & TOPOLOGY
        ("Category B: Computer Vision, Restoration & Topological Analysis", [
            ("Explain the mathematical derivation of O(1) Integral-Image Sauvola Binarization.",
             "Sauvola calculates local thresholds: $T(x,y) = m(x,y) \\cdot [1 + k \\cdot (s(x,y)/R - 1)]$. Standard calculation of local mean $m$ and standard deviation $s = \\sqrt{\\frac{1}{N}\\sum I^2 - m^2}$ over a $W \\times W$ window takes $O(W^2)$ per pixel. "
             "By constructing two Integral Images (prefix sum tables): $II(x,y) = \\sum_{i\\le x, j\\le y} I(i,j)$ and $II_2(x,y) = \\sum_{i\\le x, j\\le y} I^2(i,j)$, "
             "any rectangular sum is computed in 4 array lookups: $\\text{Sum} = II(D) + II(A) - II(B) - II(C)$. This reduces variance computation to $O(1)$ constant time per pixel, enabling real-time manuscript binarization in under 5ms."),

            ("What are Topological Betti numbers (β₀, β₁) and why use them for historical character classification?",
             "Ancient palm leaves suffer from erosion, non-uniform scaling, and ink smudging that distort Euclidean pixel distances. "
             "Persistent Homology extracts algebraic topology invariants: $\\beta_0$ counts connected components (stroke islands) and $\\beta_1$ counts 1-dimensional topological cycles (loops or enclosed holes in characters like 'ഠ', 'ര', 'ം'). "
             "Because Betti numbers are topological invariants, they are strictly invariant under affine transformations, continuous shearing, non-rigid bending, and font-scale variations."),

            ("How does Fiber-Aware Neural Inpainting (FANI 2.0) isolate stylus incisions from cellulose fibers?",
             "Palm leaves feature strong horizontal striations caused by lignified cellulose microfibrils that run collinear with the leaf axis. "
             "FANI 2.0 applies directional morphological kernel decomposition across four discrete angles ($0^\\circ, 45^\\circ, 90^\\circ, 135^\\circ$). "
             "By isolating the $0^\\circ$ sub-band (horizontal cellulose noise) and computing directional local variance, it suppresses fiber striations while preserving curved and vertical stylus ink incisions.")
        ]),

        # CATEGORY C: NLP, SANDHI GRAMMAR & DATA STRUCTURES
        ("Category C: NLP, Sandhi Grammar & Algorithmic Optimization", [
            ("Explain how the Prefix-Trie Levenshtein algorithm performs Sandhi grammar correction.",
             "Raw epigraphical OCR frequently misclassifies visually confusable characters (e.g., 'റ' vs 'ര' or 'പ' vs 'വ'). "
             "Rather than running standard $O(N \\cdot M)$ Levenshtein distance against 50,000 dictionary words ($O(V \\cdot M)$), I constructed a <b>Prefix Trie</b>. "
             "The Dynamic Programming state row is passed down during Trie traversal: $D[i] = \\min(D_{prev}[i]+1, D[i-1]+1, D_{prev}[i-1] + \\text{cost})$. "
             "Branches with edit distance exceeding $k=2$ are pruned early. Sandhi compound splitting tests split-point pairs $(w_1, w_2)$ against the Trie in $O(L \\cdot |\\Sigma|)$, boosting transcription accuracy by 15%."),

            ("When do you use a Trie over a Hash Table?",
             "A Hash Table offers $O(1)$ average lookup for exact keys, but cannot execute prefix matching, range queries, or nearest-neighbor phonetic search. "
             "A Trie provides $O(L)$ deterministic lookup (where $L$ is word length), supports prefix autocomplete, and allows simultaneous branch pruning during fuzzy dynamic programming search, making it the optimal data structure for spell-checking and Sandhi grammar engines.")
        ]),

        # CATEGORY D: FULL-STACK, CLOUD & DEVOPS ARCHITECTURE
        ("Category D: Full-Stack Architecture, WebGPU & Cloud Systems", [
            ("How do you design a distributed, high-throughput OCR and Translation Pipeline for 100,000 manuscript pages/hour?",
             "<b>Architecture:</b><br/>"
             "1. <b>Ingestion Layer:</b> API Gateway with Amazon S3 presigned upload URLs and message queuing via Apache Kafka / RabbitMQ.<br/>"
             "2. <b>Compute Workers:</b> Kubernetes auto-scaling worker pods running GPU-accelerated PyTorch TrOCR inference using TensorRT or ONNX Runtime.<br/>"
             "3. <b>Caching & Fast Retrieval:</b> Redis cache for frequent subword embeddings and Levenshtein lookups.<br/>"
             "4. <b>Storage & Indexing:</b> PostgreSQL with pgvector for semantic search over historical epigraphical corpora and MinIO/S3 for tile storage."),

            ("Walk me through a zero-downtime Kubernetes rolling deployment.",
             "In Kubernetes, the Deployment controller manages a ReplicaSet with a `RollingUpdate` strategy. "
             "When a new image tag is deployed, K8s creates a new Pod with the updated version. "
             "The old Pod continues serving traffic until the new Pod passes both `readinessProbe` (verifying HTTP endpoints and DB connections) and `livenessProbe`. "
             "Once healthy, the Service LoadBalancer redirects ingress traffic to the new pod, and the old pod is gracefully terminated (`SIGTERM` with `terminationGracePeriodSeconds: 30`).")
        ])
    ]

    for cat_title, qas in qa_sections:
        story.append(Paragraph(f"<b>{cat_title}</b>", h2_style))
        for q, a in qas:
            story.append(Paragraph(f"<b>Q: {q}</b>", q_style))
            story.append(Paragraph(f"<b>Answer:</b> {a}", a_style))
        story.append(Spacer(1, 4))

    # ==========================================
    # SECTION 6: BEHAVIORAL & LEADERSHIP (STAR METHOD)
    # ==========================================
    story.append(Paragraph("6. Behavioral & Leadership Questions (STAR Method)", h1_style))

    star_examples = [
        ("Tell me about a time you faced an ambiguous or difficult technical challenge and how you solved it.",
         "<b>Situation:</b> In EpigraphiX-AI, standard OCR models (Tesseract, EasyOCR) failed completely on 1,000-year-old palm leaves because horizontal fiber grain and leaf stains were misclassified as character strokes.<br/>"
         "<b>Task:</b> I needed to create an automated restoration and recognition pipeline that could run in real-time in the browser without requiring massive cloud compute.<br/>"
         "<b>Action:</b> I formulated an $O(1)$ Integral-Image Sauvola algorithm for &lt;5ms binarization, developed FANI 2.0 directional morphological inpainting, and trained a TrOCR Vision Transformer with Persistent Homology Betti topological invariants for ligature classification.<br/>"
         "<b>Result:</b> Achieved &gt;90% character accuracy and &lt;300ms end-to-end inference latency, creating a zero-dependency web studio that runs entirely client-side."),

        ("Describe a situation where you had to balance technical debt with strict delivery deadlines.",
         "<b>Situation:</b> During my internship at The Skybrisk, the team needed to ship the core ERP Purchase & Invoicing modules within a 3-week sprint while the existing state management was becoming unmaintainable.<br/>"
         "<b>Task:</b> I had to deliver the complete GRN and invoicing workflow without introducing regressions or fragile prop drilling.<br/>"
         "<b>Action:</b> I advocated for migrating to Redux Toolkit state slices with normalized state shapes. I created reusable custom hooks for API caching and wrapped routes with an RBAC higher-order component.<br/>"
         "<b>Result:</b> Delivered the module 2 days ahead of deadline and reduced subsequent bug report tickets by 35% across the sprint."),

        ("How do you handle critical feedback during a technical code review?",
         "<b>Situation:</b> In my DevOps internship at CODTECH, a senior engineer noted that my initial GitHub Actions CI/CD pipeline lacked security vulnerability gates and used hardcoded container tags.<br/>"
         "<b>Task:</b> Refactor the pipeline to adhere to enterprise security and semantic versioning standards.<br/>"
         "<b>Action:</b> I actively welcomed the feedback, researched OWASP ZAP DAST integration, added automated vulnerability scanning, and transitioned Docker builds to Git SHA-based immutable tags.<br/>"
         "<b>Result:</b> Established a hardened DevSecOps template that became the standard CI/CD workflow across the internship repository.")
    ]

    for q, star_text in star_examples:
        story.append(Paragraph(f"<b>Q: {q}</b>", q_style))
        story.append(Paragraph(star_text, star_label))
        story.append(Spacer(1, 3))

    # ==========================================
    # SECTION 7: SMART QUESTIONS TO ASK INTERVIEWERS
    # ==========================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Strategic Questions to Ask Interviewers", h1_style))
    story.append(Paragraph("1. <i>\"How does your engineering team manage the lifecycle between ML research prototypes and production-hardened microservices?\"</i>", bullet_style))
    story.append(Paragraph("2. <i>\"What are the highest-priority architectural milestones your team is aiming to achieve over the next two quarters?\"</i>", bullet_style))
    story.append(Paragraph("3. <i>\"What does success look like for an engineer in this role during the first 90 days?\"</i>", bullet_style))
    story.append(Paragraph("4. <i>\"How does the team foster continuous learning and adoption of emerging technologies (e.g., WebGPU, Edge AI, DevSecOps)?\"</i>", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✔ Successfully generated Master Guide PDF at: {filename}")
    return filename


if __name__ == "__main__":
    downloads_path = r"C:\Users\HP\Downloads"
    output_pdf = os.path.join(downloads_path, "Adarsh_S_Interview_Master_Guide.pdf")
    build_pdf(output_pdf)
