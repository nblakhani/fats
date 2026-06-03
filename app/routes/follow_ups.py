from flask import Blueprint, request, jsonify
from datetime import date, timedelta
from app.extensions import db
from app.models.follow_up import FollowUp

bp = Blueprint("follow_ups", __name__)

@bp.route("/", methods=["GET"])
def list_follow_ups():
    """GET /api/follow-ups
    Filters: ?staff_id= &status= &from= &to= &overdue=true
    """
    staff_id = request.args.get("staff_id")
    status   = request.args.get("status")
    from_str = request.args.get("from")
    to_str   = request.args.get("to")

    # Clamp to_str to valid date
    if to_str:
        try:
            from datetime import datetime
            import calendar as cal
            parts = to_str.split('-')
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            last_day = cal.monthrange(y, m)[1]
            if d > last_day:
                to_str = f"{y}-{m:02d}-{last_day:02d}"
        except Exception:
            pass
    overdue  = request.args.get("overdue")

    q = FollowUp.query
    if staff_id:
        q = q.filter_by(assigned_to_id=staff_id)
    if status:
        q = q.filter_by(status=status)
    if overdue == "true":
        q = q.filter(FollowUp.due_date < date.today(),
                     FollowUp.status == "scheduled")
    else:
        if from_str:
            q = q.filter(FollowUp.due_date >= from_str)
        if to_str:
            q = q.filter(FollowUp.due_date <= to_str)

    items = q.order_by(FollowUp.due_date.asc()).all()
    return jsonify([f.to_dict() for f in items])

@bp.route("/calendar", methods=["GET"])
def calendar_view():
    """GET /api/follow-ups/calendar?year=2026&month=5
    Returns follow-ups keyed by date for calendar rendering
    """
    year  = int(request.args.get("year",  date.today().year))
    month = int(request.args.get("month", date.today().month))

    from_date = date(year, month, 1)
    # last day of month
    if month == 12:
        to_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        to_date = date(year, month + 1, 1) - timedelta(days=1)

    items = (FollowUp.query
             .filter(FollowUp.due_date >= from_date,
                     FollowUp.due_date <= to_date)
             .order_by(FollowUp.due_date)
             .all())

    # Group by date string
    result = {}
    for f in items:
        key = f.due_date.isoformat()
        if key not in result:
            result[key] = []
        result[key].append(f.to_dict())
    return jsonify(result)

@bp.route("/upcoming", methods=["GET"])
def upcoming():
    """GET /api/follow-ups/upcoming?days=7
    Returns follow-ups due in next N days
    """
    days = int(request.args.get("days", 7))
    today = date.today()
    until = today + timedelta(days=days)
    items = (FollowUp.query
             .filter(FollowUp.due_date >= today,
                     FollowUp.due_date <= until,
                     FollowUp.status == "scheduled")
             .order_by(FollowUp.due_date, FollowUp.assigned_to_id)
             .all())
    return jsonify([f.to_dict() for f in items])

@bp.route("/<fu_id>", methods=["PATCH"])
def update_follow_up(fu_id):
    """PATCH /api/follow-ups/<id>
    Body: { status, due_date, notes }
    """
    fu = FollowUp.query.get_or_404(fu_id)
    data = request.get_json(force=True)
    for field in ["status", "notes"]:
        if field in data:
            setattr(fu, field, data[field])
    if "due_date" in data:
        from datetime import datetime
        fu.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        fu.status = "rescheduled"
    db.session.commit()
    return jsonify(fu.to_dict())
