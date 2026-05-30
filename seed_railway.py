"""
seed_railway.py
Seeds Railway backend with Apex Corporation staff, clients, then 30 visits.
Run: python seed_railway.py
"""
import requests
from datetime import date, timedelta

BASE = "https://fats-production.up.railway.app/api"

def post(path, data):
    r = requests.post(BASE + path, json=data)
    try:
        return r.json()
    except:
        print(f"  Error {r.status_code}: {r.text[:100]}")
        return None

def get(path):
    r = requests.get(BASE + path)
    try:
        return r.json()
    except:
        return None

print("=== Seeding Railway with Apex Corporation data ===\n")

# ── CHECK HEALTH ──────────────────────────────
h = get("/health")
if not h or h.get("status") != "ok":
    print("Cannot reach Railway — check URL and that app is running")
    exit()
print("✓ Railway is reachable\n")

# ── STAFF ─────────────────────────────────────
print("Creating staff...")
staff_data = [
    dict(name="Gian Taneja",       phone="9835547533", email="gian@apexcorporation.net",    role="manager",     region="Jamshedpur"),
    dict(name="V.N. Tiwary",       phone="9304003154", email="vn.tiwary@apexcorporation.net",role="manager",    region="Ranchi"),
    dict(name="Bhargav Vatsyayan", phone="9835100001", email="bhargav@apexcorporation.net",  role="field_staff", region="Jamshedpur"),
    dict(name="R.B. Prasad",       phone="9835100002", email="rb.prasad@apexcorporation.net",role="field_staff", region="Jamshedpur"),
    dict(name="Arjun Prasad",      phone="9835100003", email="arjun@apexcorporation.net",    role="field_staff", region="Jamshedpur"),
    dict(name="Ajay Kumar Pandey", phone="9835100004", email="ajay@apexcorporation.net",     role="field_staff", region="Ranchi"),
    dict(name="Sumit Choubey",     phone="9835100005", email="sumit@apexcorporation.net",    role="field_staff", region="Ranchi"),
    dict(name="Rajeev Kumar Sharma",phone="9835100006",email="rajeev@apexcorporation.net",   role="field_staff", region="Jamshedpur"),
]

staff_map = {}
existing_staff = get("/staff") or []
for s in existing_staff:
    staff_map[s["name"]] = s["id"]

for s in staff_data:
    if s["name"] in staff_map:
        print(f"  already exists: {s['name']}")
        continue
    r = post("/staff", s)
    if r and (isinstance(r, dict) and r.get("id") or isinstance(r, list)):
        staff_map[r["name"]] = r["id"]
        print(f"  ✓ {r['name']}")
    else:
        print(f"  ✗ {s['name']}")

# Set manager_id for field staff
mgr_jsr = staff_map.get("Gian Taneja")
mgr_ran = staff_map.get("V.N. Tiwary")
for name, mgr in [("Bhargav Vatsyayan", mgr_jsr), ("R.B. Prasad", mgr_jsr),
                   ("Arjun Prasad", mgr_jsr), ("Rajeev Kumar Sharma", mgr_jsr),
                   ("Ajay Kumar Pandey", mgr_ran), ("Sumit Choubey", mgr_ran)]:
    sid = staff_map.get(name)
    if sid and mgr:
        requests.patch(f"{BASE}/staff/{sid}", json={"manager_id": mgr})

print(f"\n✓ {len(staff_map)} staff ready\n")

# ── CLIENTS ───────────────────────────────────
print("Creating clients...")
clients_data = [
    dict(company_name="Tata Steel Ltd",              industry="Steel Manufacturing", city="Bistupur, Jamshedpur",   contact_name="Suresh Nair",     contact_phone="9431100001", account_tier="hot"),
    dict(company_name="Tata Motors Ltd",             industry="Automotive",          city="Telco, Jamshedpur",      contact_name="Rajiv Mehta",     contact_phone="9431100002", account_tier="hot"),
    dict(company_name="Tata Steel Long Products",    industry="Steel Manufacturing", city="Gamharia, Jamshedpur",   contact_name="P.K. Singh",      contact_phone="9431100003", account_tier="hot"),
    dict(company_name="Tata Cummins Ltd",            industry="Engineering",         city="Telco, Jamshedpur",      contact_name="Arun Verma",      contact_phone="9431100004", account_tier="warm"),
    dict(company_name="UCIL (Uranium Corp of India)",industry="Mining",              city="Jadugora, Jharkhand",    contact_name="D.K. Mishra",     contact_phone="9431100005", account_tier="hot"),
    dict(company_name="Rungta Mines Ltd",            industry="Mining",              city="Barbil, Jharkhand",      contact_name="Sunil Rungta",    contact_phone="9431100006", account_tier="warm"),
    dict(company_name="BMW Industries Ltd",          industry="Steel",               city="Gamharia, Jamshedpur",   contact_name="Ravi Kumar",      contact_phone="9431100007", account_tier="warm"),
    dict(company_name="Caparo Engineering India",    industry="Auto Components",     city="Adityapur, Jamshedpur",  contact_name="Manoj Sharma",    contact_phone="9431100008", account_tier="standard"),
    dict(company_name="Larsen & Toubro Ltd",         industry="Construction",        city="Ranchi, Jharkhand",      contact_name="Anand Rao",       contact_phone="9431100009", account_tier="warm"),
    dict(company_name="WABCO India Ltd",             industry="Auto Components",     city="Adityapur, Jamshedpur",  contact_name="Thomas George",   contact_phone="9431100010", account_tier="standard"),
    dict(company_name="ACC Ltd",                     industry="Cement",              city="Chaibasa, Jharkhand",    contact_name="Ramesh Gupta",    contact_phone="9431100011", account_tier="warm"),
    dict(company_name="Jindal Steel & Power Ltd",    industry="Steel",               city="Patratu, Jharkhand",     contact_name="Vikas Jindal",    contact_phone="9431100012", account_tier="hot"),
    dict(company_name="Tata Hitachi Construction",   industry="Heavy Equipment",     city="Dharwad, Jamshedpur",    contact_name="Hiroshi Tanaka",  contact_phone="9431100013", account_tier="warm"),
    dict(company_name="Kohinoor Steel Pvt Ltd",      industry="Steel",               city="Gamharia, Jamshedpur",   contact_name="Raj Kohinoor",    contact_phone="9431100014", account_tier="standard"),
    dict(company_name="Rashmi Group",                industry="Steel & Power",       city="Ranchi, Jharkhand",      contact_name="Prashant Rashmi", contact_phone="9431100015", account_tier="warm"),
    dict(company_name="Brakes India Pvt Ltd",        industry="Auto Components",     city="Adityapur, Jamshedpur",  contact_name="Venkat Iyer",     contact_phone="9431100016", account_tier="standard"),
    dict(company_name="SAIL (Steel Authority of India)", industry="Steel",           city="Bokaro, Jharkhand",      contact_name="S.K. Dubey",      contact_phone="9431100017", account_tier="prospect"),
    dict(company_name="DVC (Damodar Valley Corp)",   industry="Power",               city="Chandrapura, Jharkhand", contact_name="A.K. Ghosh",      contact_phone="9431100018", account_tier="prospect"),
]

client_map = {}
existing_clients = get("/clients") or []
for c in existing_clients:
    client_map[c["company_name"]] = c["id"]

for c in clients_data:
    if c["company_name"] in client_map:
        print(f"  already exists: {c['company_name']}")
        continue
    r = post("/clients", c)
    if r and (isinstance(r, dict) and r.get("id") or isinstance(r, list)):
        client_map[r["company_name"]] = r["id"]
        print(f"  ✓ {r['company_name']}")
    else:
        print(f"  ✗ {c['company_name']}")

print(f"\n✓ {len(client_map)} clients ready\n")

# ── 30 VISITS ─────────────────────────────────
print("Posting 30 visits...")

today = date.today()

def sid(name):
    for k, v in staff_map.items():
        if name.lower() in k.lower():
            return v
    return None

def cid(name):
    for k, v in client_map.items():
        if name.lower() in k.lower():
            return v
    return None

visits = [
    dict(st="Bhargav Vatsyayan", cl="Tata Steel",          ago=0, tin="09:15", tout="10:30", vt="Follow-up",    rep="Suresh Nair, Sr. Manager Maintenance",  pur="Follow up on GA 55 VSD compressor order — 2 units",                     prev="Quotation submitted. Client comparing with IR pricing.",           act="Confirm Atlas Copco delivery timeline — 45 days",        help="Need updated price list from Atlas Copco principal",          fu=3,  pri="High",   notes="Client leaning towards us. Price competitive."),
    dict(st="Bhargav Vatsyayan", cl="Rungta Mines",         ago=1, tin="11:30", tout="12:15", vt="Sales call",   rep="Sunil Rungta, Director",                 pur="Present Atlas Copco XATS 250 portable compressor — 3 units",            prev="Site expansion confirmed. Need 3 portable compressors.",           act="Submit formal quotation for 3 x XATS 250",               help=None,                                                          fu=4,  pri="High",   notes="Very interested. Decision in 2 weeks."),
    dict(st="Bhargav Vatsyayan", cl="Jindal Steel",         ago=2, tin="14:00", tout="15:30", vt="Follow-up",    rep="Vikas Jindal, GM Operations",            pur="Discount approval follow-up on Epiroc surface drilling order",          prev="Demo done. Client wants 5% discount on 45 lakh order.",           act="Confirm 5% discount and send revised quote",             help="MD approval needed for 5% discount on order above 40 lakhs", fu=2,  pri="High",   notes="Order likely to close this week if discount approved."),
    dict(st="Bhargav Vatsyayan", cl="BMW Industries",       ago=3, tin="10:00", tout="11:00", vt="Service visit",rep="Ravi Kumar, Maintenance Head",           pur="Quarterly service of Atlas Copco GA 30 compressor",                     prev="Last service 3 months ago. No issues.",                           act="Submit service report and schedule next visit",          help=None,                                                          fu=90, pri="Low",    notes="Service completed. All parameters normal."),
    dict(st="Bhargav Vatsyayan", cl="Kohinoor Steel",       ago=4, tin="09:30", tout="10:15", vt="Prospecting",  rep="Raj Kohinoor, MD",                       pur="First meeting — introduce Atlas Copco compressor range",                prev="Cold call. New contact from industry referral.",                  act="Send product catalogue and arrange plant visit",         help=None,                                                          fu=10, pri="Medium", notes="MD receptive. Plant expanding next quarter."),
    dict(st="R.B. Prasad",       cl="UCIL",                 ago=0, tin="10:00", tout="11:30", vt="Service visit",rep="D.K. Mishra, Head Mines",                pur="Quarterly service of Epiroc rock drills — 4 units",                     prev="Q1 service done. Drill steel wear concern raised.",               act="Order replacement drill steel from Epiroc — urgent",     help="Need Epiroc spare parts approval from V.N. Tiwary above 50k", fu=7,  pri="High",   notes="1 drill needs replacement steel. 3 running fine."),
    dict(st="R.B. Prasad",       cl="Tata Steel Long",      ago=1, tin="14:30", tout="16:00", vt="Demo",         rep="P.K. Singh, Head Mining",                pur="Epiroc Cobra Pro rock drill demo at Gamharia site",                     prev="Client expressed interest in replacing 5-year-old drills.",       act="Prepare Epiroc Cobra Pro proposal with TCO analysis",    help="Need Epiroc latest pricing from principal",                   fu=5,  pri="High",   notes="Demo went very well. P.K. impressed with penetration rate."),
    dict(st="R.B. Prasad",       cl="Tata Motors",          ago=2, tin="14:00", tout="15:30", vt="Follow-up",    rep="Rajiv Mehta, Plant Engineer",            pur="Annual AMC renewal — material handling fleet",                          prev="AMC expires end of June. New pricing requested.",                 act="Prepare AMC renewal contract and send for signature",    help=None,                                                          fu=5,  pri="High",   notes="Terms agreed verbally. PO expected this week."),
    dict(st="R.B. Prasad",       cl="SAIL",                 ago=3, tin="11:30", tout="12:30", vt="Prospecting",  rep="S.K. Dubey, GM Procurement",             pur="Introduce Atlas Copco compressor range for Bokaro plant",               prev="SAIL running aging Ingersoll Rand compressors.",                  act="Submit vendor registration documents to SAIL",           help=None,                                                          fu=14, pri="Medium", notes="Long sales cycle. Getting on approved vendor list."),
    dict(st="R.B. Prasad",       cl="Tata Hitachi",         ago=5, tin="10:30", tout="11:45", vt="Sales call",   rep="Hiroshi Tanaka, Purchase Manager",       pur="Epiroc hydraulic attachment tools — excavator range",                   prev="New contact. Tata Hitachi expanding excavator production.",       act="Send Epiroc hydraulic tools catalogue with pricing",     help=None,                                                          fu=7,  pri="Medium", notes="Hiroshi interested. Will share with technical team."),
    dict(st="Arjun Prasad",      cl="Caparo Engineering",   ago=0, tin="11:00", tout="11:45", vt="Sales call",   rep="Manoj Sharma, IT Manager",               pur="Dell laptop refresh proposal — 25 units for plant expansion",           prev="IT manager expressed interest in bulk Dell purchase.",            act="Send Dell vs HP comparison sheet with bulk pricing",     help=None,                                                          fu=5,  pri="Medium", notes="Will compare with HP. Decision in 2 weeks."),
    dict(st="Arjun Prasad",      cl="Tata Cummins",         ago=1, tin="09:30", tout="10:30", vt="Service visit",rep="Arun Verma, Admin Head",                 pur="Canon photocopier quarterly service — 12 units",                        prev="All 12 units serviced last quarter. 1 unit had drum issue.",      act="Replace drum unit on Unit 7 — part ordered",            help=None,                                                          fu=14, pri="Low",    notes="11 units fine. Unit 7 drum replaced."),
    dict(st="Arjun Prasad",      cl="WABCO India",          ago=2, tin="14:00", tout="15:00", vt="Follow-up",    rep="Thomas George, IT Head",                 pur="HP laptop order follow-up — 15 units for new office",                   prev="PO expected last week. Delayed due to budget approval.",          act="Follow up with Thomas on PO status",                     help=None,                                                          fu=7,  pri="Medium", notes="Budget approved. PO being raised. Expected by Friday."),
    dict(st="Arjun Prasad",      cl="Brakes India",         ago=3, tin="11:00", tout="11:45", vt="Sales call",   rep="Venkat Iyer, Purchase Manager",          pur="Canon colour printer proposal for design department",                   prev="Design team complained about slow BW printer.",                  act="Submit Canon imageRUNNER colour proposal",               help=None,                                                          fu=10, pri="Low",    notes="Venkat interested in colour MFD."),
    dict(st="Arjun Prasad",      cl="Rashmi Group",         ago=4, tin="10:00", tout="11:00", vt="Prospecting",  rep="Prashant Rashmi, GM Admin",              pur="Introduce Riso digital duplicator for high-volume printing",            prev="New contact. Rashmi Group prints 10,000+ copies/day.",            act="Arrange Riso duplicator demo at Rashmi office",         help=None,                                                          fu=12, pri="Medium", notes="Very interested in cost savings vs laser printing."),
    dict(st="Ajay Kumar Pandey", cl="Larsen & Toubro",      ago=0, tin="10:30", tout="11:30", vt="Prospecting",  rep="Anand Rao, Purchase Head",               pur="Introduce Maini material handling — scissor lifts and stackers",        prev="First meeting. L&T building new Ranchi warehouse.",               act="Arrange Maini scissor lift demo at L&T warehouse",      help=None,                                                          fu=10, pri="Medium", notes="Anand interested. Wants demo before deciding."),
    dict(st="Ajay Kumar Pandey", cl="ACC Ltd",              ago=1, tin="10:00", tout="11:15", vt="Follow-up",    rep="Ramesh Gupta, Purchase Manager",         pur="Timken bearing order follow-up — 12 units for cement mill",             prev="Quotation submitted. PO delayed due to budget freeze.",           act="Stay in touch — budget resumes July",                   help=None,                                                          fu=30, pri="Medium", notes="Budget freeze until July. Revisit then."),
    dict(st="Ajay Kumar Pandey", cl="DVC",                  ago=2, tin="09:00", tout="10:00", vt="Prospecting",  rep="A.K. Ghosh, Chief Engineer",             pur="Explore industrial fan and motor requirements — 4 power stations",     prev="Lead from industry exhibition last month.",                       act="Prepare Marathon motor spec sheet vs Siemens",          help=None,                                                          fu=7,  pri="Medium", notes="DVC open to quotes. Currently buying from Siemens."),
    dict(st="Ajay Kumar Pandey", cl="Larsen & Toubro",      ago=5, tin="14:00", tout="15:00", vt="Follow-up",    rep="Anand Rao, Purchase Head",               pur="Follow up on Maini demo feedback",                                      prev="Demo done last week. Technical team reviewing.",                  act="Send Maini total cost of ownership comparison",         help=None,                                                          fu=7,  pri="Medium", notes="Technical team impressed. Commercial negotiation starting."),
    dict(st="Ajay Kumar Pandey", cl="ACC Ltd",              ago=7, tin="09:30", tout="10:30", vt="Sales call",   rep="Ramesh Gupta, Purchase Manager",         pur="Atlas Copco air dryer proposal for cement plant",                       prev="Bearings discussed. New opportunity identified.",                 act="Submit Atlas Copco FD series dryer quotation",          help=None,                                                          fu=14, pri="Low",    notes="Cement dust causing compressor issues. Dryer will help."),
    dict(st="Sumit Choubey",     cl="DVC",                  ago=1, tin="11:00", tout="12:00", vt="Follow-up",    rep="A.K. Ghosh, Chief Engineer",             pur="Present Marathon motor comparison vs Siemens",                          prev="First meeting — DVC interested in motor quotes.",                 act="Submit formal quotation for Marathon motors — 20 units",help=None,                                                          fu=10, pri="High",   notes="A.K. Ghosh impressed with Marathon specs. Price competitive."),
    dict(st="Sumit Choubey",     cl="Tata Steel Long",      ago=2, tin="09:00", tout="10:30", vt="Service visit",rep="P.K. Singh, Head Mining",                pur="Emergency — Epiroc drill rig hydraulic failure",                        prev="Drill rig COP 1840 hydraulic system failed.",                     act="Order hydraulic pump from Epiroc — urgent delivery",    help="Need emergency parts order approval — estimated INR 80,000",  fu=3,  pri="High",   notes="Temporary fix done. Production resumed at 60%."),
    dict(st="Sumit Choubey",     cl="SAIL",                 ago=4, tin="14:00", tout="15:00", vt="Follow-up",    rep="S.K. Dubey, GM Procurement",             pur="Vendor registration status check",                                      prev="Documents submitted 2 weeks ago.",                                act="Follow up on vendor registration approval",              help=None,                                                          fu=14, pri="Medium", notes="Registration under review. 3 more weeks expected."),
    dict(st="Sumit Choubey",     cl="Rashmi Group",         ago=6, tin="10:00", tout="11:00", vt="Demo",         rep="Prashant Rashmi, GM Admin",              pur="Riso duplicator live demo — cost savings demonstration",                prev="Prospecting visit done. Client interested in demo.",              act="Prepare cost savings report — Riso vs laser printing",  help=None,                                                          fu=7,  pri="Medium", notes="Demo successful. 50 paise/copy vs 3 rupees laser."),
    dict(st="Rajeev Kumar Sharma",cl="Jindal Steel",        ago=0, tin="09:00", tout="10:30", vt="Follow-up",    rep="Vikas Jindal, GM Operations",            pur="Epiroc SmartROC T35 surface drill proposal review",                     prev="Technical presentation done. Commercial terms under discussion.", act="Submit revised commercial proposal",                     help="Need Epiroc special pricing approval for strategic account",  fu=5,  pri="High",   notes="Vikas very serious. Competing with Sandvik."),
    dict(st="Rajeev Kumar Sharma",cl="Tata Steel",          ago=1, tin="11:00", tout="12:30", vt="Sales call",   rep="Suresh Nair, Sr. Manager Maintenance",  pur="Timken bearing annual contract renewal — 500+ bearings",                prev="Annual contract expires end of June.",                            act="Prepare Timken annual contract renewal proposal",       help=None,                                                          fu=7,  pri="High",   notes="Tata Steel largest Timken customer. Must retain."),
    dict(st="Rajeev Kumar Sharma",cl="Caparo Engineering",  ago=3, tin="14:30", tout="15:30", vt="Collection",   rep="Manoj Sharma, IT Manager",               pur="Collect payment for HP laptop order — INR 4.5 lakhs",                  prev="Laptops delivered last week. Payment due today.",                 act="Deposit cheque and send receipt",                       help=None,                                                          fu=1,  pri="High",   notes="Cheque collected. INR 4.5 lakhs. Depositing today."),
    dict(st="Rajeev Kumar Sharma",cl="BMW Industries",      ago=4, tin="09:30", tout="10:30", vt="Follow-up",    rep="Ravi Kumar, Maintenance Head",           pur="Marathon motor rewinding status — rolling mill motor",                  prev="Motor sent for rewinding 10 days ago. Standby installed.",       act="Confirm rewinding completion and schedule installation", help=None,                                                          fu=3,  pri="High",   notes="Rewinding done. Installation scheduled Monday."),
    dict(st="Rajeev Kumar Sharma",cl="Kohinoor Steel",      ago=6, tin="11:00", tout="12:00", vt="Sales call",   rep="Raj Kohinoor, MD",                       pur="Timken bearing proposal for rolling mill — 50 units",                   prev="MD showed interest in Timken bearings.",                          act="Submit Timken bearing proposal with 3-year price lock", help=None,                                                          fu=10, pri="Medium", notes="MD liked price lock concept."),
    dict(st="Rajeev Kumar Sharma",cl="Tata Cummins",        ago=7, tin="14:00", tout="15:00", vt="Follow-up",    rep="Arun Verma, Admin Head",                 pur="Canon imageRUNNER ADVANCE upgrade proposal — 6 units",                  prev="Old Canon machines due for upgrade.",                             act="Submit Canon ADVANCE C5560i upgrade proposal",          help=None,                                                          fu=14, pri="Medium", notes="Budget available Q3. Technical evaluation ongoing."),
]

success = 0
for i, v in enumerate(visits):
    staff_id  = sid(v["st"])
    client_id = cid(v["cl"])

    if not staff_id:
        print(f"  [{i+1}] ✗ Staff not found: {v['st']}")
        continue

    visit_date = (today - timedelta(days=v["ago"])).isoformat()
    fu_date    = (today + timedelta(days=v["fu"])).isoformat()

    payload = {
        "staff_id":           staff_id,
        "visit_date":         visit_date,
        "time_in":            v["tin"],
        "time_out":           v["tout"],
        "visit_type":         v["vt"],
        "rep_met":            v["rep"],
        "purpose":            v["pur"],
        "prev_visit_summary": v["prev"],
        "action_items":       [v["act"]],
        "follow_up_date":     fu_date,
        "priority":           v["pri"],
        "notes":              v["notes"],
        "source":             "text",
    }
    if client_id:
        payload["client_id"] = client_id
    else:
        payload["client_name"] = v["cl"]
    if v.get("help"):
        payload["help_needed"] = v["help"]

    r = post("/visits", payload)
    if r and (isinstance(r, dict) and r.get("id") or isinstance(r, list)):
        print(f"  [{i+1}] ✓ {v['st'].split()[0]} → {v['cl']} ({v['vt']})")
        success += 1
    else:
        print(f"  [{i+1}] ✗ Failed: {v['st']} → {v['cl']}")

print(f"\n✓ {success}/30 visits posted")
print(f"\nDashboard: https://fats-production.up.railway.app")
print(f"PWA:       https://fats-production.up.railway.app/pwa/")
