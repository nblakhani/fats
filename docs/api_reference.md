# Field Force API — Quick Reference

Base URL: http://localhost:5000/api

## Health
GET  /api/health

## Staff
GET    /api/staff                     list all active staff
GET    /api/staff/<id>                get one
POST   /api/staff                     create  { name*, phone*, email, role, region, manager_id }
PATCH  /api/staff/<id>                update any field
DELETE /api/staff/<id>                soft-delete (active=false)

## Clients
GET    /api/clients                   ?city= &tier= &q=search
GET    /api/clients/<id>              with visit count + open follow-ups
GET    /api/clients/<id>/visits       full visit history
POST   /api/clients                   { company_name*, industry, address, city, contact_name, contact_phone, account_tier }
PATCH  /api/clients/<id>

## Visits
GET    /api/visits                    ?staff_id= &date= &from= &to= &visit_type= &priority=
GET    /api/visits/today              all today's visits grouped by staff
GET    /api/visits/<id>               full detail with action items + follow-ups
POST   /api/visits                    { staff_id*, client_id|client_name*, visit_type,
                                        visit_date, time_in, time_out, rep_met,
                                        purpose, prev_visit_summary, priority, notes,
                                        gps_lat, gps_lng, source,
                                        action_items: ["...","..."],
                                        follow_up_date, help_needed }
PATCH  /api/visits/<id>
DELETE /api/visits/<id>

## Action Items
GET    /api/action-items              ?staff_id= &status= &due_before= &has_help=true
GET    /api/action-items/open         ?staff_id=
PATCH  /api/action-items/<id>         { status, help_needed, due_date }
                                      status=done auto-sets resolved_at

## Follow-ups
GET    /api/follow-ups                ?staff_id= &status= &from= &to= &overdue=true
GET    /api/follow-ups/upcoming       ?days=7   (default 7-day window)
GET    /api/follow-ups/calendar       ?year=2026&month=5  (returns dict keyed by date)
PATCH  /api/follow-ups/<id>           { status, due_date (reschedules), notes }

## Reports
GET    /api/reports/eod               ?date=2026-05-29  (JSON — full EOD report)
GET    /api/reports/eod/text          ?date=  (plain text — WhatsApp/email ready)
GET    /api/reports/summary           ?days=7  (aggregated metrics)
GET    /api/reports/history           ?limit=30

## Status values
Visit types:  Prospecting | Sales call | Follow-up | Service visit | Demo | Collection | Delivery | Complaint | Other
Priorities:   High | Medium | Low
Action status: open | in_progress | done | cancelled
Follow-up status: scheduled | completed | rescheduled | cancelled
Staff roles:  field_staff | manager | admin
Account tiers: hot | warm | standard | prospect
