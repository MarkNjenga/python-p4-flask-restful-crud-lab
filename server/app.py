from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from models import Plant, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant_by_id(id):
    plant = Plant.query.get(id)
    if plant:
        return jsonify({
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price,
            'is_in_stock': plant.is_in_stock
        }), 200
    else:
        abort(404, description="Plant not found")

@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        abort(404, description="Plant not found")
    
    data = request.get_json()
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]
        db.session.commit()
        return jsonify({
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price,
            'is_in_stock': plant.is_in_stock
        }), 200

    return jsonify({"error": "Invalid input"}), 400


@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        abort(404, description="Plant not found")
    
    db.session.delete(plant)
    db.session.commit()
    
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
