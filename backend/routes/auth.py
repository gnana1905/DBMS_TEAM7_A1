from flask import Blueprint, request, jsonify
from functools import wraps
from models.user_model import User
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
from config import Config

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(db, app):
    """Initialize auth routes with database connection"""
    user_model = User(db.users)
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['email', 'password', 'firstName', 'lastName']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Check if user already exists
            existing_user = user_model.find_by_email(data['email'])
            if existing_user:
                return jsonify({'error': 'User already exists'}), 400
            
            # Create user
            user_data = {
                'email': data['email'],
                'password': data['password'],
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'phone': data.get('phone', ''),
                'role': data.get('role', 'guest')
            }
            
            user = user_model.create_user(user_data)
            
            # Generate token
            token = generate_token(str(user['_id']), user['role'], user['email'])
            
            return jsonify({
                'message': 'User registered successfully',
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'email': user['email'],
                    'firstName': user['firstName'],
                    'lastName': user['lastName'],
                    'role': user['role']
                }
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            
            if not data or not data.get('email') or not data.get('password'):
                return jsonify({'error': 'Email and password are required'}), 400
            
            # Find user
            user = user_model.find_by_email(data['email'])
            if not user:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Verify password
            if not user_model.verify_password(user, data['password']):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Check role if specified
            if data.get('role') and user.get('role') != data['role']:
                return jsonify({'error': 'Invalid role'}), 403
            
            # Generate token
            token = generate_token(str(user['_id']), user.get('role', 'guest'), user['email'])
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'email': user['email'],
                    'firstName': user.get('firstName', ''),
                    'lastName': user.get('lastName', ''),
                    'role': user.get('role', 'guest')
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return auth_bp

def generate_token(user_id, role, email):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'role': role,
        'email': email,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = {
                'user_id': data['user_id'],
                'role': data['role'],
                'email': data['email']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated

