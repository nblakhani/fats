from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.staff import Staff

bp = Blueprint("staff", __name__)

@bp.route("/", methods=["GET"])
def list_staff():
    """GET /api/staff  — list all active staff, optional ?region="""
    region = request.args.get("region")
    q = Staff.query.filter_by(active=True)
    if region:
        q = q.filter_by(region=region)
    return jsonify([s.to_dict() for s in q.order_by(Staff.name).all()])

@bp.route("/<staff_id>", methods=["GET"])
def get_staff(staff_id):
    """GET /api/staff/<id>"""
    s = Staff.query.get_or_404(staff_id)
    return jsonify(s.to_dict())

@bp.route("/", methods=["POST"])
def create_staff():
    """POST /api/staff
    Body: { name, phone, email, role, region, manager_id }
    """
    data = request.get_json(force=True)
    if not data.get("name") or not data.get("phone"):
        return jsonify({"error": "name and phone are required"}), 400

    s = Staff(
        name       = data["name"],
        phone      = data["phone"],
        email      = data.get("email"),
        role       = data.get("role", "field_staff"),
        region     = data.get("region"),
        manager_id = data.get("manager_id"),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@bp.route("/<staff_id>", methods=["PATCH"])
def update_staff(staff_id):
    """PATCH /api/staff/<id>  — partial update"""
    s = Staff.query.get_or_404(staff_id)
    data = request.get_json(force=True)
    for field in ["name", "phone", "email", "role", "region", "manager_id", "active"]:
        if field in data:
            setattr(s, field, data[field])
    db.session.commit()
    return jsonify(s.to_dict())

@bp.route("/<staff_id>", methods=["DELETE"])
def deactivate_staff(staff_id):
    """DELETE /api/staff/<id>  — soft delete (sets active=false)"""
    s = Staff.query.get_or_404(staff_id)
    s.active = False
    db.session.commit()
    return jsonify({"message": "staff deactivated"})
