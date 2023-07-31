from flask import jsonify, request, abort, send_file
from app.api import bp
from app.extensions import db
from app.models.review import Review
from app.models.video import Video
from app.models.top_slider import TopSlider
from app.models.bottom_slider import BottomSlider
from app.models.price import Price
import os
import json

@bp.route("/")
def index():
    return "API"

@bp.route("/get_reviews")
def get_reviews():
    reviews = Review.query.all()
    return jsonify(reviews)

@bp.route("/get_video")
def get_video():
    video = Video.query.one()
    return jsonify(video)

@bp.route("/get_top_slider")
def get_top_slider():
    slider = TopSlider.query.all()
    return jsonify(slider)

@bp.route("/get_bottom_slider")
def get_bottom_slider():
    slider = BottomSlider.query.all()
    return jsonify(slider)

@bp.route("/get_prices")
def get_prices():
    raw_prices = Price.query.all()
    prices = [[], [], []]
    for price in raw_prices:
        prices[price.price_type].append({
            'id': price.id,
            'points': json.loads(price.points),
            'value': price.value,
            'old_value': price.old_value
        })
    return jsonify(prices)

@bp.route('/image/<filename>')
def get_image(filename):
    if not os.path.isfile("app/static/images/" + filename):
        abort(404)
    return send_file("static/images/" + filename, as_attachment=True)