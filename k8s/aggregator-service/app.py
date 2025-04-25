from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Get database connection details from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}/{os.environ['MYSQL_DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Aggregator model
class Aggregator(db.Model):
    __tablename__ = 'aggregators'
    aggregator_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

# Define routes

# Endpoint to get all aggregators
@app.route('/aggregators', methods=['GET'])
def get_aggregators():
    aggregators = Aggregator.query.all()
    return jsonify([{
        'aggregator_id': aggregator.aggregator_id,
        'name': aggregator.name,
        'description': aggregator.description
    } for aggregator in aggregators])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
