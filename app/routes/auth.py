# app/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models import User
from app.services.auth_service import register_user, authenticate_user, initiate_password_reset, reset_password
from app.utils.validators import validate_registration_data

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    referral_code = data.get('referral_code')

    # Validate input data
    is_valid, errors = validate_registration_data(username, email, password)
    if not is_valid:
        return jsonify({'success': False, 'errors': errors}), 400

    # Register user
    try:
        user = register_user(username, email, password, referral_code)

        # Generate JWT token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'referral_code': user.referral_code
            }
        }), 201

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400  # <-- Return 400 for validation errors

    except Exception as e:
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500  # Generic server error

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    
    # Authenticate user
    user = authenticate_user(username_or_email, password)
    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'referral_code': user.referral_code
        }
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    # Initiate password reset
    success = initiate_password_reset(email)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Password reset instructions sent to your email'
        }), 200
    else:
        # Don't reveal if email exists or not for security
        return jsonify({
            'success': True,
            'message': 'If this email is registered, password reset instructions will be sent'
        }), 200

@auth_bp.route('/reset-password', methods=['POST'])
def handle_reset_password():
    data = request.get_json()
    
    token = data.get('token')
    new_password = data.get('new_password')
    
    # Validate password strength
    from app.utils.validators import validate_password_strength
    is_valid, password_error = validate_password_strength(new_password)
    
    if not is_valid:
        return jsonify({'success': False, 'message': password_error}), 400
    
    # Reset password
    success = reset_password(token, new_password)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Password reset successful'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid or expired token'
        }), 400

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'referral_code': user.referral_code
        }
    }), 200