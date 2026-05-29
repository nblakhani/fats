import uuid
from datetime import datetime
from app.extensions import db

class FollowUp(db.Model):
    __tablename__ = "follow_ups"

    id             = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id       = db.Column(db.String(36), db.ForeignKey("visits.id"),  nullable=False)
    client_id      = db.Column(db.String(36), db.ForeignKey("clients.id"), nullable=False)
    assigned_to_id = db.Column(db.String(36), db.ForeignKey("staff.id"),   nullable=False)
    due_date       = db.Column(db.Date,       nullable=False)
    notes          = db.Column(db.Text,       nullable=True)
    status         = db.Column(db.String(30), nullable=False, default="scheduled")
    # status: scheduled | completed | rescheduled | cancelled
    created_at     = db.Column(db.DateTime,   default=datetime.utcnow)

    # Relationships
    visit       = db.relationship("Visit",  back_populates="follow_ups")
    client      = db.relationship("Client", back_populates="follow_ups")
    assigned_to = db.relationship("Staff",  back_populates="follow_ups",
                                  foreign_keys=[assigned_to_id])

    def to_dict(self):
        return {
            "id":             self.id,
            "visit_id":       self.visit_id,
            "client_id":      self.client_id,
            "client_name":    self.client.company_name if self.client else None,
            "assigned_to_id": self.assigned_to_id,
            "assigned_to":    self.assigned_to.name if self.assigned_to else None,
            "due_date":       self.due_date.isoformat(),
            "notes":          self.notes,
            "status":         self.status,
            "created_at":     self.created_at.isoformat(),
        }
