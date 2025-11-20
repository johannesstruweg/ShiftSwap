from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Shift
from datetime import datetime, timedelta

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(Shift).delete()
    db.query(User).delete()
    db.commit()

    print("🌱 Seeding Database...")

    # 1. Create Users (Waiters)
    # Alice needs a swap.
    alice = User(name="Alice (Requestor)", role="Waiter", hours_worked_last_7d=35)
    
    # Bob is overworked (Fatigue Risk)
    bob = User(name="Bob (Overworked)", role="Waiter", hours_worked_last_7d=55)
    
    # Charlie is fresh (Best Match)
    charlie = User(name="Charlie (Fresh)", role="Waiter", hours_worked_last_7d=10)
    
    # Dave is in a different role (Should be ignored by Eligibility Engine)
    dave = User(name="Dave (Cook)", role="Cook", hours_worked_last_7d=20)

    db.add_all([alice, bob, charlie, dave])
    db.commit()

    # 2. Create a Shift for Alice to Swap
    # Shift is tomorrow, 9am - 5pm
    start = datetime.now() + timedelta(days=1).replace(hour=9, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=8)
    
    shift = Shift(role="Waiter", start_time=start, end_time=end, user_id=alice.id)
    
    db.add(shift)
    db.commit()

    print(f"✅ Seed Complete.")
    print(f"Created Shift ID: {shift.id} for {alice.name}")
    print(f"Candidates created: Bob (55hrs), Charlie (10hrs), Dave (Cook - ineligible)")
    print("Run main.py to start the server!")
    
    db.close()

if __name__ == "__main__":
    seed_data()
