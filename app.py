from flask import Flask, render_template, request, redirect, url_for
from config import settings
from models import db, Offer
from datetime import datetime, timedelta
from utils import deactivate_expired_offers

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

MIN_HOURS_AHEAD = 2  
MAX_DAYS_AHEAD = 7

@app.route("/")
def home():
    deactivate_expired_offers()

    q = request.args.get("q", "").strip()

    query = Offer.query.filter(Offer.active == True)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Offer.food_name.ilike(like)) |
            (Offer.food_description.ilike(like)) |
            (Offer.location.ilike(like)) |
            (Offer.restaurant_name.ilike(like))
        )
    offers = query.order_by(Offer.created_at.desc()).all()
    return render_template("home.html", offers=offers, q=q)


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        restaurant_name = request.form.get("restaurant_name", "").strip()
        food_name = request.form.get("food_name", "").strip()
        quantity_raw = request.form.get("quantity", "").strip()
        food_description = request.form.get("food_description", "").strip()
        location = request.form.get("location", "").strip()
        email = request.form.get("email", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        expires_at_raw = request.form.get("expires_at", "").strip()

        # Minimal validation (keep it small)
        if not all([restaurant_name, food_name, quantity_raw, location, email, phone_number, expires_at_raw]):
            return "Missing required fields", 400

        try:
            quantity = int(quantity_raw)
        except ValueError:
            return "Quantity must be a number", 400

        # HTML datetime-local returns "YYYY-MM-DDTHH:MM"
        try:
            expires_at = datetime.fromisoformat(expires_at_raw)
        except ValueError:
            return "Invalid expires_at format", 400
        

        now = datetime.now()

        # Rule 1: not in the past
        if expires_at <= now:
            return "Expiration time cannot be in the past.", 400

        # Rule 2: at least N hours ahead
        if expires_at < now + timedelta(hours=MIN_HOURS_AHEAD):
            return f"Expiration must be at least {MIN_HOURS_AHEAD} hours from now.", 400

        
        if expires_at > now + timedelta(days=MAX_DAYS_AHEAD):
            return f"Expiration must be within {MAX_DAYS_AHEAD} days.", 400


        offer = Offer(
            restaurant_name=restaurant_name,
            food_name=food_name,
            quantity=quantity,
            food_description=food_description or None,
            location=location,
            email=email,
            phone_number=phone_number,
            expires_at=expires_at,
        )

        db.session.add(offer)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("donation_form.html")

@app.post("/offers/<int:offer_id>/claim")
def claim_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    offer.claimed = True
    offer.active = False
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
