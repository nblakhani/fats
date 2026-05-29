from flask import Blueprint, request, jsonify
from datetime import date
from app.extensions import db
from app.models.action_item import ActionItem
from datetime import datetime

bp = Blueprint("action_items", __name__)

@bp.route("/", methods=["GET"])
def list_action_items():
    """GET /api/action-items
    Filters: ?staff_id= &status= &due_before= &has_help=true
    """
    staff_id   = request.args.get("staff_id")
    status     = request.args.get("status")
    due_before = request.args.get("due_before")
    has_help   = request.args.get("has_help")

    q = ActionItem.query
    if staff_id:
        q = q.filter_by(staff_id=staff_id)
    if status:
        q = q.filter_by(status=status)
    if due_before:
        q = q.filter(ActionItem.due_date <= due_before)
    if has_help == "true":
        q = q.filter(ActionItem.help_needed.isnot(None),
                     ActionItem.help_needed != "")

    items = q.order_by(ActionItem.due_date.asc()).all()
    return jsonify([i.to_dict() for i in items])

@bp.route("/open", methods=["GET"])
def open_items():
    """GET /api/action-items/open  — all open items, optionally ?staff_id="""
    staff_id = request.args.get("staff_id")
    q = ActionItem.query.filter(ActionItem.status.in_(["open", "in_progress"]))
    if staff_id:
        q = q.filter_by(staff_id=staff_id)
    items = q.order_by(ActionItem.due_date.asc()).all()
    return jsonify([i.to_dict() for i in items])

@bp.route("/<item_id>", methods=["PATCH"])
def update_action_item(item_id):
    """PATCH /api/action-items/<id>
    Body: { status, help_needed, due_date }
    status=done auto-sets resolved_at
    """
    item = ActionItem.query.get_or_404(item_id)
    data = request.get_json(force=True)
    if "status" in data:
        item.status = data["status"]
        if data["status"] == "done" and not item.resolved_at:
            item.resolved_at = datetime.utcnow()
    if "help_needed" in data:
        item.help_needed = data["help_needed"]
    if "due_date" in data:
        item.due_date = data["due_date"]
    db.session.commit()
    return jsonify(item.to_dict())
