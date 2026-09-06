import os
import shutil
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas

class CertificateCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(CertificateCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_certificate_frame()
            super(CertificateCanvas, self).showPage()
        super(CertificateCanvas, self).save()

    def draw_certificate_frame(self):
        w, h = landscape(letter) # 792 x 612
        self.saveState()
        
        # Outer Gold Border
        self.setStrokeColor(colors.HexColor('#d97706')) # Warm Gold
        self.setLineWidth(5)
        self.rect(20, 20, w - 40, h - 40)
        
        # Inner Navy Border
        self.setStrokeColor(colors.HexColor('#1e3a8a')) # Deep Navy
        self.setLineWidth(2)
        self.rect(28, 28, w - 56, h - 56)
        
        # Thin Accent Border
        self.setStrokeColor(colors.HexColor('#fbbf24')) # Light Gold
        self.setLineWidth(0.8)
        self.rect(32, 32, w - 64, h - 64)
        
        # Corner Ornaments
        corner_len = 32
        self.setStrokeColor(colors.HexColor('#d97706'))
        self.setLineWidth(2.5)
        # Top-Left
        self.line(36, h - 36, 36 + corner_len, h - 36)
        self.line(36, h - 36, 36, h - 36 - corner_len)
        # Top-Right
        self.line(w - 36, h - 36, w - 36 - corner_len, h - 36)
        self.line(w - 36, h - 36, w - 36, h - 36 - corner_len)
        # Bottom-Left
        self.line(36, 36, 36 + corner_len, 36)
        self.line(36, 36, 36, 36 + corner_len)
        # Bottom-Right
        self.line(w - 36, 36, w - 36 - corner_len, 36)
        self.line(w - 36, 36, w - 36, 36 + corner_len)
        
        # Official Gold Seal (Bottom Center)
        cx, cy = w / 2.0, 72
        self.setFillColor(colors.HexColor('#fef3c7'))
        self.setStrokeColor(colors.HexColor('#d97706'))
        self.setLineWidth(2.5)
        self.circle(cx, cy, 34, fill=1, stroke=1)
        
        # Seal Inner Star Ring
        self.setFillColor(colors.HexColor('#b45309'))
        self.setFont('Helvetica-Bold', 7)
        self.drawCentredString(cx, cy + 14, '★ ★ ★')
        self.setFont('Helvetica-Bold', 8)
        self.drawCentredString(cx, cy + 3, 'OFFICIAL')
        self.drawCentredString(cx, cy - 8, 'VERIFIED')
        self.setFont('Helvetica-Bold', 6)
        self.drawCentredString(cx, cy - 19, '★ RESEARCH ARCHIVE ★')
        
        # Bottom Footer Bar
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(45, 42, 'Certificate ID: CERT-EPI-2026-9842')
        self.drawRightString(w - 45, 42, 'Global Scientific Indexing & Archival Network')
        
        self.restoreState()

def generate_certificate():
    pdf_path = 'C:/Users/HP/Downloads/Certificate_of_Publication_Adarsh_S.pdf'
    local_path = 'Certificate_of_Publication_Adarsh_S.pdf'
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        leftMargin=50,
        rightMargin=50,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle(
        'CertHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#b45309'),
        spaceAfter=3
    )
    
    main_title_style = ParagraphStyle(
        'CertMainTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        alignment=1,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'CertSubTitle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#475569'),
        spaceAfter=6
    )
    
    author_name_style = ParagraphStyle(
        'CertAuthor',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=22,
        leading=26,
        alignment=1,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3
    )
    
    affil_style = ParagraphStyle(
        'CertAffil',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    cert_text_style = ParagraphStyle(
        'CertText',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#475569'),
        spaceAfter=4
    )
    
    paper_title_style = ParagraphStyle(
        'CertPaperTitle',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=12,
        leading=15.5,
        alignment=1,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=8
    )
    
    details_style = ParagraphStyle(
        'CertDetails',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor('#334155'),
        spaceAfter=12
    )
    
    story = []
    
    story.append(Paragraph('INTERNATIONAL SCIENTIFIC RESEARCH & DIGITAL PALAEOGRAPHY ARCHIVE', header_style))
    story.append(Paragraph('CERTIFICATE OF RESEARCH PUBLICATION', main_title_style))
    story.append(Paragraph('This is to proudly certify that the original research paper authored by', subtitle_style))
    story.append(Paragraph('ADARSH S.', author_name_style))
    story.append(Paragraph('Department of Computer Science & Engineering, APJ Abdul Kalam Technological University, Kerala, India', affil_style))
    story.append(Paragraph('entitled', cert_text_style))
    story.append(Paragraph('“EpigraphiX-AI: Neural Epigraphical OCR, Topological Binarization, Strict Manuscript Authentication, and Multi-Model Intelligence for Degraded Historical Palm-Leaf Manuscripts”', paper_title_style))
    
    summary_text = 'has been peer-archived, verified, and officially published in the global open-access scientific repository with permanent Digital Object Identifier (DOI) and international bibliographic indexing.'
    story.append(Paragraph(summary_text, details_style))
    story.append(Spacer(1, 4))
    
    # Signatures & Verification Grid
    sig_cell_style = ParagraphStyle('SigCell', parent=styles['Normal'], fontName='Times-Roman', fontSize=9, leading=12.5, alignment=1, textColor=colors.HexColor('#334155'))
    
    sig_table_data = [
        [
            Paragraph('<b>Date of Publication:</b><br/>August 25, 2026<br/><b>Status:</b> Verified Open Access', sig_cell_style),
            Paragraph('', sig_cell_style), # Spacer for center seal
            Paragraph('<b>Verified & Certified By:</b><br/><b>Editorial & Research Review Board</b><br/>Computational Epigraphy Council', sig_cell_style)
        ]
    ]
    
    sig_table = Table(sig_table_data, colWidths=[220, 252, 220])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    
    story.append(sig_table)
    
    doc.build(story, canvasmaker=CertificateCanvas)
    
    shutil.copy(pdf_path, local_path)
    print(f'Successfully generated Certificate of Publication at: {pdf_path}')

if __name__ == '__main__':
    generate_certificate()
