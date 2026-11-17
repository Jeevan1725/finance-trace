import uuid
from datetime import timedelta
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.entity import Person, Company
from app.models.transaction import Transaction


def analyze_case(db: Session, case_id: uuid.UUID) -> list[dict]:
    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    txns = db.query(Transaction).filter(Transaction.case_id == case_id).order_by(Transaction.value_date).all()
    persons = {str(p.id): p.full_name for p in db.query(Person).filter(Person.case_id == case_id).all()}
    companies = {str(c.id): c.name for c in db.query(Company).filter(Company.case_id == case_id).all()}
    
    acc_by_id = {str(a.id): a for a in accounts}
    alerts = []

    def get_name(acc_id):
        acc = acc_by_id.get(acc_id)
        if not acc: return "Unknown"
        name = persons.get(str(acc.entity_id)) or companies.get(str(acc.entity_id))
        return f"{name} (*{acc.account_last4})" if name else f"*{acc.account_last4}"

    # 1. Layering (Pass-through) & Structuring per account
    inflows = defaultdict(lambda: {"total": 0.0, "count": 0, "small_count": 0})
    outflows = defaultdict(lambda: {"total": 0.0, "count": 0})
    
    for t in txns:
        if not t.account_id: continue
        acc_id = str(t.account_id)
        amt = float(t.amount)
        
        if t.direction == "CREDIT":
            inflows[acc_id]["total"] += amt
            inflows[acc_id]["count"] += 1
            if amt < 50000:
                inflows[acc_id]["small_count"] += 1
        else:
            outflows[acc_id]["total"] += amt
            outflows[acc_id]["count"] += 1

    for acc_id, inf in inflows.items():
        if inf["total"] > 0:
            out_total = outflows[acc_id]["total"]
            # Pass-through detection
            if inf["total"] > 500000 and out_total > 500000:
                ratio = abs(inf["total"] - out_total) / max(inf["total"], out_total)
                if ratio < 0.15:
                    alerts.append({
                        "type": "LAYERING_PASS_THROUGH",
                        "severity": "HIGH",
                        "message": f"Account {get_name(acc_id)} is a pass-through: received INR {inf['total']:,.2f} and sent INR {out_total:,.2f} (difference {ratio*100:.1f}%).",
                    })
            # Structuring detection
            if inf["small_count"] >= 5:
                alerts.append({
                    "type": "STRUCTURING_SMURFING",
                    "severity": "MEDIUM",
                    "message": f"Account {get_name(acc_id)} received {inf['small_count']} small deposits (< INR 50k). Possible smurfing.",
                })

    # 2. Rapid Movement (In and out within 3 days)
    for t_out in txns:
        if t_out.direction != "DEBIT" or not t_out.account_id: continue
        acc_id = str(t_out.account_id)
        # Find recent matching credits into this same account
        for t_in in txns:
            if t_in.direction != "CREDIT" or str(t_in.account_id) != acc_id: continue
            days_diff = (t_out.value_date - t_in.value_date).days
            if 0 <= days_diff <= 3:
                in_amt = float(t_in.amount)
                out_amt = float(t_out.amount)
                if in_amt > 100000 and (out_amt / in_amt) >= 0.8:
                    alerts.append({
                        "type": "RAPID_MOVEMENT",
                        "severity": "HIGH",
                        "message": f"Rapid movement in {get_name(acc_id)}: INR {out_amt:,.2f} sent out {days_diff} days after receiving INR {in_amt:,.2f}.",
                    })
                    break # only flag once per outgoing txn

    # 3. Circular Flow (A -> B and B -> A)
    edges = set()
    for t in txns:
        if t.account_id and t.counterparty_entity_id:
            edges.add((str(t.account_id), str(t.counterparty_entity_id)))
            
    flagged_cycles = set()
    for src, dst in edges:
        if (dst, src) in edges:
            pair = tuple(sorted([src, dst]))
            if pair not in flagged_cycles:
                flagged_cycles.add(pair)
                alerts.append({
                    "type": "CIRCULAR_FLOW",
                    "severity": "HIGH",
                    "message": f"Circular flow detected between {get_name(src)} and {get_name(dst)}. Funds are round-tripping.",
                })

    # Sort by severity
    sev_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
    alerts.sort(key=lambda x: sev_order.get(x["severity"], 4))
    
    return alerts