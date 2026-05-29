"""
scheduler.py
Registers the EOD report cron job using APScheduler.
Fires daily at EOD_REPORT_TIME (default 19:00 IST).
"""
import json
import logging
from datetime import date, datetime
from app.extensions import scheduler

logger = logging.getLogger(__name__)


def register_jobs(app):
    time_str = app.config.get("EOD_REPORT_TIME", "19:00")
    hour, minute = [int(x) for x in time_str.split(":")]

    # Remove existing job if re-registering (hot reload)
    if scheduler.get_job("eod_report"):
        scheduler.remove_job("eod_report")

    scheduler.add_job(
        func      = _run_eod_report,
        args      = [app],
        trigger   = "cron",
        hour      = hour,
        minute    = minute,
        id        = "eod_report",
        name      = "EOD Field Report",
        replace_existing = True,
    )
    logger.info(f"EOD report job registered for {hour:02d}:{minute:02d} IST daily")


def _run_eod_report(app):
    """Called by APScheduler at EOD time."""
    with app.app_context():
        from app.services.report_builder import build_eod_report, format_text_report
        from app.models.report import Report
        from app.extensions import db

        try:
            logger.info("Running EOD report job...")
            report_data = build_eod_report(date.today())
            text_report = format_text_report(report_data)

            # Save to reports table
            report = Report(
                report_date      = date.today(),
                generated_by     = "scheduler",
                delivery_channel = "api",
                payload          = json.dumps(report_data),
                sent_at          = datetime.utcnow(),
            )
            db.session.add(report)
            db.session.commit()

            logger.info(f"EOD report saved — {report_data['summary']['total_visits']} visits")

            # Phase 4: send via WhatsApp
            # _send_whatsapp(app, text_report)

        except Exception as e:
            logger.error(f"EOD report job failed: {e}", exc_info=True)
