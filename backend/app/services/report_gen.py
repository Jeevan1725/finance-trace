import io
import uuid
from datetime import datetime
from decimal import Decimal
from collections import defaultdict
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.entity import Person, Company
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.document import Document
from app.models.audit import AuditLog


def _rs(amount) -> str:
    try:
        return "Rs. " + f"{float(amount):,.2f}"
    except Exception:
        return "Rs. 0.00"


def generate_report(db: Session, case_id: uuid.UUID) -> bytes:
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise ValueError("Case not found")

    persons = db.query(Person).filter(Person.case_id == case_id).all()
    companies = db.query(Company).filter(Company.case_id == case_id).all()
    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    txns = db.query(Transaction).filter(Transaction.case_id == case_id).order_by(Transaction.value_date).all()
    docs = db.query(Document).filter(Document.case_id == case_id).all()
    audits = db.query(AuditLog).filter(AuditLog.case_id == case_id).order_by(AuditLog.created_at).all()

    # Entity name lookup
    entity_names = {}
    for p in persons:
        entity_names[("PERSON", str(p.id))] = p.full_name
    for c in companies:
        entity_names[("COMPANY", str(c.id))] = c.name

    def _acc_label(acc):
        if not acc:
            return "???"
        name = entity_names.get((acc.entity_type, str(acc.entity_id)))
        if name:
            return name[:22] + " (*" + (acc.account_last4 or "????") + ")"
        return "*" + (acc.account_last4 or "????")

    # Aggregate flows
    edge_map = defaultdict(lambda: {"count": 0, "total": Decimal(0)})
    total_credit = Decimal(0)
    total_debit = Decimal(0)
    for t in txns:
        if t.direction == "CREDIT":
            total_credit += t.amount
        else:
            total_debit += t.amount
        if t.account_id and t.counterparty_entity_id:
            if t.direction == "DEBIT":
                src, dst = t.account_id, t.counterparty_entity_id
            else:
                src, dst = t.counterparty_entity_id, t.account_id
            edge_map[(str(src), str(dst))]["count"] += 1
            edge_map[(str(src), str(dst))]["total"] += t.amount

    acc_by_id = {str(a.id): a for a in accounts}

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=f"Forensic Report - {case.case_number}",
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#1e40af"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, textColor=colors.HexColor("#1e3a8a"), spaceBefore=12, spaceAfter=6)
    body = styles["BodyText"]
    small = ParagraphStyle("Small", parent=body, fontSize=8, leading=10)
    conf_style = ParagraphStyle("Confidential", parent=body, fontSize=9, textColor=colors.HexColor("#b91c1c"), alignment=1)

    story = []

    # Cover
    story.append(Paragraph("CONFIDENTIAL - FORENSIC ANALYSIS", conf_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Financial Fund-Flow Report", h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Case: {case.case_number}", h2))
    story.append(Paragraph(case.title, body))
    if case.description:
        story.append(Paragraph(case.description, body))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%d %b %Y %H:%M UTC')}", small))
    story.append(Paragraph(f"Case ID: {case.id}", small))
    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h2))
    summary_data = [
        ["Metric", "Count / Value"],
        ["Persons", str(len(persons))],
        ["Companies", str(len(companies))],
        ["Bank accounts detected", str(len(accounts))],
        ["Documents uploaded", str(len(docs))],
        ["Transactions parsed", str(len(txns))],
        ["Total credits (inflow)", _rs(total_credit)],
        ["Total debits (outflow)", _rs(total_debit)],
        ["Audit log entries", str(len(audits))],
    ]
    st = Table(summary_data, colWidths=[80*mm, 90*mm])
    st.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eff6ff")]),
    ]))
    story.append(st)
    story.append(Spacer(1, 12))

    # Parties
    story.append(Paragraph("2. Parties Identified", h2))
    party_data = [["Type", "Name", "PAN", "DIN/CIN", "Role"]]
    for p in persons:
        party_data.append(["Person", p.full_name, p.pan or "-", p.din or "-", p.role])
    for c in companies:
        party_data.append(["Company", c.name, c.pan or "-", c.cin or "-", "ENTITY"])
    if len(party_data) > 1:
        pt = Table(party_data, colWidths=[22*mm, 50*mm, 30*mm, 30*mm, 40*mm])
        pt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        story.append(pt)
    else:
        story.append(Paragraph("No persons or companies recorded for this case yet.", body))
    story.append(Spacer(1, 10))

    # Accounts
    story.append(Paragraph("3. Bank Accounts Identified", h2))
    acc_data = [["Last 4", "Bank", "Type", "Belongs To"]]
    for a in accounts:
        name = entity_names.get((a.entity_type, str(a.entity_id)))
        acc_data.append([a.account_last4 or "-", a.bank_name or "-", a.account_type, name or a.entity_type])
    if len(acc_data) > 1:
        at = Table(acc_data, colWidths=[30*mm, 50*mm, 40*mm, 50*mm])
        at.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        story.append(at)
    story.append(PageBreak())

    # Flow Matrix
    story.append(Paragraph("4. Fund-Flow Matrix (Source to Destination)", h2))
    if edge_map:
        flow_data = [["From", "To", "Txns", "Total Amount"]]
        for (src, dst), agg in sorted(edge_map.items(), key=lambda kv: -float(kv[1]["total"])):
            src_acc = acc_by_id.get(src)
            dst_acc = acc_by_id.get(dst)
            flow_data.append([
                _acc_label(src_acc),
                _acc_label(dst_acc),
                str(agg["count"]),
                _rs(agg["total"]),
            ])
        ft = Table(flow_data, colWidths=[55*mm, 55*mm, 15*mm, 45*mm])
        ft.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fef3c7")]),
        ]))
        story.append(ft)
    else:
        story.append(Paragraph("No fund-flow edges detected yet.", body))
    story.append(PageBreak())

    # Transaction Log
    story.append(Paragraph("5. Chronological Transaction Log", h2))
    txn_data = [["Date", "Amount", "Dir", "Mode", "Counterparty / Narration"]]
    for t in txns[:200]:
        txn_data.append([
            t.value_date.strftime("%d-%m-%Y"),
            _rs(t.amount),
            t.direction,
            t.mode or "-",
            (t.narration_raw or "")[:55],
        ])
    if len(txn_data) > 1:
        tt = Table(txn_data, colWidths=[20*mm, 25*mm, 14*mm, 18*mm, 95*mm])
        tt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 7),
            ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(tt)
        if len(txns) > 200:
            story.append(Paragraph(f"... {len(txns)-200} more transactions not shown.", small))
    story.append(PageBreak())

    # Chain of Custody
    story.append(Paragraph("6. Document Chain of Custody", h2))
    doc_data = [["File", "Type", "Size", "SHA-256 Hash", "Uploaded"]]
    for d in docs:
        doc_data.append([
            (d.file_name or "")[:30],
            d.doc_type,
            str(d.file_size or 0),
            (d.file_hash or "")[:16] + "...",
            d.uploaded_at.strftime("%d-%m-%Y %H:%M") if d.uploaded_at else "-",
        ])
    if len(doc_data) > 1:
        dt = Table(doc_data, colWidths=[40*mm, 20*mm, 18*mm, 40*mm, 30*mm])
        dt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 7),
            ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
        ]))
        story.append(dt)
    story.append(Spacer(1, 10))

    # Audit Trail
    story.append(Paragraph("7. Audit Trail (last 30 actions)", h2))
    audit_data = [["Time", "Action", "Target", "Actor"]]
    for a in audits[-30:]:
        audit_data.append([
            a.created_at.strftime("%d-%m-%Y %H:%M") if a.created_at else "-",
            a.action,
            a.target_type or "-",
            str(a.actor_id)[:8],
        ])
    if len(audit_data) > 1:
        audt = Table(audit_data, colWidths=[40*mm, 50*mm, 30*mm, 30*mm])
        audt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 7),
            ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
        ]))
        story.append(audt)

    doc.build(story)
    return buffer.getvalue()