from flask import Flask, jsonify
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/data', methods=['GET'])
def get_data():
    # Sample data to send back to the frontend
    data = {
        "message": "Hello, World!",
        "items": ["Item 1", "Item 2", "Item 3"]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
