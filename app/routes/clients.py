from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.client import Client

bp = Blueprint("clients", __name__)

@bp.route("/", methods=["GET"])
def list_clients():
    """GET /api/clients  — ?city= ?tier= ?q=search"""
    city  = request.args.get("city")
    tier  = request.args.get("tier")
    query = request.args.get("q", "").strip()

    q = Client.query.filter_by(active=True)
    if city:
        q = q.filter_by(city=city)
    if tier:
        q = q.filter_by(account_tier=tier)
    if query:
        q = q.filter(Client.company_name.ilike(f"%{query}%"))

    clients = q.order_by(Client.company_name).all()
    return jsonify([c.to_dict() for c in clients])

@bp.route("/<client_id>", methods=["GET"])
def get_client(client_id):
    """GET /api/clients/<id>  — include visit count and open follow-ups"""
    c = Client.query.get_or_404(client_id)
    return jsonify(c.to_dict(include_stats=True))

@bp.route("/", methods=["POST"])
def create_client():
    """POST /api/clients
    Body: { company_name, industry, address, city, contact_name,
            contact_phone, contact_email, account_tier, notes }
    """
    data = request.get_json(force=True)
    if not data.get("company_name"):
        return jsonify({"error": "company_name is required"}), 400

    c = Client(
        company_name  = data["company_name"],
        industry      = data.get("industry"),
        address       = data.get("address"),
        city          = data.get("city"),
        contact_name  = data.get("contact_name"),
        contact_phone = data.get("contact_phone"),
        contact_email = data.get("contact_email"),
        account_tier  = data.get("account_tier", "standard"),
        notes         = data.get("notes"),
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201

@bp.route("/<client_id>", methods=["PATCH"])
def update_client(client_id):
    c = Client.query.get_or_404(client_id)
    data = request.get_json(force=True)
    for field in ["company_name", "industry", "address", "city",
                  "contact_name", "contact_phone", "contact_email",
                  "account_tier", "notes", "active"]:
        if field in data:
            setattr(c, field, data[field])
    db.session.commit()
    return jsonify(c.to_dict())

@bp.route("/<client_id>/visits", methods=["GET"])
def client_visits(client_id):
    """GET /api/clients/<id>/visits  — full visit history for a client"""
    from app.models.visit import Visit
    Client.query.get_or_404(client_id)
    visits = (Visit.query
              .filter_by(client_id=client_id)
              .order_by(Visit.visit_date.desc())
              .all())
    return jsonify([v.to_dict() for v in visits])
