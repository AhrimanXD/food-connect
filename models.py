from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, DateTime, func
from datetime import datetime
db = SQLAlchemy()

class Offer(db.Model):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  restaurant_name: Mapped[str] = mapped_column(String(50), nullable= False)
  food_name: Mapped[str] = mapped_column(String(50), nullable=False)
  quantity: Mapped[int] = mapped_column(Integer, nullable = False)
  food_description: Mapped[str] = mapped_column(Text, nullable=True)
  location: Mapped[str] = mapped_column(String(30), nullable = False)
  claimed: Mapped[bool] = mapped_column(Boolean, default= False)
  email: Mapped[str] = mapped_column(String(100), nullable= False)
  phone_number: Mapped[int] = mapped_column(Integer, nullable= False)
  expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())