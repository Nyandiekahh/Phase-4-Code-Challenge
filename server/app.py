from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        hero_dict = hero.to_dict()
        hero_dict['powers'] = [hp.power.to_dict() for hp in hero.hero_powers]
        return jsonify(hero_dict)
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    else:
        return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    description = data.get('description')
    if description:
        try:
            power.description = description
            db.session.commit()
            return jsonify(power.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400
    return jsonify({"errors": ["validation errors"]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    
    if not strength or strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["validation errors"]}), 400
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    
    if not hero or not power:
        return jsonify({"errors": ["validation errors"]}), 400
    
    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()
    
    return jsonify(hero.to_dict()), 200

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)