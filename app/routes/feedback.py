from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.feedback import Feedback, FEEDBACK_LABELS
from app.models.staff import Staff
from app.models.visit import Visit

bp = Blueprint("feedback", __name__)

@bp.route("/", methods=["POST"])
def send_feedback():
    """POST /api/feedback/
    Body: { visit_id, staff_id, from_id, ftype, message (optional) }
    """
    data = request.get_json(force=True)

    required = ["staff_id", "ftype"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"{f} is required"}), 400

    # Validate visit if provided
    visit_id = data.get("visit_id") or None
    if visit_id:
        visit = Visit.query.get(visit_id)
        if not visit:
            return jsonify({"error": "visit not found"}), 404

    fb = Feedback(
        visit_id = visit_id,
        staff_id = data["staff_id"],
        from_id  = data["from_id"],
        ftype    = data["ftype"],
        message  = data.get("message") or None,
        is_read  = False,
    )
    db.session.add(fb)
    db.session.commit()
    return jsonify(fb.to_dict()), 201

@bp.route("/staff/<staff_id>/", methods=["GET"])
def staff_feedback(staff_id):
    """GET /api/feedback/staff/<id>/
    Returns all feedback for a staff member, newest first.
    ?unread=true for unread only
    """
    unread = request.args.get("unread") == "true"
    q = Feedback.query.filter_by(staff_id=staff_id)
    if unread:
        q = q.filter_by(is_read=False)
    items = q.order_by(Feedback.created_at.desc()).all()
    return jsonify([f.to_dict() for f in items])

@bp.route("/staff/<staff_id>/unread-count/", methods=["GET"])
def unread_count(staff_id):
    """GET /api/feedback/staff/<id>/unread-count/"""
    count = Feedback.query.filter_by(staff_id=staff_id, is_read=False).count()
    return jsonify({"count": count})

@bp.route("/<fb_id>/read/", methods=["PATCH"])
def mark_read(fb_id):
    """PATCH /api/feedback/<id>/read/  — mark as read"""
    fb = Feedback.query.get_or_404(fb_id)
    fb.is_read = True
    db.session.commit()
    return jsonify(fb.to_dict())

@bp.route("/staff/<staff_id>/read-all/", methods=["PATCH"])
def mark_all_read(staff_id):
    """PATCH /api/feedback/staff/<id>/read-all/"""
    Feedback.query.filter_by(staff_id=staff_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"message": "all marked read"})

@bp.route("/types/", methods=["GET"])
def feedback_types():
    """GET /api/feedback/types/  — list all feedback types and labels"""
    return jsonify([{"ftype": k, "label": v} for k, v in FEEDBACK_LABELS.items()])

@bp.route("/visit/<visit_id>/", methods=["GET"])
def visit_feedback(visit_id):
    """GET /api/feedback/visit/<id>/  — all feedback on a specific visit"""
    items = Feedback.query.filter_by(visit_id=visit_id).order_by(Feedback.created_at.desc()).all()
    return jsonify([f.to_dict() for f in items])
