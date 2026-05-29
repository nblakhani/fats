import uuid
from datetime import datetime
from app.extensions import db

class ActionItem(db.Model):
    __tablename__ = "action_items"

    id          = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id    = db.Column(db.String(36), db.ForeignKey("visits.id"),  nullable=False)
    staff_id    = db.Column(db.String(36), db.ForeignKey("staff.id"),   nullable=False)
    description = db.Column(db.Text,       nullable=False)
    status      = db.Column(db.String(30), nullable=False, default="open")
    # status: open | in_progress | done | cancelled
    help_needed = db.Column(db.Text,       nullable=True)
    due_date    = db.Column(db.Date,       nullable=True)
    resolved_at = db.Column(db.DateTime,   nullable=True)
    created_at  = db.Column(db.DateTime,   default=datetime.utcnow)

    # Relationships
    visit = db.relationship("Visit", back_populates="action_items")
    staff = db.relationship("Staff", back_populates="action_items")

    def to_dict(self):
        return {
            "id":          self.id,
            "visit_id":    self.visit_id,
            "staff_id":    self.staff_id,
            "staff_name":  self.staff.name if self.staff else None,
            "description": self.description,
            "status":      self.status,
            "help_needed": self.help_needed,
            "due_date":    self.due_date.isoformat() if self.due_date else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at":  self.created_at.isoformat(),
        }
