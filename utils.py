from datetime import datetime
from models import Offer, db

def deactivate_expired_offers():
    now = datetime.now()
    Offer.query.filter(Offer.active == True, Offer.expires_at <= now).update(
        {Offer.active: False},
        synchronize_session=False
    )
    db.session.commit()
