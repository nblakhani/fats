from flask import Blueprint, request, jsonify
from datetime import date, datetime
from app.extensions import db
from app.models.visit import Visit
from app.models.client import Client
from app.models.staff import Staff
from app.models.action_item import ActionItem
from app.models.follow_up import FollowUp

bp = Blueprint("visits", __name__)

def parse_date(val):
    """Safely parse a date string to a date object."""
    if not val:
        return None
    if isinstance(val, date):
        return val
    try:
        return datetime.strptime(str(val).strip(), "%Y-%m-%d").date()
    except Exception:
        return None

@bp.route("/", methods=["GET"])
def list_visits():
    staff_id   = request.args.get("staff_id")
    date_str   = request.args.get("date")
    from_str   = request.args.get("from")
    to_str     = request.args.get("to")

    # Clamp to_str to valid date (e.g. June 31 → June 30)
    if to_str:
        try:
            from datetime import datetime, date
            parts = to_str.split('-')
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            import calendar
            last_day = calendar.monthrange(y, m)[1]
            if d > last_day:
                to_str = f"{y}-{m:02d}-{last_day:02d}"
        except Exception:
            pass
    visit_type = request.args.get("visit_type")
    priority   = request.args.get("priority")

    q = Visit.query
    if staff_id:   q = q.filter_by(staff_id=staff_id)
    if date_str:   q = q.filter_by(visit_date=date_str)
    if from_str:   q = q.filter(Visit.visit_date >= from_str)
    if to_str:     q = q.filter(Visit.visit_date <= to_str)
    if visit_type: q = q.filter_by(visit_type=visit_type)
    if priority:   q = q.filter_by(priority=priority)
    lob = request.args.get('lob')
    if lob:        q = q.filter_by(lob=lob)

    visits = q.order_by(Visit.visit_date.desc(), Visit.time_in).all()
    return jsonify([v.to_dict() for v in visits])

@bp.route("/<visit_id>", methods=["GET"])
def get_visit(visit_id):
    v = Visit.query.get_or_404(visit_id)
    return jsonify(v.to_dict(include_related=True))

@bp.route("/", methods=["POST"])
def create_visit():
    data = request.get_json(force=True)

    # Resolve staff
    staff_id = data.get("staff_id")
    if not staff_id:
        return jsonify({"error": "staff_id is required"}), 400
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"error": "staff not found"}), 404

    # Resolve client
    client_id = data.get("client_id")
    if not client_id:
        client_name = (data.get("client_name") or "").strip()
        if not client_name:
            return jsonify({"error": "client_id or client_name required"}), 400
        client = Client.query.filter(
            Client.company_name.ilike(client_name)
        ).first()
        if not client:
            client = Client(
                company_name = client_name,
                city         = data.get("location"),
            )
            db.session.add(client)
            db.session.flush()
        client_id = client.id

    # Parse dates safely
    visit_date  = parse_date(data.get("visit_date")) or date.today()
    follow_date = parse_date(data.get("follow_up_date"))
    action_due  = follow_date or parse_date(data.get("due_date"))

    visit = Visit(
        staff_id           = staff_id,
        client_id          = client_id,
        visit_date         = visit_date,
        time_in            = data.get("time_in") or None,
        time_out           = data.get("time_out") or None,
        visit_type         = data.get("visit_type", "Visit"),
        rep_met            = data.get("rep_met") or None,
        purpose            = data.get("purpose") or None,
        prev_visit_summary = data.get("prev_visit_summary") or None,
        priority           = data.get("priority", "Medium"),
        notes              = data.get("notes") or None,
        gps_lat            = data.get("gps_lat") or None,
        gps_lng            = data.get("gps_lng") or None,
        source             = data.get("source", "text"),
        lob                = data.get("lob") or None,
    )
    db.session.add(visit)
    db.session.flush()

    # Action items
    for item_text in (data.get("action_items") or []):
        if str(item_text).strip():
            ai = ActionItem(
                visit_id    = visit.id,
                staff_id    = staff_id,
                description = str(item_text).strip(),
                due_date    = action_due,
                help_needed = data.get("help_needed") or None,
            )
            db.session.add(ai)

    # Follow-up
    if follow_date:
        fu = FollowUp(
            visit_id       = visit.id,
            client_id      = client_id,
            assigned_to_id = staff_id,
            due_date       = follow_date,
            notes          = data.get("follow_up_notes") or "",
            status         = "scheduled",
        )
        db.session.add(fu)

    db.session.commit()

    # Auto-complete any open follow-ups for this client+staff on or before visit date
    try:
        from app.models.follow_up import FollowUp
        open_fus = FollowUp.query.filter(
            FollowUp.client_id      == client_id,
            FollowUp.assigned_to_id == staff_id,
            FollowUp.status         == 'scheduled',
            FollowUp.due_date       <= visit_date
        ).all()
        for fu in open_fus:
            fu.status = 'completed'
        if open_fus:
            db.session.commit()
    except Exception:
        pass  # non-critical

    return jsonify(visit.to_dict(include_related=True)), 201

@bp.route("/<visit_id>", methods=["PATCH"])
def update_visit(visit_id):
    v = Visit.query.get_or_404(visit_id)
    data = request.get_json(force=True)
    fields = ["time_in", "time_out", "visit_type", "rep_met", "purpose",
              "prev_visit_summary", "priority", "notes", "gps_lat", "gps_lng"]
    for f in fields:
        if f in data:
            setattr(v, f, data[f])
    db.session.commit()
    return jsonify(v.to_dict(include_related=True))

@bp.route("/<visit_id>", methods=["DELETE"])
def delete_visit(visit_id):
    v = Visit.query.get_or_404(visit_id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({"message": "visit deleted"})

@bp.route("/today", methods=["GET"])
def today_visits():
    visits = (Visit.query
              .filter_by(visit_date=date.today())
              .order_by(Visit.staff_id, Visit.time_in)
              .all())
    result = {}
    for v in visits:
        sid = v.staff_id
        if sid not in result:
            result[sid] = {
                "staff_id":   sid,
                "staff_name": v.staff.name if v.staff else sid,
                "visits":     [],
            }
        result[sid]["visits"].append(v.to_dict())
    return jsonify(list(result.values()))
