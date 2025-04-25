from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Get database connection details from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}/{os.environ['MYSQL_DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Agent model
class Agent(db.Model):
    __tablename__ = 'agents'
    agent_id = db.Column(db.Integer, primary_key=True)
    agent_code = db.Column(db.String(255), nullable=False)
    agent_name = db.Column(db.String(255), nullable=False)
    agent_email = db.Column(db.String(255), nullable=False)
    agent_phone = db.Column(db.String(20), nullable=False)

# Define routes

# Endpoint to get all agents
@app.route('/agents', methods=['GET'])
def get_agents():
    agents = Agent.query.all()
    return jsonify([{
        'agent_id': agent.agent_id,
        'agent_code': agent.agent_code,
        'agent_name': agent.agent_name,
        'agent_email': agent.agent_email,
        'agent_phone': agent.agent_phone
    } for agent in agents])

# Endpoint to create a new agent
@app.route('/agents', methods=['POST'])
def create_agent():
    data = request.get_json()
    new_agent = Agent(
        agent_code=data['agent_code'],
        agent_name=data['agent_name'],
        agent_email=data['agent_email'],
        agent_phone=data['agent_phone']
    )
    db.session.add(new_agent)
    db.session.commit()
    return jsonify({'message': 'Agent created'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
