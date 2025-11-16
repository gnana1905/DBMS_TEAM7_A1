from flask import Blueprint, request, jsonify
from models.booking_model import Booking
from models.room_model import Room
from routes.auth import token_required, admin_required
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

def init_bookings_routes(db, app):
    """Initialize bookings routes with database connection"""
    booking_model = Booking(db.bookings)
    room_model = Room(db.rooms)
    
    @bookings_bp.route('/book', methods=['POST'])
    @token_required
    def create_booking(current_user):
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['room_id', 'checkin_date', 'checkout_date', 'guests']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            room_id = data['room_id']
            checkin_date = data['checkin_date']
            checkout_date = data['checkout_date']
            
            # Validate dates
            checkin = datetime.strptime(checkin_date, '%Y-%m-%d')
            checkout = datetime.strptime(checkout_date, '%Y-%m-%d')
            
            if checkin >= checkout:
                return jsonify({'error': 'Check-out date must be after check-in date'}), 400
            
            if checkin < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                return jsonify({'error': 'Check-in date cannot be in the past'}), 400
            
            # Check if room exists
            room = room_model.get_room_by_id(room_id)
            if not room:
                return jsonify({'error': 'Room not found'}), 404
            
            # Check if room is available
            if room.get('status') != 'available':
                return jsonify({'error': 'Room is not available'}), 400
            
            # Check for overlapping bookings
            if not booking_model.check_room_availability(room_id, checkin_date, checkout_date):
                return jsonify({'error': 'Room is already booked for these dates'}), 400
            
            # Calculate total price
            nights = (checkout - checkin).days
            price_per_night = room.get('price', 0)
            total_price = nights * price_per_night
            
            # Create booking
            booking_data = {
                'user_id': current_user['user_id'],
                'room_id': room_id,
                'room_number': room.get('roomNumber', ''),
                'room_name': room.get('name', ''),
                'checkin_date': checkin_date,
                'checkout_date': checkout_date,
                'guests': data['guests'],
                'rooms': data.get('rooms', 1),
                'price_per_night': price_per_night,
                'total_price': total_price,
                'status': 'pending',
                'payment_status': 'pending'
            }
            
            booking = booking_model.create_booking(booking_data)
            booking['_id'] = str(booking['_id'])
            
            return jsonify({
                'message': 'Booking created successfully',
                'booking': booking
            }), 201
            
        except ValueError as e:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @bookings_bp.route('/bookings', methods=['GET'])
    @token_required
    def get_user_bookings(current_user):
        try:
            from bson import ObjectId
            
            bookings = booking_model.get_user_bookings(current_user['user_id'])
            
            # Convert ObjectId to string and populate room details
            for booking in bookings:
                # Convert all ObjectId fields to strings
                if '_id' in booking:
                    booking['_id'] = str(booking['_id'])
                if 'room_id' in booking and isinstance(booking['room_id'], ObjectId):
                    booking['room_id'] = str(booking['room_id'])
                if 'user_id' in booking and isinstance(booking['user_id'], ObjectId):
                    booking['user_id'] = str(booking['user_id'])
                
                room = room_model.get_room_by_id(booking.get('room_id'))
                if room:
                    booking['room_details'] = {
                        'name': room.get('name'),
                        'image': room.get('image'),
                        'roomNumber': room.get('roomNumber')
                    }
            
            return jsonify({
                'bookings': bookings,
                'count': len(bookings)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @bookings_bp.route('/bookings/all', methods=['GET'])
    @token_required
    @admin_required
    def get_all_bookings(current_user):
        try:
            from bson import ObjectId
            from models.user_model import User
            
            bookings = booking_model.get_all_bookings()
            user_model = User(db.users)
            
            # Convert ObjectId to string and populate user details
            for booking in bookings:
                booking['_id'] = str(booking['_id'])
                if 'room_id' in booking and isinstance(booking['room_id'], ObjectId):
                    booking['room_id'] = str(booking['room_id'])
                if 'user_id' in booking:
                    user_id = booking['user_id']
                    if isinstance(user_id, ObjectId):
                        user_id = str(user_id)
                    # Get user details
                    user = user_model.find_by_id(user_id)
                    if user:
                        booking['user_details'] = {
                            'email': user.get('email', ''),
                            'firstName': user.get('firstName', ''),
                            'lastName': user.get('lastName', ''),
                            'phone': user.get('phone', '')
                        }
                    booking['user_id'] = user_id
                
                # Populate room details
                room = room_model.get_room_by_id(booking.get('room_id'))
                if room:
                    booking['room_details'] = {
                        'name': room.get('name'),
                        'image': room.get('image'),
                        'roomNumber': room.get('roomNumber')
                    }
            
            return jsonify({
                'bookings': bookings,
                'count': len(bookings)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @bookings_bp.route('/booking/<booking_id>', methods=['DELETE'])
    @token_required
    def delete_booking(current_user, booking_id):
        try:
            # Get booking to verify ownership
            booking = booking_model.get_booking_by_id(booking_id)
            if not booking:
                return jsonify({'error': 'Booking not found'}), 404
            
            # Check if booking belongs to user (unless admin)
            user_id = current_user['user_id']
            if isinstance(booking.get('user_id'), str):
                booking_user_id = booking.get('user_id')
            else:
                from bson import ObjectId
                booking_user_id = str(booking.get('user_id'))
            
            # Only allow deletion if:
            # 1. Booking belongs to the user AND status is pending
            # 2. OR user is admin
            if current_user.get('role') != 'admin':
                if booking_user_id != user_id:
                    return jsonify({'error': 'Unauthorized'}), 403
                if booking.get('status') != 'pending':
                    return jsonify({'error': 'Only pending bookings can be deleted'}), 400
            
            # Delete booking
            success = booking_model.delete_booking(booking_id, user_id if current_user.get('role') != 'admin' else None)
            
            if success:
                # If booking was confirmed, update room status back to available
                if booking.get('status') == 'confirmed':
                    room_id = booking.get('room_id')
                    if isinstance(room_id, ObjectId):
                        room_id = str(room_id)
                    room_model.update_room_status(room_id, 'available')
                
                return jsonify({
                    'message': 'Booking deleted successfully'
                }), 200
            else:
                return jsonify({'error': 'Failed to delete booking'}), 500
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return bookings_bp

