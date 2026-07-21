"""
Generate professional PDF documentation for Finance Audit Management System
Requirements: A4, Arial font, 15px heading, 14px subheading, 12px body, justified, page numbers
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os


class NumberedCanvas(canvas.Canvas):
    """Custom canvas to add page numbers at bottom-right"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_state = None

    def showPage(self):
        self._add_page_number()
        canvas.Canvas.showPage(self)

    def _add_page_number(self):
        self.setFont("Helvetica", 10)
        self.drawRightString(
            A4[0] - 15*mm,
            15*mm,
            f"Page {self._pageNumber}"
        )


def create_documentation_pdf(output_path):
    """Create the PDF documentation"""
    
    # Set up the PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Define custom styles
    styles = getSampleStyleSheet()
    
    # Title style (15pt, Arial, centered)
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    # Heading style (15pt, Arial, bold, justified)
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=8,
        spaceBefore=8,
        alignment=TA_JUSTIFY
    )
    
    # Subheading style (14pt, Arial, bold, justified)
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=6,
        spaceBefore=6,
        alignment=TA_JUSTIFY
    )
    
    # Body style (12pt, Arial, justified)
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )
    
    # Build the content
    story = []
    
    # ===== TITLE PAGE =====
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("Finance Audit Management System", title_style))
    story.append(Paragraph("Project Documentation", title_style))
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("A Comprehensive Web Application for Financial Audit & Project Management", body_style))
    story.append(Spacer(1, 30*mm))
    
    # Metadata table
    metadata = [
        ['Document Type:', 'Project Documentation'],
        ['Version:', '1.0'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Framework:', 'Flask (Python)'],
        ['Status:', 'Active Development']
    ]
    
    metadata_table = Table(metadata, colWidths=[60*mm, 80*mm])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e6e6e6'))
    ]))
    
    story.append(metadata_table)
    story.append(PageBreak())
    
    # ===== PROBLEM STATEMENT =====
    story.append(Paragraph("1. Problem Statement", heading_style))
    
    problem_text = """
    Organizations face significant challenges in managing financial audits and project finances efficiently. 
    Traditional methods rely on scattered spreadsheets, manual data entry, and disconnected reporting systems. 
    This leads to:<br/><br/>
    • <b>Data Inconsistency:</b> Multiple versions of truth across different departments and teams<br/>
    • <b>Inefficient Auditing:</b> Time-consuming manual review processes and slow compliance reporting<br/>
    • <b>Poor Risk Visibility:</b> Lack of centralized dashboard for financial risk assessment<br/>
    • <b>Limited Collaboration:</b> No unified platform for auditors and project managers to work together<br/>
    • <b>Compliance Challenges:</b> Difficulty tracking findings and recommendations across projects
    """
    
    story.append(Paragraph(problem_text, body_style))
    story.append(Spacer(1, 8*mm))
    
    # ===== SOLUTION & FEATURES =====
    story.append(Paragraph("2. Solution & Features", heading_style))
    
    solution_text = """
    The Finance Audit Management System provides a unified, web-based platform for managing projects, 
    audits, and financial transactions. It enables organizations to streamline audit processes, track 
    compliance, and make data-driven financial decisions.
    """
    
    story.append(Paragraph(solution_text, body_style))
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph("Key Features:", subheading_style))
    
    features_text = """
    <b>Project Management:</b> Create, edit, and monitor projects with budget allocation, 
    timeline tracking, and risk assessment<br/><br/>
    
    <b>Audit Management:</b> Log audit activities with findings, compliance scores, and risk ratings. 
    Track audit progress and generate reports<br/><br/>
    
    <b>Financial Tracking:</b> Record transactions, categorize expenses, and monitor budget utilization 
    against actual spending<br/><br/>
    
    <b>Role-Based Access:</b> Admin users manage all projects and audits; regular users manage their 
    assigned projects<br/><br/>
    
    <b>Dashboard & Analytics:</b> Real-time visualization of project status, budget variance, risk 
    distribution, and compliance metrics<br/><br/>
    
    <b>User Authentication:</b> Secure registration and login system with password hashing and session 
    management<br/><br/>
    
    <b>Reporting:</b> Generate comprehensive financial and audit reports with status breakdown, risk 
    analysis, and budget summaries
    """
    
    story.append(Paragraph(features_text, body_style))
    story.append(PageBreak())
    
    # ===== SCREENSHOTS & USER INTERFACE =====
    story.append(Paragraph("3. Screenshots & User Interface", heading_style))
    
    story.append(Paragraph("Dashboard", subheading_style))
    story.append(Paragraph(
        "The main dashboard provides at-a-glance metrics including total projects, active audits, "
        "budget summaries, and high-risk project counts. Charts visualize project status distribution "
        "and recent audit activities.",
        body_style
    ))
    story.append(Spacer(1, 8*mm))
    
    story.append(Paragraph("Projects View", subheading_style))
    story.append(Paragraph(
        "Displays all projects with filtering and sorting capabilities. Each project shows name, code, "
        "status, budget allocation, and risk level. Users can quickly identify budget variances and "
        "project health status.",
        body_style
    ))
    story.append(Spacer(1, 8*mm))
    
    story.append(Paragraph("Audit Management", subheading_style))
    story.append(Paragraph(
        "Comprehensive audit logging interface allowing users to record audit findings, associate audits "
        "with projects, assign risk scores and compliance ratings. Supports multiple audit types: internal, "
        "external, compliance, and financial audits.",
        body_style
    ))
    story.append(Spacer(1, 8*mm))
    
    story.append(Paragraph("Reports Section", subheading_style))
    story.append(Paragraph(
        "Generates dynamic financial reports including project status breakdown, budget utilization metrics, "
        "risk distribution analysis, and compliance score aggregation across all audits.",
        body_style
    ))
    story.append(PageBreak())
    
    # ===== TECH STACK =====
    story.append(Paragraph("4. Technology Stack", heading_style))
    
    story.append(Paragraph("Backend", subheading_style))
    tech_backend = [
        ['Technology', 'Purpose'],
        ['Python 3', 'Core programming language'],
        ['Flask 2.3.3', 'Web framework and routing'],
        ['Flask-SQLAlchemy', 'ORM for database operations'],
        ['Flask-Login', 'User authentication & session mgmt']
    ]
    
    backend_table = Table(tech_backend, colWidths=[50*mm, 90*mm])
    backend_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    story.append(backend_table)
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("Frontend", subheading_style))
    tech_frontend = [
        ['Technology', 'Purpose'],
        ['HTML5/CSS3', 'Markup and styling'],
        ['JavaScript', 'Client-side interactivity'],
        ['Jinja2', 'Template engine'],
        ['Bootstrap', 'Responsive UI framework']
    ]
    
    frontend_table = Table(tech_frontend, colWidths=[50*mm, 90*mm])
    frontend_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    story.append(frontend_table)
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("Database & Security", subheading_style))
    tech_other = [
        ['Technology', 'Purpose'],
        ['SQLite/PostgreSQL', 'Relational database'],
        ['Werkzeug', 'Password hashing & WSGI utilities'],
        ['Flask-WTF', 'CSRF protection & form validation'],
        ['python-dotenv', 'Environment variable management']
    ]
    
    other_table = Table(tech_other, colWidths=[50*mm, 90*mm])
    other_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    story.append(other_table)
    story.append(PageBreak())
    
    # ===== UNIQUE POINTS =====
    story.append(Paragraph("5. Unique Points / Competitive Advantages", heading_style))
    
    unique_text = """
    <b>Role-Based Access Control:</b> Differentiated permissions for admin and user roles enable 
    secure, multi-tenant usage where auditors see only relevant data.<br/><br/>
    
    <b>Integrated Risk Scoring:</b> Combines risk assessment and compliance scoring in one platform, 
    allowing organizations to quantify and track audit outcomes systematically.<br/><br/>
    
    <b>Budget Variance Tracking:</b> Real-time comparison of budgeted vs. actual spending per project, 
    with calculated variance metrics for financial oversight.<br/><br/>
    
    <b>Comprehensive Audit Logging:</b> Supports multiple audit types (internal, external, compliance, 
    financial) with findings, recommendations, and corrective action tracking.<br/><br/>
    
    <b>Transaction Management:</b> Detailed transaction recording with vendor tracking, payment status, 
    and receipt file attachment capabilities.<br/><br/>
    
    <b>Multi-Level Reporting:</b> Dashboard-level summaries, project-level details, and organization-wide 
    reports provide insights at every level.<br/><br/>
    
    <b>Finding Management:</b> Track audit findings with severity levels, corrective actions, and 
    resolution status for compliance documentation.
    """
    
    story.append(Paragraph(unique_text, body_style))
    story.append(Spacer(1, 8*mm))
    
    # ===== FUTURE IMPROVEMENTS =====
    story.append(Paragraph("6. Future Improvements & Roadmap", heading_style))
    
    future_text = """
    <b>Advanced Analytics & AI:</b> Implement predictive analytics to forecast budget risks and suggest 
    audit priorities based on historical patterns.<br/><br/>
    
    <b>Mobile Application:</b> Develop iOS and Android apps for auditors to log findings and review 
    projects on-the-go.<br/><br/>
    
    <b>API Integration:</b> RESTful API for third-party integrations with accounting software (QuickBooks, 
    SAP) and document management systems.<br/><br/>
    
    <b>Advanced Search & Filtering:</b> Full-text search, saved filters, and smart search suggestions 
    for faster data discovery.<br/><br/>
    
    <b>Workflow Automation:</b> Configurable audit workflows, automated notifications, and approval routing 
    for findings and recommendations.<br/><br/>
    
    <b>Multi-language Support:</b> Localization for global organizations to use the system in preferred languages.<br/><br/>
    
    <b>Enhanced Reporting:</b> Export to multiple formats (PDF, Excel, Word), custom report builder, and 
    scheduled email reports.<br/><br/>
    
    <b>Two-Factor Authentication:</b> Implement 2FA for enhanced security of sensitive financial data.<br/><br/>
    
    <b>Audit Trail Enhancements:</b> Detailed logging of all user actions with immutable audit logs for 
    compliance and forensic analysis.
    """
    
    story.append(Paragraph(future_text, body_style))
    
    # Build PDF with custom canvas for page numbers
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ PDF documentation created: {output_path}")
    print(f"✓ File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")


if __name__ == '__main__':
    output_file = os.path.join(
        os.path.dirname(__file__),
        'Finance_Audit_System_Documentation.pdf'
    )
    create_documentation_pdf(output_file)
