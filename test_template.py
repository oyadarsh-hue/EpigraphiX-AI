import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, FrameBreak, PageBreak, NextPageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def test_template():
    pdf_filename = "test_ieee_layout.pdf"
    doc = BaseDocTemplate(pdf_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    
    # Frames for Page 1: Top banner frame + 2 bottom column frames
    f_top = Frame(36, 520, 540, 230, id='f_top', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    f_p1_c1 = Frame(36, 40, 261, 470, id='f_p1_c1', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    f_p1_c2 = Frame(315, 40, 261, 470, id='f_p1_c2', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    
    # Frames for Subsequent Pages: 2 full column frames
    f_c1 = Frame(36, 40, 261, 710, id='f_c1', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    f_c2 = Frame(315, 40, 261, 710, id='f_c2', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    
    first_page_template = PageTemplate(id='FirstPage', frames=[f_top, f_p1_c1, f_p1_c2])
    two_col_template = PageTemplate(id='TwoCol', frames=[f_c1, f_c2])
    
    doc.addPageTemplates([first_page_template, two_col_template])
    
    styles = getSampleStyleSheet()
    story = []
    
    # Tell document to use TwoCol for next page
    story.append(NextPageTemplate('TwoCol'))
    
    # Top frame content (Title, Authors, Abstract)
    story.append(Paragraph("<b>EpigraphiX-AI: Neural Palm-Leaf Manuscript OCR</b>", styles['Title']))
    story.append(Paragraph("Adarsh S. et al.", styles['Normal']))
    story.append(Paragraph("<b>Abstract</b>—This is a test abstract of the paper.", styles['Normal']))
    story.append(FrameBreak()) # Move to bottom Col 1
    
    # Col 1
    story.append(Paragraph("<b>I. INTRODUCTION</b>", styles['Heading2']))
    story.append(Paragraph("Introduction paragraph in column 1. Palm leaf manuscripts are historical records.", styles['Normal']))
    for i in range(10):
        story.append(Paragraph(f"Paragraph {i} in column 1 testing text flow across frames.", styles['Normal']))
    story.append(FrameBreak()) # Move to Col 2
    
    # Col 2
    story.append(Paragraph("<b>II. RELATED WORK</b>", styles['Heading2']))
    for i in range(10):
        story.append(Paragraph(f"Paragraph {i} in column 2 testing text flow across frames.", styles['Normal']))
        
    doc.build(story)
    print("Test build successful!")

if __name__ == "__main__":
    test_template()
