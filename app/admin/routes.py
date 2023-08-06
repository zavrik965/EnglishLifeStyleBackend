from flask import jsonify, request, abort, send_file
from app.admin import bp
from app.extensions import db
from app.models.review import Review
from app.models.video import Video
from app.models.top_slider import TopSlider
from app.models.bottom_slider import BottomSlider
from app.models.price import Price
from app.models.user import User
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
import hashlib
import json

@bp.route("/")
def index():
    return "admin"

@bp.route("/login", methods=["POST"])
def login():
    login = request.json.get("login")
    password = request.json.get("password")
    hash_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = User.query.filter(User.login == login).filter(User.password == hash_password).all()
    if user:
        access_token = create_access_token(identity=login)
        response = {"access_token":access_token}
        return response
    response = jsonify({"status": "Not auth"})
    unset_jwt_cookies(response)
    return response, 401

@bp.route("/update_reviews", methods=["POST"])
@jwt_required()
def update_reviews():
    raw_reviews = request.json
    old_reviews = Review.query.all()
    new_list_reviews = []
    for raw_review in raw_reviews:
        if raw_review.get("id") == -1:
            review = Review(author=raw_review.get("author"), content=raw_review.get("content"))
            db.session.add(review)
            new_list_reviews.append(review.id)
        else:
            new_list_reviews.append(raw_review.get("id"))
    for review in old_reviews:
        if review.id not in new_list_reviews:
            Review.query.filter(Review.id == review.id).delete()
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/set_video", methods=["POST"])
@jwt_required()
def set_video():
    raw_url = request.json
    video = Video.query.one()
    video.url = raw_url.get("url")
    db.session.commit()
    return jsonify(video)

@bp.route("/update_top_slider", methods=["POST"])
@jwt_required()
def update_top_slider():
    raw_slider = request.json
    old_slider = TopSlider.query.all()
    new_list_slider = []
    for raw_slider_item in raw_slider:
        if raw_slider_item.get("id") == -1:
            slider = TopSlider(image_url=raw_slider_item.get("image_url"), content=raw_slider_item.get("content"))
            db.session.add(slider)
            new_list_slider.append(slider.id)
        else:
            new_list_slider.append(raw_slider_item.get("id"))
    for slider in old_slider:
        if slider.id not in new_list_slider:
            TopSlider.query.filter(TopSlider.id == slider.id).delete()
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/update_bottom_slider", methods=["POST"])
@jwt_required()
def update_bottom_slider():
    raw_slider = request.json
    old_slider = BottomSlider.query.all()
    new_list_slider = []
    for raw_slider_item in raw_slider:
        if raw_slider_item.get("id") == -1:
            slider = BottomSlider(image_url=raw_slider_item.get("image_url"), content=raw_slider_item.get("content"))
            db.session.add(slider)
            new_list_slider.append(slider.id)
        else:
            new_list_slider.append(raw_slider_item.get("id"))
    for slider in old_slider:
        if slider.id not in new_list_slider:
            BottomSlider.query.filter(BottomSlider.id == slider.id).delete()
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/add_image", methods=["POST"])
@jwt_required()
def add_image():
    img = request.files['file']
    image_url = request.form["image_url"]
    img.save(f"app/static/images/{image_url}")
    return jsonify({"status": "OK"}), 200

@bp.route("/update_price_lists", methods=["POST"])
@jwt_required()
def update_price_lists():
    raw_price_lists = request.json
    old_prices = Price.query.all()
    new_list_prices = []
    for price_type, raw_price_list in enumerate(raw_price_lists):
        for raw_price in raw_price_list:
            if raw_price.get("id") == -1:
                price = Price(points=json.dumps(raw_price.get("points")), value=raw_price.get("value"), old_value=raw_price.get("old_value"), price_type=price_type)
                db.session.add(price)
                new_list_prices.append(price.id)
            else:
                new_list_prices.append(raw_price.get("id"))
    for price in old_prices:
        if price.id not in new_list_prices:
            Price.query.filter(Price.id == price.id).delete()
    db.session.commit()
    return jsonify({"status": "OK"}), 200