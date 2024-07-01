from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from flask_jwt_extended import JWTManager, create_access_token # type: ignore
from flask_socketio import SocketIO # type: ignore
import threading
import time

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['JWT_SECRET_KEY'] = 'your-secret-key'

# In-memory database for demonstration
users = {
    "professor": bcrypt.generate_password_hash("password").decode('utf-8')
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users and bcrypt.check_password_hash(users[username], password):
        access_token = create_access_token(identity=username)
        return jsonify(token=access_token)
    else:
        return jsonify(message="Invalid credentials"), 401

@socketio.on('connect')
def handle_connect():
    print('Client connected')

def send_data():
    # Example function to send dummy coordinates
    while True:
        coordinates = {'lat': 37.7749, 'lng': -122.4194}  # Dummy coordinates (San Francisco)
        socketio.emit('coordinates', coordinates, namespace='/ws')
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=send_data).start()
    socketio.run(app, host='0.0.0.0', port=5000)
