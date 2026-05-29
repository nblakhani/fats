"""
report_builder.py
Builds the EOD report data structure for a given date.
Used by both the /api/reports endpoint and the scheduler cron job.
"""
from datetime import date
from app.models.visit import Visit
from app.models.action_item import ActionItem
from app.models.follow_up import FollowUp
from app.models.staff import Staff


def build_eod_report(report_date: date = None) -> dict:
    if report_date is None:
        report_date = date.today()

    # All visits on this date
    visits = (Visit.query
              .filter_by(visit_date=report_date)
              .order_by(Visit.staff_id, Visit.time_in)
              .all())

    # All open action items (across all time — not just today)
    open_actions = (ActionItem.query
                    .filter(ActionItem.status.in_(["open", "in_progress"]))
                    .order_by(ActionItem.due_date)
                    .all())

    # Follow-ups due today or overdue
    due_follow_ups = (FollowUp.query
                      .filter(FollowUp.due_date <= report_date,
                              FollowUp.status == "scheduled")
                      .order_by(FollowUp.due_date)
                      .all())

    # Group visits by staff
    staff_sections = {}
    for v in visits:
        sid = v.staff_id
        if sid not in staff_sections:
            staff_sections[sid] = {
                "staff_id":   sid,
                "staff_name": v.staff.name if v.staff else sid,
                "region":     v.staff.region if v.staff else None,
                "visits":     [],
            }
        staff_sections[sid]["visits"].append({
            "visit_id":          v.id,
            "client":            v.client.company_name if v.client else "—",
            "location":          v.client.city if v.client else None,
            "rep_met":           v.rep_met,
            "time_in":           v.time_in,
            "time_out":          v.time_out,
            "visit_type":        v.visit_type,
            "purpose":           v.purpose,
            "prev_visit_summary": v.prev_visit_summary,
            "priority":          v.priority,
            "notes":             v.notes,
            "gps":               {"lat": float(v.gps_lat), "lng": float(v.gps_lng)}
                                 if v.gps_lat else None,
            "action_items":      [a.to_dict() for a in v.action_items],
            "follow_ups":        [f.to_dict() for f in v.follow_ups],
        })

    # Summary metrics
    total_visits     = len(visits)
    active_staff     = len(staff_sections)
    new_prospects    = sum(1 for v in visits if v.visit_type == "Prospecting")
    help_needed      = [a.to_dict() for a in open_actions if a.help_needed]
    overdue_fu       = [f.to_dict() for f in due_follow_ups
                        if f.due_date < report_date]
    due_today_fu     = [f.to_dict() for f in due_follow_ups
                        if f.due_date == report_date]

    return {
        "report_date":    report_date.isoformat(),
        "summary": {
            "total_visits":    total_visits,
            "active_staff":    active_staff,
            "new_prospects":   new_prospects,
            "open_actions":    len(open_actions),
            "due_today":       len(due_today_fu),
            "overdue":         len(overdue_fu),
            "help_needed":     len(help_needed),
        },
        "by_staff":          list(staff_sections.values()),
        "follow_ups_due_today": due_today_fu,
        "overdue_follow_ups":   overdue_fu,
        "help_needed":          help_needed,
        "all_open_actions":     [a.to_dict() for a in open_actions],
    }


def format_text_report(report: dict) -> str:
    """Renders the report dict as a plain-text string for WhatsApp/email."""
    lines = []
    s = report["summary"]
    d = report["report_date"]

    lines.append(f"FIELD FORCE EOD REPORT — {d}")
    lines.append("=" * 50)
    lines.append(
        f"Visits: {s['total_visits']}  |  Staff active: {s['active_staff']}  |  "
        f"Prospects: {s['new_prospects']}  |  Help needed: {s['help_needed']}"
    )
    lines.append("")

    for section in report["by_staff"]:
        lines.append(f"► {section['staff_name'].upper()}"
                     + (f"  [{section['region']}]" if section["region"] else ""))
        for v in section["visits"]:
            time_str = ""
            if v["time_in"]:
                time_str = f"{v['time_in']}"
                if v["time_out"]:
                    time_str += f"–{v['time_out']}"
            lines.append(
                f"  {time_str:12}  {v['client']}  [{v['visit_type']}]"
                + (f"  ({v['priority']} priority)" if v["priority"] != "Medium" else "")
            )
            if v["rep_met"]:
                lines.append(f"               Rep met: {v['rep_met']}")
            if v["purpose"]:
                lines.append(f"               Purpose: {v['purpose']}")
            if v["action_items"]:
                for ai in v["action_items"]:
                    lines.append(f"               ✓ Action: {ai['description']}")
            if v["follow_ups"]:
                for fu in v["follow_ups"]:
                    lines.append(f"               → Follow-up: {fu['due_date']}")
        lines.append("")

    if report["follow_ups_due_today"]:
        lines.append("FOLLOW-UPS DUE TODAY")
        lines.append("-" * 40)
        for fu in report["follow_ups_due_today"]:
            lines.append(f"  {fu['client_name']:30}  {fu['assigned_to']}")
        lines.append("")

    if report["overdue_follow_ups"]:
        lines.append("OVERDUE FOLLOW-UPS  ⚠")
        lines.append("-" * 40)
        for fu in report["overdue_follow_ups"]:
            lines.append(
                f"  {fu['client_name']:30}  {fu['assigned_to']}  (due {fu['due_date']})"
            )
        lines.append("")

    if report["help_needed"]:
        lines.append("HELP NEEDED FROM MANAGEMENT")
        lines.append("-" * 40)
        for ai in report["help_needed"]:
            lines.append(f"  {ai['staff_name']:20}  {ai['help_needed']}")

    return "\n".join(lines)
