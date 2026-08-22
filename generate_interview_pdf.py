import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

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
            self.draw_page_number(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, letter[1] - 30, "Adarsh S — Comprehensive Interview Preparation Master Guide")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(40, letter[1] - 35, letter[0] - 40, letter[1] - 35)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 25, page_text)
        self.drawString(40, 25, "Confidential — Prepared for Technical & HR Interview Rounds")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(40, 37, letter[0] - 40, 37)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY = colors.HexColor("#2B6CB0") # Vibrant Slate Blue
    ACCENT = colors.HexColor("#C53030")    # Subdued Crimson
    DARK_TEXT = colors.HexColor("#2D3748") # Charcoal
    LIGHT_BG = colors.HexColor("#F7FAFC")  # Off-white
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=1, # Center
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold_Custom',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=15,
        spaceAfter=3
    )

    q_style = ParagraphStyle(
        'Question_Style',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        'Answer_Style',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=10,
        spaceAfter=6
    )

    star_label = ParagraphStyle(
        'STAR_Label',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=ACCENT,
        leftIndent=10,
        spaceAfter=1
    )

    story = []

    # Title Banner
    story.append(Paragraph("ADARSH S — INTERVIEW MASTER GUIDE", title_style))
    story.append(Paragraph("Comprehensive Project Explanations, Technical Architecture, and Q&A from Resume", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # SECTION 1: ELEVATOR PITCH
    story.append(Paragraph("1. Master Elevator Pitch: \"Tell Me About Yourself\"", h1_style))
    pitch_text = (
        "<b>Script (60-90 Seconds):</b><br/>"
        "\"Good morning/afternoon. I am an MCA graduate from Government Engineering College, Thrissur, with a solid technical "
        "foundation across Computer Vision, Applied AI, and Full-Stack Software Engineering. "
        "Over the past year, I have translated academic theory into real-world engineering across three distinct internships and research projects. "
        "First, I built <b>EpigraphiX-AI</b>, an advanced document intelligence platform combining custom Sauvola binarization, CNN neural lattices, "
        "and NLP Levenshtein decoders to transcribe ancient palm-leaf manuscripts with over 90% accuracy. "
        "Second, I architected <b>AssentTag</b>, a biometric privacy platform leveraging ResNet 128D facial embeddings and OpenCV for automated "
        "selective blurring and consent management. "
        "Professionally, I completed internships at <b>Bluegen Solutions</b> building Django backends, <b>The Skybrisk</b> delivering MERN-based ERP modules, "
        "and <b>CODTECH IT Solutions</b> automating CI/CD pipelines and Kubernetes container orchestration. "
        "I am looking for a Software Engineering / AI Engineer role where I can build scalable, high-performance systems and solve challenging business problems.\""
    )
    story.append(Paragraph(pitch_text, body_style))
    story.append(Spacer(1, 8))

    # SECTION 2: EPIGRAPHIX-AI
    story.append(Paragraph("2. Deep-Dive: EpigraphiX-AI (Palm-Leaf Manuscript OCR Suite)", h1_style))
    story.append(Paragraph("<b>Project Summary:</b> SOTA Document Vision & Epigraphical Intelligence platform designed to restore, segment, transcribe, and translate degraded ancient Malayalam & Grantha palm-leaf manuscripts (<i>Thaliyola</i>).", body_style))
    story.append(Spacer(1, 4))
    
    # Tech Architecture Table
    epigraphix_table_data = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Technologies Used</b>", body_bold), Paragraph("<b>Engineering Highlights & Metrics</b>", body_bold)],
        [
            Paragraph("Restoration & Vision Pipeline", body_style),
            Paragraph("OpenCV, MATLAB, Sauvola Algorithm, FANI", body_style),
            Paragraph("Engineered $O(1)$ Integral-Image Sauvola Binarization (<5ms latency); Fiber-Aware Inpainting suppresses cellulose grain noise while preserving stylus incisions.", body_style)
        ],
        [
            Paragraph("ML / DL Classifier Decision Space", body_style),
            Paragraph("CNN Neural Lattice, SVM, Random Forest, k-NN, GNB, Scikit-learn", body_style),
            Paragraph("Benchmarked a 5-classifier ensemble using Topological Betti Invariants ($\\beta_0, \\beta_1$) and loop curvature entropy; achieved >90% character accuracy.", body_style)
        ],
        [
            Paragraph("NLP Linguistic Correction Engine", body_style),
            Paragraph("Dynamic Programming, Levenshtein Distance, Trie Lexicon", body_style),
            Paragraph("Custom Sandhi grammar decoder and Malayalam Trie lexicon lookup aligned raw OCR outputs, reducing Word Error Rate (WER) by 15%.", body_style)
        ],
        [
            Paragraph("Interactive Web Studio & Translation", body_style),
            Paragraph("JavaScript (ES6+), HTML5 Canvas API, Node.js", body_style),
            Paragraph("Multi-row glyph segmentation, confidence heatmaps, trilingual semantic translation (Old/Modern Malayalam, English, Hindi), and vector PDF reports.", body_style)
        ]
    ]
    t1 = Table(epigraphix_table_data, colWidths=[120, 130, 280])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>EpigraphiX-AI Top Interview Questions:</b>", h2_style))
    
    story.append(Paragraph("Q1: Why did you use Sauvola Binarization instead of standard Otsu Thresholding?", q_style))
    story.append(Paragraph("<b>Answer:</b> Otsu calculates a single global threshold based on histogram bimodality. Palm-leaf manuscripts suffer from uneven aging, stains, and non-uniform lighting across the leaf surface. Global thresholding causes massive character loss in darker regions. Sauvola calculates local thresholds dynamically using local mean (m) and standard deviation (s): <i>T(x,y) = m * (1 + k * (s/R - 1))</i>. To make it real-time (<5ms), I implemented it using <b>O(1) Integral Images</b> for prefix-sum variance calculation.", a_style))

    story.append(Paragraph("Q2: What is the CNN Neural Lattice and why benchmark 5 different ML models?", q_style))
    story.append(Paragraph("<b>Answer:</b> Ancient manuscripts have limited training samples. Deep CNNs can overfit on small datasets. To build a robust decision space, I extracted geometric features (Loop Curvature Entropy, Horizontal Projection Variance, and Topological Betti numbers) and benchmarked SVM (RBF kernel), Random Forest (100 trees), k-NN, and Gaussian Naive Bayes alongside the CNN Neural Lattice to identify optimal precision-recall trade-offs.", a_style))

    story.append(Paragraph("Q3: How does the NLP post-processing engine reduce Word Error Rate (WER)?", q_style))
    story.append(Paragraph("<b>Answer:</b> Raw OCR output on degraded glyphs often produces ambiguous characters (e.g., confusing similar Malayalam ligatures). The NLP engine runs a dynamic programming Wagner-Fischer Levenshtein distance algorithm over a prefix Trie built from a 50,000-word Malayalam lexicon, applying weighted penalty matrices for visually confusable character pairs and boosting transcription accuracy by 15%.", a_style))

    story.append(Spacer(1, 8))

    # SECTION 3: ASSENTTAG
    story.append(Paragraph("3. Deep-Dive: AssentTag (Biometric Privacy & Consent Management)", h1_style))
    story.append(Paragraph("<b>Project Summary:</b> Privacy-by-Default Computer Vision & Biometric Consent platform designed to automatically blur non-consenting individuals in shared images/videos and orchestrate dynamic unblurring (\"The Veil\").", body_style))
    story.append(Spacer(1, 4))

    assenttag_table = [
        [Paragraph("<b>Layer</b>", body_bold), Paragraph("<b>Tech Stack</b>", body_bold), Paragraph("<b>Core Functionality & Architecture</b>", body_bold)],
        [
            Paragraph("Vision & Face Pipeline", body_style),
            Paragraph("OpenCV, Dlib, 68-Point Landmarks", body_style),
            Paragraph("Detects facial bounding boxes in real-time; applies selective Gaussian blurring to unverified faces while keeping consented users unblurred.", body_style)
        ],
        [
            Paragraph("Biometric Embeddings", body_style),
            Paragraph("ResNet-34 Deep Metric Learning", body_style),
            Paragraph("Extracts 128-dimensional facial embedding vectors; computes Euclidean distance ($d < 0.6$) against registered identity descriptors.", body_style)
        ],
        [
            Paragraph("Backend & Workflows", body_style),
            Paragraph("Python, Django, MySQL, REST APIs", body_style),
            Paragraph("Thread-safe descriptor matching, in-memory caching to eliminate redundant DB reads, dynamic consent approval requests (\"The Veil\"), and OTP authentication.", body_style)
        ]
    ]
    t2 = Table(assenttag_table, colWidths=[120, 130, 280])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>AssentTag Top Interview Questions:</b>", h2_style))
    
    story.append(Paragraph("Q1: How does biometric identification work with 128D facial embeddings?", q_style))
    story.append(Paragraph("<b>Answer:</b> Dlib's ResNet-34 model maps a detected face image into a 128-dimensional hypersphere where faces of the same person are clustered close together. When a media item is uploaded, the system extracts the 128D vector for each detected face and calculates the Euclidean Distance: <i>d(p, q) = sqrt(sum((p_i - q_i)^2))</i>. If the distance is below the tuned threshold (0.6), the face is classified as verified; otherwise, Gaussian blurring is automatically applied.", a_style))

    story.append(Paragraph("Q2: How did you design the in-memory descriptor caching in Django?", q_style))
    story.append(Paragraph("<b>Answer:</b> Querying MySQL for facial descriptors on every frame or batch image is a database I/O bottleneck. I implemented an in-memory caching layer storing serialized NumPy arrays of user embeddings. Matching is vectorized using matrix multiplications, reducing comparison latency from ~250ms per face to <10ms.", a_style))

    story.append(Paragraph("Q3: What is \"The Veil\" workflow and how does it enforce GDPR compliance?", q_style))
    story.append(Paragraph("<b>Answer:</b> Under GDPR, individuals have a right to privacy in shared digital media. By default, any face without explicit pre-consent is blurred. \"The Veil\" sends a push notification to the tagged individual with a preview request. Once the recipient approves the consent token, the system unblurs only their face in the rendered media.", a_style))

    story.append(Spacer(1, 8))

    # SECTION 4: PROFESSIONAL EXPERIENCE
    story.append(Paragraph("4. Deep-Dive: Professional Experience (Internships)", h1_style))
    
    # Skybrisk
    story.append(Paragraph("A. The Skybrisk — React.js Development Intern (Feb 2026 – Mar 2026)", h2_style))
    story.append(Paragraph("<b>Role Focus:</b> MERN-Stack Enterprise ERP Management System (Products, Orders, GRN, Invoicing, RBAC).", body_style))
    story.append(Paragraph("<b>Key Accomplishments:</b>", body_bold))
    story.append(Paragraph("• Built core ERP workflows: Product Catalog, Purchase/Sales Orders, Goods Receipt Note (GRN) tracking, and Invoicing.", bullet_style))
    story.append(Paragraph("• Implemented Redux Toolkit state slices for authentication, global alerts, and role-based access control (Admin, Sales, Purchase, Inventory).", bullet_style))
    story.append(Paragraph("• Integrated interactive Chart.js analytics dashboards and client-side PDF invoice export via jsPDF, boosting reporting speed by 20%.", bullet_style))
    story.append(Paragraph("<b>Interview Q: How does Role-Based Access Control (RBAC) work in your React application?</b><br/>"
                           "<b>Answer:</b> User authentication returns a signed JWT containing the user's role. In React Router v6, I wrapped sensitive routes inside a higher-order `ProtectedRoute` component. This component checks the Redux auth state and role permissions; unauthorized roles are redirected to an Access Denied view while valid requests render the target outlet.", a_style))

    # CODTECH
    story.append(Paragraph("B. CODTECH IT Solutions — DevOps Intern (Feb 2026 – Mar 2026)", h2_style))
    story.append(Paragraph("<b>Role Focus:</b> CI/CD Automation, Kubernetes Microservices Deployment, and DevSecOps.", body_style))
    story.append(Paragraph("<b>Key Accomplishments:</b>", body_bold))
    story.append(Paragraph("• Automated end-to-end CI/CD build, test, and release pipelines using GitHub Actions (`.github/workflows`).", bullet_style))
    story.append(Paragraph("• Orchestrated containerized microservices deployments with Kubernetes manifests (3 replica pods, Service LoadBalancers).", bullet_style))
    story.append(Paragraph("• Integrated OWASP ZAP DAST security scanning into GitHub Actions to identify security header flaws and enforce automated compliance.", bullet_style))
    story.append(Paragraph("<b>Interview Q: Explain your Kubernetes Deployment configuration and why 3 replicas?</b><br/>"
                           "<b>Answer:</b> I created declarative YAML manifests defining Deployments and Services. Configuring `replicas: 3` ensures high availability and zero-downtime rolling updates (`RollingUpdate` strategy). If any pod crashes, the K8s ReplicaSet controller automatically provisions a replacement pod while the Service LoadBalancer routes traffic to healthy pods.", a_style))

    # Bluegen
    story.append(Paragraph("C. Bluegen Solutions — Software Development Intern (Dec 2025 – Mar 2026)", h2_style))
    story.append(Paragraph("<b>Role Focus:</b> Python/Django Backend Architecture, MySQL Schema Normalization, API Development.", body_style))
    story.append(Paragraph("<b>Key Accomplishments:</b>", body_bold))
    story.append(Paragraph("• Engineered scalable Django REST API endpoints handling user sessions, authentication, and core business transactions.", bullet_style))
    story.append(Paragraph("• Normalized MySQL database schema across 8+ tables (3NF) with foreign-key indexing, cutting query latency by 25%.", bullet_style))
    story.append(Paragraph("• Profiled and resolved 15+ backend defects using Django Debug Toolbar and logging, enhancing server stability.", bullet_style))

    story.append(Spacer(1, 8))

    # SECTION 5: CORE TECHNICAL SKILLS Q&A
    story.append(Paragraph("5. Rapid-Fire Core Technical Concepts Q&A", h1_style))
    
    qa_list = [
        ("Data Structures: When to use a Trie over a Hash Table?",
         "A Hash Table has O(1) average lookup for exact matches but cannot perform prefix matching. A Trie allows O(L) prefix searches (where L is word length), making it ideal for autocomplete, dictionary spell-checking, and lexical search as used in EpigraphiX-AI."),
        
        ("Deep Learning: What is the vanishing gradient problem and how does ResNet solve it?",
         "In deep networks, backpropagated gradients shrink exponentially through chain rule multiplication, stopping early layers from updating. ResNet introduces identity 'skip connections' (residual mappings: F(x) + x) allowing gradients to flow directly back through the network without degradation."),
        
        ("DevOps: What is the difference between Docker and Kubernetes?",
         "Docker is a containerization platform to package applications and dependencies into standardized containers. Kubernetes is a container orchestration system that manages multiple containers across a cluster, providing auto-scaling, self-healing, load balancing, and rolling updates."),
         
        ("Security: How does JWT Authentication work?",
         "JWT is a stateless token containing Header, Payload, and Signature. The server signs the payload with a secret key. The client sends the token in the `Authorization: Bearer <token>` header. The server verifies the signature without needing to query a session database, enabling horizontal scalability.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>Q: {q}</b>", q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", a_style))

    story.append(Spacer(1, 8))

    # SECTION 6: BEHAVIORAL QUESTIONS (STAR METHOD)
    story.append(Paragraph("6. Behavioral & Situational Questions (STAR Method)", h1_style))
    
    story.append(Paragraph("<b>Q: Tell me about a time you faced a difficult technical challenge and how you solved it.</b>", q_style))
    story.append(Paragraph("<b>Situation:</b> During EpigraphiX-AI, standard OCR libraries failed completely on ancient palm leaves due to leaf fiber textures being misclassified as character strokes.", star_label))
    story.append(Paragraph("<b>Task:</b> I needed to design an optical restoration algorithm that suppressed natural leaf background noise without erasing fine stylus ink incisions.", star_label))
    story.append(Paragraph("<b>Action:</b> I researched adaptive local thresholding and developed an Integral-Image accelerated Sauvola binarization pipeline coupled with Fiber-Aware Neural Inpainting to isolate stylus grooves.", star_label))
    story.append(Paragraph("<b>Result:</b> Reduced binarization processing time to under 5ms per frame and increased OCR character recognition accuracy from ~65% to over 90%.", star_label))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Questions to Ask the Interviewer at the End:</b>", h2_style))
    story.append(Paragraph("1. \"What does the typical day-to-day engineering cycle look like for this team?\"", bullet_style))
    story.append(Paragraph("2. \"What are the key technical challenges or architecture goals the team is tackling this quarter?\"", bullet_style))
    story.append(Paragraph("3. \"What opportunities exist for someone in this role to contribute to both AI/ML pipelines and core full-stack services?\"", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {filename}")

if __name__ == "__main__":
    downloads_path = r"C:\Users\HP\Downloads"
    output_pdf = os.path.join(downloads_path, "Adarsh_S_Interview_Master_Guide.pdf")
    build_pdf(output_pdf)
