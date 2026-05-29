import uuid
from datetime import datetime
from app.extensions import db

class Report(db.Model):
    __tablename__ = "reports"

    id               = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_date      = db.Column(db.Date,       nullable=False)
    generated_by     = db.Column(db.String(50), default="scheduler")
    delivery_channel = db.Column(db.String(50), default="api")
    # channel: api | email | whatsapp
    payload          = db.Column(db.Text,       nullable=True)  # JSON snapshot of report
    sent_at          = db.Column(db.DateTime,   nullable=True)
    created_at       = db.Column(db.DateTime,   default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":               self.id,
            "report_date":      self.report_date.isoformat(),
            "generated_by":     self.generated_by,
            "delivery_channel": self.delivery_channel,
            "sent_at":          self.sent_at.isoformat() if self.sent_at else None,
            "created_at":       self.created_at.isoformat(),
        }
