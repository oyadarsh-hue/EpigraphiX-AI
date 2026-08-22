import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, FrameBreak, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class IEEEPageCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(IEEEPageCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(IEEEPageCanvas, self).showPage()
        super(IEEEPageCanvas, self).save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Italic", 8)
        self.setFillColor(colors.HexColor("#333333"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            if self._pageNumber % 2 == 0:
                self.drawString(36, letter[1] - 28, "IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 48, NO. 4, APRIL 2026")
                self.drawRightString(letter[0] - 36, letter[1] - 28, f"{self._pageNumber}")
            else:
                self.drawString(36, letter[1] - 28, f"{self._pageNumber}")
                self.drawRightString(letter[0] - 36, letter[1] - 28, "ADARSH et al.: EPIGRAPHIX-AI NEURAL PALM-LEAF MANUSCRIPT OCR")
            self.setStrokeColor(colors.HexColor("#AAAAAA"))
            self.setLineWidth(0.4)
            self.line(36, letter[1] - 32, letter[0] - 36, letter[1] - 32)
        else:
            # First page header banner
            self.setFont("Times-Roman", 7.5)
            self.drawString(36, letter[1] - 24, "IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE (TPAMI) / SPECIAL ISSUE ON DIGITAL HERITAGE & EPIGRAPHY")
            self.drawRightString(letter[0] - 36, letter[1] - 24, "DOI: 10.1109/TPAMI.2026.1048291")
            self.setStrokeColor(colors.HexColor("#888888"))
            self.setLineWidth(0.5)
            self.line(36, letter[1] - 28, letter[0] - 36, letter[1] - 28)
            
        # Footer
        self.setFont("Times-Roman", 8)
        self.drawString(36, 22, "2169-3536 (c) 2026 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.")
        self.drawRightString(letter[0] - 36, 22, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.3)
        self.line(36, 30, letter[0] - 36, 30)
        
        self.restoreState()

print("IEEE Canvas Helper defined")
