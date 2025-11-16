from flask import Blueprint, request, jsonify
from routes.auth import token_required
from datetime import datetime
from bson import ObjectId

feedback_bp = Blueprint('feedback', __name__)

def init_feedback_routes(db, app):
    """Initialize feedback routes with database connection"""
    
    @feedback_bp.route('/feedback', methods=['POST'])
    @token_required
    def submit_feedback(current_user):
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('rating') or not data.get('comment'):
                return jsonify({'error': 'Rating and comment are required'}), 400
            
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
            
            # Create feedback document
            feedback_data = {
                'user_id': current_user['user_id'],
                'user_email': current_user['email'],
                'booking_id': data.get('booking_id'),
                'rating': rating,
                'comment': data['comment'],
                'created_at': datetime.utcnow()
            }
            
            result = db.feedback.insert_one(feedback_data)
            feedback_data['_id'] = str(result.inserted_id)
            
            return jsonify({
                'message': 'Feedback submitted successfully',
                'feedback': feedback_data
            }), 201
            
        except ValueError:
            return jsonify({'error': 'Invalid rating value'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @feedback_bp.route('/feedback', methods=['GET'])
    def get_feedback():
        try:
            feedbacks = list(db.feedback.find({}).sort('created_at', -1).limit(50))
            
            # Convert ObjectId to string
            for feedback in feedbacks:
                feedback['_id'] = str(feedback['_id'])
            
            return jsonify({
                'feedback': feedbacks,
                'count': len(feedbacks)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return feedback_bp

