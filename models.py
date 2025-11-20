from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)  # e.g., "Cashier", "Nurse", "Driver"
    # Critical data point for AI fairness ranking
    hours_worked_last_7d = Column(Integer, default=0)

    shifts = relationship("Shift", back_populates="user")
    swap_requests = relationship("SwapRequest", back_populates="requestor")

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="shifts")
    # One shift can have multiple swap requests associated with it
    swap_requests = relationship("SwapRequest", back_populates="shift")

class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id = Column(Integer, primary_key=True, index=True)
    requesting_user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    status = Column(String, default="PENDING")  # PENDING, APPROVED, DENIED
    
    # Stores the raw JSON reasoning from the AI for manager auditing
    ai_ranking_metadata = Column(String, nullable=True)

    requestor = relationship("User", back_populates="swap_requests")
    shift = relationship("Shift", back_populates="swap_requests")
