from flask import render_template
from . import db
from .models import Concerts

def init_routes(app):
    @app.route("/")
    def index():
        concerts = Concerts.query.order_by(Concerts.event_date).limit(10).all()
        return render_template('index.html', concerts=concerts)