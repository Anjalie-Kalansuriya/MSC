import os
import requests
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

# Get database configuration from environment variables
DB_HOST = os.environ.get("DB_HOST", "mysql-service")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

# External API URL
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/users"

def get_external_data():
    try:
        response = requests.get(EXTERNAL_API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        app.logger.error(f"Error fetching external data: {e}")
        return []

def store_data_in_db(data):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS external_users (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)

        for user in data:
            cursor.execute("""
                INSERT INTO external_users (id, name, email)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE name=%s, email=%s
            """, (user['id'], user['name'], user['email'], user['name'], user['email']))

        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        app.logger.error(f"MySQL error: {e}")

@app.route("/integrate", methods=["GET"])
def integrate():
    data = get_external_data()
    if data:
        store_data_in_db(data)
        return jsonify({"message": "Data integrated successfully"}), 200
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
