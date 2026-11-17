import re
path = 'C:/Users/jeeva/Documents/finance-trace/backend/app/services/report_gen.py'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Add import at top
content = content.replace(
    'from app.models.audit import AuditLog',
    'from app.models.audit import AuditLog\nfrom app.services.forensics import analyze_case'
)

# Add findings section after exec summary
findings_code = '''
    # --- NEW: Forensic Findings ---
    alerts = analyze_case(db, case_id)
    story.append(Paragraph("2. Key Forensic Findings", h2))
    if alerts:
        alert_data = [["Severity", "Finding"]]
        for a in alerts:
            alert_data.append([a["severity"], a["message"]])
        al_table = Table(alert_data, colWidths=[25*mm, 150*mm])
        al_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#b91c1c")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("TEXTCOLOR", (0,1), (0,-1), colors.HexColor("#b91c1c")), # Red severity
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(al_table)
    else:
        story.append(Paragraph("No suspicious patterns detected with current rule set.", body))
    story.append(PageBreak())
'''
# Insert findings before Section 2 (Parties)
content = content.replace(
    '    # Parties\n    story.append(Paragraph("2. Parties Identified", h2))',
    findings_code + '\n    # Parties\n    story.append(Paragraph("3. Parties Identified", h2))'
)

# Renumber the rest
content = content.replace('3. Bank Accounts Identified', '4. Bank Accounts Identified')
content = content.replace('4. Fund-Flow Matrix', '5. Fund-Flow Matrix')
content = content.replace('5. Chronological Transaction Log', '6. Chronological Transaction Log')
content = content.replace('6. Document Chain of Custody', '7. Document Chain of Custody')
content = content.replace('7. Audit Trail', '8. Audit Trail')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Report patched with findings!")