import uuid
from datetime import datetime
from app.extensions import db

FEEDBACK_TYPES = [
    "great_job",        # 🌟 Great job!
    "well_done",        # 👍 Well done
    "good_effort",      # 💪 Good effort
    "needs_followup",   # 🔔 Please follow up promptly
    "improve_notes",    # 📝 Please add more detail to notes
    "improve_coverage", # 📍 Need better area coverage
    "pricing_support",  # 💰 Will arrange pricing support
    "escalating",       # ⚡ Escalating this to management
    "custom",           # ✍️ Custom message
]

FEEDBACK_LABELS = {
    "great_job":        "🌟 Great job!",
    "well_done":        "👍 Well done",
    "good_effort":      "💪 Good effort",
    "needs_followup":   "🔔 Please follow up promptly",
    "improve_notes":    "📝 Please add more detail to notes",
    "improve_coverage": "📍 Need better area coverage",
    "pricing_support":  "💰 Will arrange pricing support",
    "escalating":       "⚡ Escalating to management",
    "custom":           "✍️ Custom message",
}

class Feedback(db.Model):
    __tablename__ = "feedback"

    id          = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id    = db.Column(db.String(36), db.ForeignKey("visits.id"), nullable=False)
    staff_id    = db.Column(db.String(36), db.ForeignKey("staff.id"),  nullable=False)
    from_id     = db.Column(db.String(36), db.ForeignKey("staff.id"),  nullable=True)
    ftype       = db.Column(db.String(50), nullable=False)
    message     = db.Column(db.Text,       nullable=True)
    is_read     = db.Column(db.Boolean,    default=False)
    created_at  = db.Column(db.DateTime,   default=datetime.utcnow)

    # Relationships
    staff    = db.relationship("Staff", foreign_keys=[staff_id])
    sender   = db.relationship("Staff", foreign_keys=[from_id])

    def to_dict(self):
        return {
            "id":         self.id,
            "visit_id":   self.visit_id,
            "staff_id":   self.staff_id,
            "staff_name": self.staff.name  if self.staff  else None,
            "from_id":    self.from_id,
            "from_name":  self.sender.name if self.sender else None,
            "ftype":      self.ftype,
            "label":      FEEDBACK_LABELS.get(self.ftype, self.ftype),
            "message":    self.message,
            "is_read":    self.is_read,
            "created_at": self.created_at.isoformat(),
        }
