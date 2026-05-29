"""
seed_apex.py — Apex Corporation realistic seed data
Based on apexcorporation.net — real clients, products, staff names
Run: python seed_apex.py  (clears existing data first)
"""
import os
os.environ.setdefault("FLASK_ENV", "development")

from app import create_app
from app.extensions import db
from app.models.staff import Staff
from app.models.client import Client
from app.models.visit import Visit
from app.models.action_item import ActionItem
from app.models.follow_up import FollowUp
from datetime import date, timedelta

app = create_app()

with app.app_context():
    # Clear existing
    FollowUp.query.delete()
    ActionItem.query.delete()
    Visit.query.delete()
    Client.query.delete()
    Staff.query.delete()
    db.session.commit()

    # ── STAFF (from leadership page) ──────────────────────────
    mgr1 = Staff(name="Gian Taneja",        phone="9835547533", email="gian@apexcorporation.net",
                 role="manager", region="Jamshedpur")
    mgr2 = Staff(name="V.N. Tiwary",        phone="9304003154", email="vn.tiwary@apexcorporation.net",
                 role="manager", region="Ranchi")
    db.session.add_all([mgr1, mgr2])
    db.session.flush()

    s1 = Staff(name="Bhargav Vatsyayan",    phone="9835100001", email="bhargav@apexcorporation.net",
               role="field_staff", region="Jamshedpur", manager_id=mgr1.id)
    s2 = Staff(name="R.B. Prasad",          phone="9835100002", email="rb.prasad@apexcorporation.net",
               role="field_staff", region="Jamshedpur", manager_id=mgr1.id)
    s3 = Staff(name="Arjun Prasad",         phone="9835100003", email="arjun@apexcorporation.net",
               role="field_staff", region="Jamshedpur", manager_id=mgr1.id)
    s4 = Staff(name="Ajay Kumar Pandey",    phone="9835100004", email="ajay@apexcorporation.net",
               role="field_staff", region="Ranchi", manager_id=mgr2.id)
    s5 = Staff(name="Sumit Choubey",        phone="9835100005", email="sumit@apexcorporation.net",
               role="field_staff", region="Ranchi", manager_id=mgr2.id)
    s6 = Staff(name="Rajeev Kumar Sharma",  phone="9835100006", email="rajeev@apexcorporation.net",
               role="field_staff", region="Jamshedpur", manager_id=mgr1.id)
    db.session.add_all([s1, s2, s3, s4, s5, s6])
    db.session.flush()

    # ── CLIENTS (real clients from website) ──────────────────
    clients = [
        Client(company_name="Tata Steel Ltd",
               industry="Steel Manufacturing", city="Bistupur, Jamshedpur",
               contact_name="Suresh Nair", contact_phone="9431100001",
               account_tier="hot", notes="Atlas Copco compressors + Timken bearings. Key account."),
        Client(company_name="Tata Motors Ltd",
               industry="Automotive", city="Telco, Jamshedpur",
               contact_name="Rajiv Mehta", contact_phone="9431100002",
               account_tier="hot", notes="Material handling + motors. Annual AMC due."),
        Client(company_name="Tata Steel Long Products",
               industry="Steel Manufacturing", city="Gamharia, Jamshedpur",
               contact_name="P.K. Singh", contact_phone="9431100003",
               account_tier="hot", notes="Mining equipment — Epiroc rock drills."),
        Client(company_name="Tata Cummins Ltd",
               industry="Engineering", city="Telco, Jamshedpur",
               contact_name="Arun Verma", contact_phone="9431100004",
               account_tier="warm", notes="Canon photocopiers — 12 units. Service contract."),
        Client(company_name="UCIL (Uranium Corp of India)",
               industry="Mining", city="Jadugora, Jharkhand",
               contact_name="D.K. Mishra", contact_phone="9431100005",
               account_tier="hot", notes="Epiroc underground mining equipment. Critical account."),
        Client(company_name="Rungta Mines Ltd",
               industry="Mining", city="Barbil, Jharkhand",
               contact_name="Sunil Rungta", contact_phone="9431100006",
               account_tier="warm", notes="Atlas Copco portable compressors + drilling."),
        Client(company_name="BMW Industries Ltd",
               industry="Steel", city="Gamharia, Jamshedpur",
               contact_name="Ravi Kumar", contact_phone="9431100007",
               account_tier="warm", notes="Marathon motors + industrial fans."),
        Client(company_name="Caparo Engineering India",
               industry="Auto Components", city="Adityapur, Jamshedpur",
               contact_name="Manoj Sharma", contact_phone="9431100008",
               account_tier="standard", notes="Dell laptops + Canon printers."),
        Client(company_name="Larsen & Toubro Ltd",
               industry="Construction", city="Ranchi, Jharkhand",
               contact_name="Anand Rao", contact_phone="9431100009",
               account_tier="warm", notes="Material handling equipment — Maini products."),
        Client(company_name="WABCO India Ltd",
               industry="Auto Components", city="Adityapur, Jamshedpur",
               contact_name="Thomas George", contact_phone="9431100010",
               account_tier="standard", notes="HP laptops + peripherals for office."),
        Client(company_name="ACC Ltd",
               industry="Cement", city="Chaibasa, Jharkhand",
               contact_name="Ramesh Gupta", contact_phone="9431100011",
               account_tier="warm", notes="Compressors + bearings. Annual service."),
        Client(company_name="Jindal Steel & Power Ltd",
               industry="Steel", city="Patratu, Jharkhand",
               contact_name="Vikas Jindal", contact_phone="9431100012",
               account_tier="hot", notes="Epiroc + Atlas Copco. Large account."),
        Client(company_name="Tata Hitachi Construction",
               industry="Heavy Equipment", city="Dharwad, Jamshedpur",
               contact_name="Hiroshi Tanaka", contact_phone="9431100013",
               account_tier="warm", notes="Rock drilling tools + hydraulic attachments."),
        Client(company_name="Kohinoor Steel Pvt Ltd",
               industry="Steel", city="Gamharia, Jamshedpur",
               contact_name="Raj Kohinoor", contact_phone="9431100014",
               account_tier="standard", notes="Bearings + motors. New account."),
        Client(company_name="Rashmi Group",
               industry="Steel & Power", city="Kolkata / Jharkhand",
               contact_name="Prashant Rashmi", contact_phone="9431100015",
               account_tier="warm", notes="Material handling. Exploring compressor needs."),
        Client(company_name="Brakes India Pvt Ltd",
               industry="Auto Components", city="Adityapur, Jamshedpur",
               contact_name="Venkat Iyer", contact_phone="9431100016",
               account_tier="standard", notes="Canon + HP for office automation."),
        Client(company_name="SAIL (Steel Authority of India)",
               industry="Steel", city="Bokaro, Jharkhand",
               contact_name="S.K. Dubey", contact_phone="9431100017",
               account_tier="prospect", notes="Prospecting — large potential for compressors."),
        Client(company_name="DVC (Damodar Valley Corp)",
               industry="Power", city="Chandrapura, Jharkhand",
               contact_name="A.K. Ghosh", contact_phone="9431100018",
               account_tier="prospect", notes="Industrial fans + motors. First contact made."),
    ]
    db.session.add_all(clients)
    db.session.flush()

    # Map by name for easy reference
    c = {cl.company_name: cl for cl in clients}
    today = date.today()
    yday  = today - timedelta(days=1)
    d2    = today - timedelta(days=2)
    d3    = today - timedelta(days=3)

    # ── VISITS ───────────────────────────────────────────────
    visits_data = [
        # Today
        dict(staff=s1, client=c["Tata Steel Ltd"], visit_date=today,
             time_in="09:30", time_out="10:45", visit_type="Follow-up",
             rep_met="Suresh Nair, Sr. Manager Maintenance",
             purpose="Follow-up on Atlas Copco GA 55 VSD compressor quotation",
             prev_visit_summary="Last visit 3 days ago — submitted quotation for 2 units GA 55 VSD. Client wanted to compare with Ingersoll Rand pricing.",
             priority="High", source="voice",
             notes="Client happy with pricing. Wants delivery in 45 days. Need to confirm Atlas Copco lead time.",
             action="Confirm delivery timeline with Atlas Copco Delhi",
             action_help="Need updated price list from Atlas Copco — check with principal",
             fu_date=today+timedelta(days=3), fu_notes="Confirm order after delivery timeline confirmed"),

        dict(staff=s2, client=c["UCIL (Uranium Corp of India)"], visit_date=today,
             time_in="10:00", time_out="11:30", visit_type="Service visit",
             rep_met="D.K. Mishra, Head Mines",
             purpose="Quarterly service of Epiroc rock drills — 4 units",
             prev_visit_summary="Last service Q1 — all 4 drills serviced. Client raised concern about drill steel wear.",
             priority="High", source="text",
             notes="Service completed. 1 drill needs replacement drill steel — ordered. 3 running fine.",
             action="Order replacement drill steel from Epiroc — urgent",
             action_help="Need Epiroc spare parts approval from V.N. Tiwary above INR 50,000",
             fu_date=today+timedelta(days=7), fu_notes="Deliver drill steel and install"),

        dict(staff=s3, client=c["Caparo Engineering India"], visit_date=today,
             time_in="11:00", time_out="11:45", visit_type="Sales call",
             rep_met="Manoj Sharma, IT Manager",
             purpose="Present Dell laptop refresh proposal — 25 units",
             prev_visit_summary="IT manager expressed interest in bulk Dell purchase for new plant expansion.",
             priority="Medium", source="voice",
             notes="Good meeting. Manoj wants comparison with HP. Will decide in 2 weeks.",
             action="Send Dell vs HP comparison sheet with pricing",
             fu_date=today+timedelta(days=5), fu_notes="Follow up on laptop decision"),

        dict(staff=s6, client=c["Jindal Steel & Power Ltd"], visit_date=today,
             time_in="14:00", time_out="15:15", visit_type="Follow-up",
             rep_met="Vikas Jindal, GM Operations",
             purpose="Follow-up on Epiroc surface drilling equipment — 3 units",
             prev_visit_summary="Demo done 2 weeks ago. Client very interested. Price negotiation pending.",
             priority="High", source="voice",
             notes="Client wants 5% discount on order value. MD approval needed.",
             action="Get discount approval from Gian Taneja for 5% on Epiroc order",
             action_help="Need MD approval for 5% discount — order value ~45 lakhs",
             fu_date=today+timedelta(days=2), fu_notes="Confirm discount and close order"),

        dict(staff=s4, client=c["Larsen & Toubro Ltd"], visit_date=today,
             time_in="10:30", time_out="11:30", visit_type="Prospecting",
             rep_met="Anand Rao, Purchase Head",
             purpose="Introduce Maini material handling range — scissor lifts and stackers",
             prev_visit_summary="Cold call — first meeting.",
             priority="Medium", source="text",
             notes="Anand interested in scissor lifts for new Ranchi warehouse. Wants demo.",
             action="Arrange Maini demo at L&T Ranchi warehouse",
             fu_date=today+timedelta(days=10), fu_notes="Demo of Maini scissor lift"),

        dict(staff=s5, client=c["DVC (Damodar Valley Corp)"], visit_date=today,
             time_in="09:00", time_out="10:00", visit_type="Prospecting",
             rep_met="A.K. Ghosh, Chief Engineer",
             purpose="First meeting — explore industrial fan and motor requirements",
             prev_visit_summary="Lead generated from industry exhibition last month.",
             priority="Medium", source="voice",
             notes="DVC has 4 power stations. Currently buying motors from Siemens. Open to quotes.",
             action="Prepare Marathon motor spec sheet vs Siemens comparison",
             fu_date=today+timedelta(days=7), fu_notes="Send motor comparison + pricing"),

        # Yesterday
        dict(staff=s1, client=c["Rungta Mines Ltd"], visit_date=yday,
             time_in="10:00", time_out="11:00", visit_type="Sales call",
             rep_met="Sunil Rungta, Director",
             purpose="Present Atlas Copco portable compressor XATS 250 for new mine site",
             prev_visit_summary="Site expansion announced — need portable compressors for Barbil site.",
             priority="High", source="voice",
             notes="Sunil very interested. Wants 3 units. Will compare with other vendors.",
             action="Submit formal quotation for 3 × XATS 250",
             fu_date=today+timedelta(days=4), fu_notes="Quotation follow-up"),

        dict(staff=s2, client=c["Tata Motors Ltd"], visit_date=yday,
             time_in="14:00", time_out="15:30", visit_type="Follow-up",
             rep_met="Rajiv Mehta, Plant Engineer",
             purpose="Annual AMC renewal discussion for material handling fleet",
             prev_visit_summary="AMC expires end of June. Rajiv wanted new pricing with extended coverage.",
             priority="High", source="text",
             notes="AMC terms agreed verbally. Formal PO expected this week.",
             action="Prepare AMC renewal contract and send for signature",
             fu_date=today+timedelta(days=5), fu_notes="Collect signed AMC"),

        dict(staff=s3, client=c["SAIL (Steel Authority of India)"], visit_date=yday,
             time_in="11:30", time_out="12:30", visit_type="Prospecting",
             rep_met="S.K. Dubey, GM Procurement",
             purpose="Introduce Atlas Copco compressor range for Bokaro steel plant",
             prev_visit_summary="SAIL Bokaro currently running aging Ingersoll Rand compressors.",
             priority="Medium", source="voice",
             notes="S.K. Dubey receptive. Will put us on approved vendor list. Long sales cycle.",
             action="Submit vendor registration documents to SAIL procurement",
             fu_date=today+timedelta(days=14), fu_notes="Check vendor registration status"),

        dict(staff=s6, client=c["BMW Industries Ltd"], visit_date=d2,
             time_in="09:30", time_out="10:30", visit_type="Service visit",
             rep_met="Ravi Kumar, Maintenance Head",
             purpose="Service call — Marathon motor fault at rolling mill",
             prev_visit_summary="Urgent call received — motor tripped at mill.",
             priority="High", source="text",
             notes="Motor winding fault confirmed. Sent for rewinding. Temporary standby motor installed.",
             action="Track rewinding progress — expected 10 days",
             fu_date=today+timedelta(days=10), fu_notes="Motor rewinding delivery"),

        dict(staff=s4, client=c["ACC Ltd"], visit_date=d2,
             time_in="10:00", time_out="11:15", visit_type="Follow-up",
             rep_met="Ramesh Gupta, Purchase Manager",
             purpose="Follow-up on Timken bearing order for cement mill",
             prev_visit_summary="Quotation submitted last week for 12 Timken roller bearings.",
             priority="Medium", source="voice",
             notes="Ramesh says PO delayed due to budget freeze. Expected next month.",
             action="Stay in touch monthly — budget resumes July",
             fu_date=today+timedelta(days=30), fu_notes="Budget review follow-up"),

        dict(staff=s5, client=c["Tata Steel Long Products"], visit_date=d3,
             time_in="14:30", time_out="16:00", visit_type="Demo",
             rep_met="P.K. Singh, Head Mining",
             purpose="Epiroc Cobra Pro rock drill demo at Gamharia site",
             prev_visit_summary="Client expressed interest in replacing 5 year old rock drills.",
             priority="High", source="voice",
             notes="Demo went very well. P.K. Singh impressed with penetration rate. Wants formal proposal.",
             action="Prepare Epiroc Cobra Pro formal proposal with TCO analysis",
             action_help="Need Epiroc's latest pricing and delivery schedule from principal",
             fu_date=today+timedelta(days=5), fu_notes="Submit Epiroc proposal"),
    ]

    for vd in visits_data:
        v = Visit(
            staff_id           = vd["staff"].id,
            client_id          = vd["client"].id,
            visit_date         = vd["visit_date"],
            time_in            = vd.get("time_in"),
            time_out           = vd.get("time_out"),
            visit_type         = vd["visit_type"],
            rep_met            = vd.get("rep_met"),
            purpose            = vd.get("purpose"),
            prev_visit_summary = vd.get("prev_visit_summary"),
            priority           = vd.get("priority","Medium"),
            notes              = vd.get("notes"),
            source             = vd.get("source","text"),
        )
        db.session.add(v)
        db.session.flush()

        if vd.get("action"):
            ai = ActionItem(
                visit_id    = v.id,
                staff_id    = vd["staff"].id,
                description = vd["action"],
                help_needed = vd.get("action_help"),
                due_date    = vd.get("fu_date"),
                status      = "open",
            )
            db.session.add(ai)

        if vd.get("fu_date"):
            fu = FollowUp(
                visit_id       = v.id,
                client_id      = vd["client"].id,
                assigned_to_id = vd["staff"].id,
                due_date       = vd["fu_date"],
                notes          = vd.get("fu_notes",""),
                status         = "scheduled",
            )
            db.session.add(fu)

    db.session.commit()

    print("Apex Corporation seed data loaded.")
    print(f"  Staff:        {Staff.query.count()}")
    print(f"  Clients:      {Client.query.count()}")
    print(f"  Visits:       {Visit.query.count()}")
    print(f"  Action items: {ActionItem.query.count()}")
    print(f"  Follow-ups:   {FollowUp.query.count()}")
