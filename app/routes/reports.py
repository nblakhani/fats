from flask import Blueprint, request, jsonify
from datetime import date
from app.extensions import db
from app.models.report import Report
from app.services.report_builder import build_eod_report, format_text_report

bp = Blueprint("reports", __name__)

@bp.route("/eod", methods=["GET"])
def eod_report():
    """GET /api/reports/eod?date=2026-05-29
    Returns the EOD report as JSON. Date defaults to today.
    """
    date_str = request.args.get("date")
    if date_str:
        from datetime import datetime
        report_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        report_date = date.today()

    report = build_eod_report(report_date)
    return jsonify(report)

@bp.route("/eod/text", methods=["GET"])
def eod_report_text():
    """GET /api/reports/eod/text?date=2026-05-29
    Returns the report as plain text — ready for WhatsApp / email.
    """
    date_str = request.args.get("date")
    if date_str:
        from datetime import datetime
        report_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        report_date = date.today()

    report = build_eod_report(report_date)
    text   = format_text_report(report)
    return text, 200, {"Content-Type": "text/plain; charset=utf-8"}

@bp.route("/history", methods=["GET"])
def report_history():
    """GET /api/reports/history?limit=30
    Returns audit log of all generated reports.
    """
    limit = int(request.args.get("limit", 30))
    reports = (Report.query
               .order_by(Report.report_date.desc())
               .limit(limit)
               .all())
    return jsonify([r.to_dict() for r in reports])

@bp.route("/summary", methods=["GET"])
def weekly_summary():
    """GET /api/reports/summary?days=7
    Quick metrics for the last N days — useful for manager dashboard.
    """
    from datetime import timedelta
    from app.models.visit import Visit
    from app.models.follow_up import FollowUp
    from app.models.action_item import ActionItem

    days  = int(request.args.get("days", 7))
    since = date.today() - timedelta(days=days)

    visits    = Visit.query.filter(Visit.visit_date >= since).all()
    open_fu   = FollowUp.query.filter_by(status="scheduled").count()
    overdue   = FollowUp.query.filter(
                    FollowUp.due_date < date.today(),
                    FollowUp.status == "scheduled").count()
    open_ai   = ActionItem.query.filter(
                    ActionItem.status.in_(["open", "in_progress"])).count()
    help_ai   = ActionItem.query.filter(
                    ActionItem.status.in_(["open", "in_progress"]),
                    ActionItem.help_needed.isnot(None),
                    ActionItem.help_needed != "").count()

    # Visit type breakdown
    type_counts = {}
    for v in visits:
        type_counts[v.visit_type] = type_counts.get(v.visit_type, 0) + 1

    # Staff activity
    staff_counts = {}
    for v in visits:
        name = v.staff.name if v.staff else v.staff_id
        staff_counts[name] = staff_counts.get(name, 0) + 1

    return jsonify({
        "period_days":    days,
        "since":          since.isoformat(),
        "total_visits":   len(visits),
        "open_follow_ups": open_fu,
        "overdue_follow_ups": overdue,
        "open_actions":   open_ai,
        "help_needed":    help_ai,
        "by_type":        type_counts,
        "by_staff":       staff_counts,
    })
