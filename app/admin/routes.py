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

@bp.route("/add_review", methods=["POST"])
@jwt_required()
def add_review():
    raw_review = request.json
    review = Review(author=raw_review.get("author"), content=raw_review.get("content"))
    db.session.add(review)
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/change_review", methods=["POST"])
@jwt_required()
def change_review():
    raw_review = request.json
    review = Review.query.filter(Review.id == raw_review.get("id"))
    review.author = raw_review.get("author")
    review.content = raw_review.get("content")
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/remove_review", methods=["POST"])
@jwt_required()
def remove_review():
    raw_review = request.json
    review = Review.query.filter(Review.id == raw_review.get("id")).delete()
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

@bp.route("/add_to_top_slider", methods=["POST"])
@jwt_required()
def add_to_top_slider():
    raw_slider = request.json
    slider = TopSlider(image_url=f'http://192.168.168.71:5000/api/image/{raw_slider.get("image_url")}', content=raw_slider.get("content"))
    db.session.add(slider)
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/add_to_bottom_slider", methods=["POST"])
@jwt_required()
def add_to_bottom_slider():
    raw_slider = request.json
    slider = BottomSlider(image_url=f'http://192.168.168.71:5000/api/image/{raw_slider.get("image_url")}', content=raw_slider.get("content"))
    db.session.add(slider)
    db.session.commit()
    return jsonify({"status": "OK"}), 200

@bp.route("/add_image", methods=["POST"])
@jwt_required()
def add_image():
    img = request.files['file']
    image_url = request.form["image_url"]
    img.save(f"app/static/image/{image_url}")