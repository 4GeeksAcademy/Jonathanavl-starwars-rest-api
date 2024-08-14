from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_characters = db.Table('favorite_characters',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
)

favorite_planets = db.Table('favorite_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'))
)

favorite_vehicles = db.Table('favorite_vehicles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    favorite_characters = db.relationship('Character', secondary=favorite_characters, backref=db.backref('users_with_favorites', lazy='dynamic'))
    favorite_planets = db.relationship('Planet', secondary=favorite_planets, backref=db.backref('users_with_favorites', lazy='dynamic'))
    favorite_vehicles = db.relationship('Vehicle', secondary=favorite_vehicles, backref=db.backref('users_with_favorites', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email
    def serialize(self):
        return {
            "id": self.id,
            "username": self.user_name,
            "email": self.email,
        }
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    population = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "homeworld": self.homeworld
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250))
    hp = db.Column(db.Integer)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "hp": self.hp
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('favorite_characters_relation', cascade='all, delete-orphan'))
    character = db.relationship('Character', backref=db.backref('favorite_characters_relation', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<FavoriteCharacter user_id={self.user_id} character_id={self.character_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character": self.character.serialize()
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('favorite_planets_relation', cascade='all, delete-orphan'))
    planet = db.relationship('Planet', backref=db.backref('favorite_planets_relation', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<FavoritePlanet user_id={self.user_id} planet_id={self.planet_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet": self.planet.serialize()
        }

class FavoriteVehicle(db.Model):
    __tablename__ = 'favorite_vehicle'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), primary_key=True)
    
    user = db.relationship('User', backref=db.backref('favorite_vehicles_relation', cascade='all, delete-orphan'))
    vehicle = db.relationship('Vehicle', backref=db.backref('favorite_vehicles_relation', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<FavoriteVehicle user_id={self.user_id} vehicle_id={self.vehicle_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "vehicle": self.vehicle.serialize()
        }
