from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import Config
from routes.auth import init_auth_routes, token_required
from routes.rooms import init_rooms_routes
from routes.bookings import init_bookings_routes
from routes.feedback import init_feedback_routes
from models.booking_model import Booking
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize CORS
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# Initialize MongoDB
mongo = PyMongo(app)
db = mongo.db

# Initialize routes
auth_bp = init_auth_routes(db, app)
rooms_bp = init_rooms_routes(db, app)
bookings_bp = init_bookings_routes(db, app)
feedback_bp = init_feedback_routes(db, app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(rooms_bp, url_prefix='/api')
app.register_blueprint(bookings_bp, url_prefix='/api')
app.register_blueprint(feedback_bp, url_prefix='/api')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'EaseStay API is running',
        'database': 'connected' if mongo.db else 'disconnected'
    }), 200

# User login log endpoint
@app.route('/api/user/login-log', methods=['POST'])
@token_required
def log_user_login(current_user):
    try:
        data = request.get_json()
        
        login_log = {
            'user_id': current_user['user_id'],
            'email': data.get('email', current_user.get('email', '')),
            'role': data.get('role', current_user.get('role', 'guest')),
            'login_time': datetime.utcnow(),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        db.user_login_logs.insert_one(login_log)
        
        return jsonify({
            'message': 'Login logged successfully',
            'login_time': login_log['login_time'].isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User preferences endpoint
@app.route('/api/user/preferences', methods=['POST'])
@token_required
def save_user_preferences(current_user):
    try:
        data = request.get_json()
        
        preferences = {
            'user_id': current_user['user_id'],
            'checkin_date': data.get('checkin_date'),
            'checkout_date': data.get('checkout_date'),
            'updated_at': datetime.utcnow()
        }
        
        # Add login_time if provided
        if data.get('login_time'):
            preferences['login_time'] = datetime.utcnow()
        
        # Update or insert preferences
        db.user_preferences.update_one(
            {'user_id': current_user['user_id']},
            {'$set': preferences},
            upsert=True
        )
        
        # Convert datetime to string for JSON serialization
        preferences_serialized = {
            'user_id': preferences['user_id'],
            'checkin_date': preferences['checkin_date'],
            'checkout_date': preferences['checkout_date'],
            'updated_at': preferences['updated_at'].isoformat()
        }
        if 'login_time' in preferences:
            preferences_serialized['login_time'] = preferences['login_time'].isoformat()
        
        return jsonify({
            'message': 'Preferences saved successfully',
            'preferences': preferences_serialized
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payment endpoint
@app.route('/api/payment', methods=['POST'])
@token_required
def process_payment(current_user):
    try:
        from bson import ObjectId
        from models.room_model import Room
        
        data = request.get_json()
        
        booking_id = data.get('booking_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method', 'card')
        
        if not booking_id or not amount:
            return jsonify({'error': 'Booking ID and amount are required'}), 400
        
        # Update booking payment status
        booking_model = Booking(db.bookings)
        booking = booking_model.get_booking_by_id(booking_id)
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Update booking status to confirmed
        success = booking_model.update_booking_status(booking_id, 'confirmed')
        
        if success:
            # Update room status to occupied
            room_model = Room(db.rooms)
            room_id = booking.get('room_id')
            # Convert ObjectId to string if needed
            if isinstance(room_id, ObjectId):
                room_id = str(room_id)
            room_model.update_room_status(room_id, 'occupied')
            
            # Record payment
            payment_data = {
                'booking_id': str(ObjectId(booking_id)) if isinstance(booking_id, ObjectId) else str(booking_id),
                'user_id': str(current_user['user_id']) if isinstance(current_user['user_id'], ObjectId) else str(current_user['user_id']),
                'amount': float(amount),
                'payment_method': payment_method,
                'status': 'completed',
                'created_at': datetime.utcnow()
            }
            
            db.payments.insert_one(payment_data)
            
            # Convert payment_data ObjectId to string for JSON serialization
            payment_data['_id'] = str(payment_data['_id'])
            
            return jsonify({
                'message': 'Room booked successfully',
                'payment': payment_data
            }), 200
        else:
            return jsonify({'error': 'Failed to process payment'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting EaseStay Flask Server...")
    print(f"MongoDB URI: {Config.MONGO_URI}")
    print("API endpoints available at http://localhost:5000/api")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)