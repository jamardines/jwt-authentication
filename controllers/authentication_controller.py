from flask import Blueprint, request, jsonify, current_app
import logging

auth_bp = Blueprint('auth_bp', __name__)
logger = logging.getLogger(__name__)

VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No input data provided'}), 400

        username = data.get('username')
        password = data.get('password')
        client_ip = request.remote_addr

        if not username or not password:
            logger.info("Login ATTEMPT - missing credentials - ip=%s username=%s", client_ip, username)
            return jsonify({'message': 'Username and password are required'}), 400

        # Validate against static values
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            logger.info("Login SUCCESS - user=%s ip=%s", username, client_ip)
            return jsonify({
                "message": "Login successful",
                "user": username
            }), 200

        logger.warning("Login FAILED - invalid credentials - user=%s ip=%s", username, client_ip)
        return jsonify({"message": "Invalid username or password"}), 401

    except Exception as e:
        logger.exception("Login error")
        return jsonify({'message': str(e)}), 400