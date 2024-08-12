import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Vehicle, FavoritePlanet, FavoriteCharacter, FavoriteVehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters])

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get_or_404(character_id)
    return jsonify(character.serialize())

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.serialize())

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles])

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(vehicle.serialize())

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorite_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()
    favorite_characters = FavoriteCharacter.query.filter_by(user_id=user_id).all()
    favorite_vehicles = FavoriteVehicle.query.filter_by(user_id=user_id).all()
    return jsonify({
        'planets': [Planet.query.get(fav.planet_id).serialize() for fav in favorite_planets],
        'characters': [Character.query.get(fav.character_id).serialize() for fav in favorite_characters],
        'vehicles': [Vehicle.query.get(fav.vehicle_id).serialize() for fav in favorite_vehicles]
    })

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Supongamos que el usuario actual tiene id = 1
    new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet added successfully'})

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = 1 
    new_favorite = FavoriteCharacter(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite character added successfully'})

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = 1  # Supongamos que el usuario actual tiene id = 1
    new_favorite = FavoriteVehicle(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite vehicle added successfully'})

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1 
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'message': 'Favorite not found'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet deleted successfully'})

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = 1 
    favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({'message': 'Favorite not found'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite character deleted successfully'})

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = 1 
    favorite = FavoriteVehicle.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if not favorite:
        return jsonify({'message': 'Favorite not found'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite vehicle deleted successfully'})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
