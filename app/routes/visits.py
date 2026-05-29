from flask import Blueprint, request, jsonify
from datetime import date
from app.extensions import db
from app.models.visit import Visit
from app.models.client import Client
from app.models.staff import Staff
from app.models.action_item import ActionItem
from app.models.follow_up import FollowUp

bp = Blueprint("visits", __name__)

@bp.route("/", methods=["GET"])
def list_visits():
    """GET /api/visits
    Filters: ?staff_id= &date= &from= &to= &visit_type= &priority=
    """
    staff_id   = request.args.get("staff_id")
    date_str   = request.args.get("date")
    from_str   = request.args.get("from")
    to_str     = request.args.get("to")
    visit_type = request.args.get("visit_type")
    priority   = request.args.get("priority")

    q = Visit.query
    if staff_id:
        q = q.filter_by(staff_id=staff_id)
    if date_str:
        q = q.filter_by(visit_date=date_str)
    if from_str:
        q = q.filter(Visit.visit_date >= from_str)
    if to_str:
        q = q.filter(Visit.visit_date <= to_str)
    if visit_type:
        q = q.filter_by(visit_type=visit_type)
    if priority:
        q = q.filter_by(priority=priority)

    visits = q.order_by(Visit.visit_date.desc(), Visit.time_in).all()
    return jsonify([v.to_dict() for v in visits])

@bp.route("/<visit_id>", methods=["GET"])
def get_visit(visit_id):
    """GET /api/visits/<id>  — full detail with action items and follow-ups"""
    v = Visit.query.get_or_404(visit_id)
    return jsonify(v.to_dict(include_related=True))

@bp.route("/", methods=["POST"])
def create_visit():
    """POST /api/visits
    Required: staff_id, client_id (or client_name for auto-create), visit_type
    Optional: visit_date, time_in, time_out, rep_met, purpose, prev_visit_summary,
              priority, notes, gps_lat, gps_lng, source,
              action_items (list of strings),
              follow_up_date (string YYYY-MM-DD)
    """
    data = request.get_json(force=True)

    # Resolve staff
    staff_id = data.get("staff_id")
    if not staff_id:
        return jsonify({"error": "staff_id is required"}), 400
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"error": "staff not found"}), 404

    # Resolve client — accept client_id or auto-create by name
    client_id = data.get("client_id")
    if not client_id:
        client_name = data.get("client_name", "").strip()
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

    # Parse visit date
    visit_date = date.today()
    if data.get("visit_date"):
        try:
            from datetime import datetime
            visit_date = datetime.strptime(data["visit_date"], "%Y-%m-%d").date()
        except ValueError:
            pass

    visit = Visit(
        staff_id           = staff_id,
        client_id          = client_id,
        visit_date         = visit_date,
        time_in            = data.get("time_in"),
        time_out           = data.get("time_out"),
        visit_type         = data.get("visit_type", "Visit"),
        rep_met            = data.get("rep_met"),
        purpose            = data.get("purpose"),
        prev_visit_summary = data.get("prev_visit_summary"),
        priority           = data.get("priority", "Medium"),
        notes              = data.get("notes"),
        gps_lat            = data.get("gps_lat"),
        gps_lng            = data.get("gps_lng"),
        source             = data.get("source", "text"),
    )
    db.session.add(visit)
    db.session.flush()  # get visit.id before committing

    # Auto-create action items if provided as list
    for item_text in data.get("action_items", []):
        if item_text.strip():
            ai = ActionItem(
                visit_id    = visit.id,
                staff_id    = staff_id,
                description = item_text.strip(),
                due_date    = data.get("follow_up_date"),
                help_needed = data.get("help_needed"),
            )
            db.session.add(ai)

    # Auto-create follow-up if date provided
    if data.get("follow_up_date"):
        fu = FollowUp(
            visit_id       = visit.id,
            client_id      = client_id,
            assigned_to_id = staff_id,
            due_date       = data["follow_up_date"],
            notes          = data.get("follow_up_notes", ""),
            status         = "scheduled",
        )
        db.session.add(fu)

    db.session.commit()
    return jsonify(visit.to_dict(include_related=True)), 201

@bp.route("/<visit_id>", methods=["PATCH"])
def update_visit(visit_id):
    """PATCH /api/visits/<id>  — edit any field"""
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
    """GET /api/visits/today  — all visits logged today, grouped by staff"""
    visits = (Visit.query
              .filter_by(visit_date=date.today())
              .order_by(Visit.staff_id, Visit.time_in)
              .all())
    # Group by staff
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
