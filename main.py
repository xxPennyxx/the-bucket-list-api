from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///places.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap5(app)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Place(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(500), nullable=False)  # Google Maps URL
    open: Mapped[str] = mapped_column(String(100), nullable=False)
    close: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[str] = mapped_column(String(10), nullable=False)
    review: Mapped[str] = mapped_column(String(500), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/places")
def places():
    return render_template("places.html")

@app.route("/add")
def add_page():
    return render_template("add.html")



@app.route("/all_places", methods=["GET"])
def all_places():
    places = db.session.execute(db.select(Place)).scalars().all()
    if not places:
        return jsonify(error="No places found"), 404
    return jsonify(places=[place.to_dict() for place in places])

@app.route("/places/<int:place_id>", methods=["GET"])
def get_place(place_id):
    place = db.get_or_404(Place, place_id)
    return jsonify(place=place.to_dict())

@app.route("/random", methods=["GET"])
def get_random_place():
    places = db.session.execute(db.select(Place)).scalars().all()
    if not places:
        return jsonify(error="No places found"), 404
    random_place = random.choice(places)
    return jsonify(place=random_place.to_dict())

@app.route("/add_place", methods=["POST"])
def add_place():
    data = request.get_json()
    if not data:
        return jsonify(error="Missing JSON data"), 400

    try:
        new_place = Place(
            name=data["name"],
            city=data["city"],
            country=data["country"],
            location=data["location"],
            open=data["open"],
            close=data["close"],
            rating=data["rating"],
            review=data["review"]
        )
        db.session.add(new_place)
        db.session.commit()
    except KeyError as e:
        return jsonify(error=f"Missing field: {str(e)}"), 400
    except Exception as e:
        return jsonify(error=str(e)), 400

    return jsonify(message="Successfully added new place", place=new_place.to_dict()), 201

@app.route("/places/<int:place_id>", methods=["PUT"])
def update_place_put(place_id):
    place = db.get_or_404(Place, place_id)
    data = request.get_json()
    required_fields = ["name", "city", "country", "location", "open", "close", "rating", "review"]
    if not data or not all(field in data for field in required_fields):
        return jsonify(error=f"Missing fields: {required_fields}"), 400

    for field in required_fields:
        setattr(place, field, data[field])

    db.session.commit()
    return jsonify(message="Place updated successfully (PUT)", place=place.to_dict())

@app.route("/places/<int:place_id>", methods=["PATCH"])
def update_place_patch(place_id):
    place = db.get_or_404(Place, place_id)
    data = request.get_json()
    if not data:
        return jsonify(error="No data provided for update"), 400

    for field in ["name", "city", "country", "location", "open", "close", "rating", "review"]:
        if field in data:
            setattr(place, field, data[field])

    db.session.commit()
    return jsonify(message="Place updated successfully (PATCH)", place=place.to_dict())

@app.route("/places/<int:place_id>", methods=["DELETE"])
def delete_place(place_id):
    place = db.get_or_404(Place, place_id)
    db.session.delete(place)
    db.session.commit()
    return jsonify(message=f"Place with ID {place_id} deleted successfully")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
