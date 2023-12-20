from flask import Flask, request, jsonify
from .auth import JWTManager

app = Flask(__name__)

users = {
    'admin@example.com': {'password': 'secret', 'user_id': 123}
}

@app.route('/')
def index():
  return 'Hello, World!'
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users:
        return jsonify({'error': 'Email already registered'}), 400

    user_id = len(users) + 1
    users[email] = {'password': password, 'user_id': user_id}

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email not in users or users[email]['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    user_id = users[email]['user_id']
    token = JWTManager.encode_token({'user_id': user_id})
    return jsonify({'token': token})

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    print("Token recebido:", token)
    if not token:
        return jsonify({'message': 'Token ausente'}), 401

    decoded = JWTManager.decode_token(token)
    if isinstance(decoded, dict):
        user_id = decoded.get('user_id')
        return jsonify({'message': 'Acesso permitido para o usuário {user_id}'}), 200
    else:
        return jsonify({'message': decoded}), 401

if __name__ == '__main__':
    app.run(debug=True)
