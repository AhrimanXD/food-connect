from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, DateTime, func, JSON
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
  active: Mapped[bool] = mapped_column(Boolean, default=True)
  email: Mapped[str] = mapped_column(String(100), nullable= False)
  phone_number: Mapped[str] = mapped_column(String, nullable= False)
  embedding: Mapped[list[float] | None] = mapped_column(JSON, nullable=True) 
  expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  def __repr__(self) -> str:
    return f"<Offer id={self.id} food_name={self.food_name!r} location={self.location!r} claimed={self.claimed}>"

  def to_json(self):
    return {
      "id": self.id,
      "restaurant_name": self.restaurant_name,
      "food_name": self.food_name,
      "quantity": self.quantity,
      "food_description": self.food_description,
      "claimed": self.claimed,
      "email": self.email,
      "phone_number": self.phone_number,
      "expires_at": self.expires_at.isoformat() if self.expires_at else None,
      "created_at": self.created_at.isoformat() if self.created_at else None
    }