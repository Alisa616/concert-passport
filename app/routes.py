from flask import render_template
from . import db
from .models import Concerts

def init_routes(app):
    @app.route("/")
    def show_concerts():
        concerts = Concerts.query.order_by(Concerts.event_date).all()

        return render_template('index.html', concerts=concerts)

    @app.route("/<int:concert_id>")
    def concert_detail(concert_id):
        concert = Concerts.query.get_or_404(concert_id)
        return render_template('concert_detail.html', concert=concert)