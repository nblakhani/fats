import uuid
from datetime import datetime
from app.extensions import db

class Staff(db.Model):
    __tablename__ = "staff"

    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name       = db.Column(db.String(120), nullable=False)
    phone      = db.Column(db.String(20),  nullable=False, unique=True)
    email      = db.Column(db.String(120), nullable=True,  unique=True)
    role       = db.Column(db.String(50),  nullable=False, default="field_staff")
    # roles: field_staff | manager | admin
    region     = db.Column(db.String(100), nullable=True)
    manager_id = db.Column(db.String(36),  db.ForeignKey("staff.id"), nullable=True)
    lob        = db.Column(db.String(200), nullable=True)  # primary LOB(s) assigned
    rating     = db.Column(db.Integer,      nullable=True)   # 1-5 star performance rating
    rating_comment = db.Column(db.Text,    nullable=True)   # performance notes
    active     = db.Column(db.Boolean,     default=True)
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)

    # Relationships
    visits       = db.relationship("Visit",      back_populates="staff", lazy="dynamic")
    action_items = db.relationship("ActionItem", back_populates="staff", lazy="dynamic")
    follow_ups   = db.relationship("FollowUp",   back_populates="assigned_to", lazy="dynamic")
    reports      = db.relationship("Staff",      foreign_keys=[manager_id])

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "phone":      self.phone,
            "email":      self.email,
            "role":       self.role,
            "region":     self.region,
            "manager_id": self.manager_id,
            "lob":        getattr(self, "lob", None),
            "rating":         self.rating,
            "rating_comment": self.rating_comment,
            "active":     self.active,
            "created_at": self.created_at.isoformat(),
        }
