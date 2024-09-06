from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    
    # Relationships
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-hero_powers',)

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    # Relationships
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-hero_powers',)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long.')
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, ForeignKey('powers.id'), nullable=False)
    
    # Relationships
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')
    
    # Serialization rules
    serialize_rules = ('-hero', '-power')

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Strength must be one of: Strong, Weak, Average.')
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
