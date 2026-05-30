import uuid
from datetime import datetime
from app.extensions import db

class Client(db.Model):
    __tablename__ = "clients"

    id            = db.Column(db.String(36),  primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name  = db.Column(db.String(200), nullable=False)
    industry      = db.Column(db.String(100), nullable=True)
    address       = db.Column(db.Text,        nullable=True)
    city          = db.Column(db.String(100), nullable=True)
    contact_name  = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20),  nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    account_tier  = db.Column(db.String(20),  nullable=True, default="standard")
    # tiers: hot | warm | standard | prospect
    notes         = db.Column(db.Text,        nullable=True)
    rating        = db.Column(db.Integer,      nullable=True)   # 1-5 star client rating
    rating_comment = db.Column(db.Text,       nullable=True)   # payment, repeat orders, etc
    active        = db.Column(db.Boolean,     default=True)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    # Relationships
    visits     = db.relationship("Visit",    back_populates="client", lazy="dynamic")
    follow_ups = db.relationship("FollowUp", back_populates="client", lazy="dynamic")

    def to_dict(self, include_stats=False):
        d = {
            "id":            self.id,
            "company_name":  self.company_name,
            "industry":      self.industry,
            "address":       self.address,
            "city":          self.city,
            "contact_name":  self.contact_name,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "account_tier":  self.account_tier,
            "notes":         self.notes,
            "rating":         self.rating,
            "rating_comment": self.rating_comment,
            "active":        self.active,
            "created_at":    self.created_at.isoformat(),
        }
        if include_stats:
            d["total_visits"]    = self.visits.count()
            d["open_follow_ups"] = self.follow_ups.filter_by(status="scheduled").count()
        return d
