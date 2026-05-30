import uuid
from datetime import datetime, date
from app.extensions import db

VISIT_TYPES = [
    "Prospecting", "Sales call", "Follow-up", "Service visit",
    "Demo", "Collection", "Delivery", "Complaint", "Other"
]

PRIORITIES = ["High", "Medium", "Low"]

class Visit(db.Model):
    __tablename__ = "visits"

    id                 = db.Column(db.String(36),  primary_key=True, default=lambda: str(uuid.uuid4()))
    staff_id           = db.Column(db.String(36),  db.ForeignKey("staff.id"),   nullable=False)
    client_id          = db.Column(db.String(36),  db.ForeignKey("clients.id"), nullable=False)

    visit_date         = db.Column(db.Date,        nullable=False, default=date.today)
    time_in            = db.Column(db.String(10),  nullable=True)   # stored as "HH:MM"
    time_out           = db.Column(db.String(10),  nullable=True)

    visit_type         = db.Column(db.String(50),  nullable=False, default="Visit")
    rep_met            = db.Column(db.String(200), nullable=True)   # name + designation
    purpose            = db.Column(db.Text,        nullable=True)   # main issue / reason
    prev_visit_summary = db.Column(db.Text,        nullable=True)   # what happened last time
    priority           = db.Column(db.String(20),  nullable=False, default="Medium")
    notes              = db.Column(db.Text,        nullable=True)   # other observations

    gps_lat            = db.Column(db.Numeric(10, 7), nullable=True)
    gps_lng            = db.Column(db.Numeric(10, 7), nullable=True)

    source             = db.Column(db.String(20),  nullable=False, default="text")
    # source: voice | text

    created_at         = db.Column(db.DateTime,   default=datetime.utcnow)

    # Relationships
    staff        = db.relationship("Staff",      back_populates="visits")
    client       = db.relationship("Client",     back_populates="visits")
    action_items = db.relationship("ActionItem", back_populates="visit",
                                   cascade="all, delete-orphan", lazy="dynamic")
    follow_ups   = db.relationship("FollowUp",   back_populates="visit",
                                   cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self, include_related=False):
        d = {
            "id":                 self.id,
            "staff_id":           self.staff_id,
            "staff_name":         self.staff.name if self.staff else None,
            "client_id":          self.client_id,
            "client_name":        self.client.company_name if self.client else None,
            "visit_date":         self.visit_date.isoformat() if self.visit_date else None,
            "time_in":            self.time_in,
            "time_out":           self.time_out,
            "visit_type":         self.visit_type,
            "rep_met":            self.rep_met,
            "purpose":            self.purpose,
            "prev_visit_summary": self.prev_visit_summary,
            "priority":           self.priority,
            "notes":              self.notes,
            "gps_lat":            float(self.gps_lat)  if self.gps_lat  else None,
            "gps_lng":            float(self.gps_lng)  if self.gps_lng  else None,
            "lob":               getattr(self, "lob", None),
            "source":             self.source,
            "created_at":         self.created_at.isoformat(),
        }
        if include_related:
            d["action_items"] = [a.to_dict() for a in self.action_items]
            d["follow_ups"]   = [f.to_dict() for f in self.follow_ups]
        return d
