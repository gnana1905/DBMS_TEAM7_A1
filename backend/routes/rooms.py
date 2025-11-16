from flask import Blueprint, request, jsonify
from models.room_model import Room
from routes.auth import token_required, admin_required

rooms_bp = Blueprint('rooms', __name__)

def init_rooms_routes(db, app):
    """Initialize rooms routes with database connection"""
    room_model = Room(db.rooms)
    
    @rooms_bp.route('/rooms', methods=['GET'])
    def get_rooms():
        try:
            rooms = room_model.get_all_rooms()
            
            # Convert ObjectId to string
            for room in rooms:
                room['_id'] = str(room['_id'])
            
            return jsonify({
                'rooms': rooms,
                'count': len(rooms)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @rooms_bp.route('/rooms/available', methods=['GET'])
    def get_available_rooms():
        try:
            checkin_date = request.args.get('checkin')
            checkout_date = request.args.get('checkout')
            
            rooms = room_model.get_available_rooms(checkin_date, checkout_date)
            
            # Convert ObjectId to string
            for room in rooms:
                room['_id'] = str(room['_id'])
            
            return jsonify({
                'rooms': rooms,
                'count': len(rooms)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @rooms_bp.route('/room/<room_id>/status', methods=['PUT'])
    @token_required
    @admin_required
    def update_room_status(current_user, room_id):
        try:
            data = request.get_json()
            status = data.get('status')
            
            if not status or status not in ['available', 'occupied', 'maintenance']:
                return jsonify({'error': 'Invalid status. Must be: available, occupied, or maintenance'}), 400
            
            success = room_model.update_room_status(room_id, status)
            
            if success:
                room = room_model.get_room_by_id(room_id)
                if room:
                    room['_id'] = str(room['_id'])
                    return jsonify({
                        'message': 'Room status updated successfully',
                        'room': room
                    }), 200
                else:
                    return jsonify({'error': 'Room not found'}), 404
            else:
                return jsonify({'error': 'Failed to update room status'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @rooms_bp.route('/room/<room_id>/cleaning', methods=['PUT'])
    @token_required
    @admin_required
    def mark_room_for_cleaning(current_user, room_id):
        """Admin can mark a room as needing cleaning"""
        try:
            # Mark room for cleaning and set status to maintenance if not already
            room = room_model.get_room_by_id(room_id)
            if not room:
                return jsonify({'error': 'Room not found'}), 404
            
            # Update needs_cleaning flag
            success = room_model.mark_room_needs_cleaning(room_id)
            
            # If room is not already in maintenance, set it to maintenance
            if room.get('status') != 'maintenance':
                room_model.update_room_status(room_id, 'maintenance')
            
            if success:
                room = room_model.get_room_by_id(room_id)
                if room:
                    room['_id'] = str(room['_id'])
                    return jsonify({
                        'message': 'Room marked for cleaning',
                        'room': room
                    }), 200
                else:
                    return jsonify({'error': 'Room not found'}), 404
            else:
                return jsonify({'error': 'Failed to mark room for cleaning'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @rooms_bp.route('/rooms/cleaning', methods=['GET'])
    @token_required
    def get_rooms_needing_cleaning(current_user):
        """Get all rooms that need cleaning (for staff) - includes maintenance and needs_cleaning"""
        try:
            # Get rooms that need cleaning OR are in maintenance status
            # Staff should see both rooms marked for cleaning and rooms in maintenance
            from bson import ObjectId
            
            # Query for rooms that need cleaning OR are in maintenance
            query = {
                '$or': [
                    {'needs_cleaning': True},
                    {'status': 'maintenance'}
                ]
            }
            
            rooms_list = list(room_model.collection.find(query))
            
            # Convert ObjectId to string
            for room in rooms_list:
                room['_id'] = str(room['_id'])
            
            return jsonify({
                'rooms': rooms_list,
                'count': len(rooms_list)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @rooms_bp.route('/room/<room_id>/clean', methods=['PUT'])
    @token_required
    def mark_room_clean(current_user, room_id):
        """Staff can mark a room as cleaned"""
        try:
            success = room_model.mark_room_clean(room_id)
            
            if success:
                room = room_model.get_room_by_id(room_id)
                if room:
                    room['_id'] = str(room['_id'])
                    return jsonify({
                        'message': 'Room marked as clean',
                        'room': room
                    }), 200
                else:
                    return jsonify({'error': 'Room not found'}), 404
            else:
                return jsonify({'error': 'Failed to mark room as clean'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return rooms_bp

