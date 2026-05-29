"""
seed.py — run once after flask db upgrade to create test data.
Usage: python3 seed.py
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
    db.create_all()

    # Manager
    mgr = Staff(name="Rajiv Sharma", phone="9810000001",
                email="rajiv@company.com", role="manager", region="Gurgaon")
    db.session.add(mgr)
    db.session.flush()

    # Field staff
    s1 = Staff(name="Suresh Kumar", phone="9810000002",
               email="suresh@company.com", role="field_staff",
               region="Gurgaon", manager_id=mgr.id)
    s2 = Staff(name="Priya Mehta", phone="9810000003",
               email="priya@company.com", role="field_staff",
               region="Gurgaon", manager_id=mgr.id)
    db.session.add_all([s1, s2])
    db.session.flush()

    # Clients
    c1 = Client(company_name="Mehta Traders",     city="Sector 14, Gurgaon",
                contact_name="Rohit Mehta",        account_tier="hot")
    c2 = Client(company_name="Raj Enterprises",   city="DLF Phase 2, Gurgaon",
                contact_name="Anil Raj",           account_tier="warm")
    c3 = Client(company_name="Singh & Co",        city="Sohna Road, Gurgaon",
                contact_name="Harpreet Singh",     account_tier="prospect")
    db.session.add_all([c1, c2, c3])
    db.session.flush()

    today = date.today()

    # Visits
    v1 = Visit(staff_id=s1.id, client_id=c1.id, visit_date=today,
               time_in="10:30", time_out="11:15",
               visit_type="Follow-up", rep_met="Rohit Mehta, MD",
               purpose="Follow-up on Q2 order quotation",
               prev_visit_summary="Last visit: discussed 500-unit order, price objection",
               priority="High", source="voice",
               notes="Client wants revised pricing by Friday")
    v2 = Visit(staff_id=s1.id, client_id=c2.id, visit_date=today,
               time_in="12:00", time_out="12:45",
               visit_type="Sales call", rep_met="Anil Raj, Purchase Head",
               purpose="Introduce new product line",
               priority="Medium", source="text")
    v3 = Visit(staff_id=s2.id, client_id=c3.id, visit_date=today,
               time_in="11:00", time_out="11:30",
               visit_type="Prospecting", rep_met="Harpreet Singh, Owner",
               purpose="First meeting — assess AMC potential",
               priority="Medium", source="voice")
    db.session.add_all([v1, v2, v3])
    db.session.flush()

    # Action items
    ai1 = ActionItem(visit_id=v1.id, staff_id=s1.id,
                     description="Send revised pricing to Rohit Mehta by Friday",
                     due_date=today + timedelta(days=2),
                     help_needed="Need approval from manager for 5% discount")
    ai2 = ActionItem(visit_id=v2.id, staff_id=s1.id,
                     description="Share product catalogue and samples",
                     due_date=today + timedelta(days=1))
    db.session.add_all([ai1, ai2])

    # Follow-ups
    fu1 = FollowUp(visit_id=v1.id, client_id=c1.id, assigned_to_id=s1.id,
                   due_date=today + timedelta(days=3),
                   notes="Confirm order after revised pricing sent", status="scheduled")
    fu2 = FollowUp(visit_id=v3.id, client_id=c3.id, assigned_to_id=s2.id,
                   due_date=today + timedelta(days=7),
                   notes="Second meeting — bring AMC proposal", status="scheduled")
    db.session.add_all([fu1, fu2])

    db.session.commit()
    print("Seed data created successfully.")
    print(f"  Staff:   {Staff.query.count()}")
    print(f"  Clients: {Client.query.count()}")
    print(f"  Visits:  {Visit.query.count()}")
    print(f"  Actions: {ActionItem.query.count()}")
    print(f"  F/Ups:   {FollowUp.query.count()}")
