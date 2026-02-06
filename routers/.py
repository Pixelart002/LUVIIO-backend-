from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf():
    filename = "Jen_Hisab_Suresh_Ji_Calculation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("Jen Hisab / Suresh Ji - Calculation Sheet", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Data for the table
    data = [
        ["Date", "Item Description", "Calculation", "Amount (INR)"],
        ["31/12/26", "5 1/2 Katora", "305 x 1.30", "396.50"],
        ["", "5/4 Katora tapen gulli", "700 x 2.50", "1,750.00"],
        ["", "5-5 Katora", "1800 x 1.5", "2,700.00"],
        ["11/1/26", "Tapen Gulli (15)", "1244 x 2.5", "3,110.00"],
        ["", "5 1/2 Katora", "1270 x 1.30", "1,651.00"],
        ["", "Pone char Jali", "2000 x .70", "1,400.00"],
        ["20/1/2026", "5 1/2 Katora", "2180 x 1.30", "2,834.00"],
        ["", "5-5 Katora (20)", "692 x 1.50", "1,038.00"],
        ["", "Pone char Jali", "2000 x .70", "1,400.00"],
        ["25/1/26", "Pone char Jali", "2200 x .70", "1,540.00"],
        ["", '" " (ditto)', "2700 x .70", "1,890.00"],
        ["", "", "TOTAL", "19,709.50"]
    ]

    # Create Table
    table = Table(data, colWidths=[80, 200, 100, 100])

    # Add Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'), # Align amounts to right
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), # Total row background
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'), # Total row bold
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)
    print(f"PDF generated: {filename}")

create_pdf()
