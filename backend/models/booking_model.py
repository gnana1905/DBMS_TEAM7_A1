from datetime import datetime
from bson import ObjectId

class Booking:
    def __init__(self, db_collection):
        self.collection = db_collection
    
    def create_booking(self, booking_data):
        """Create a new booking"""
        booking_data['created_at'] = datetime.utcnow()
        booking_data['status'] = booking_data.get('status', 'pending')
        
        result = self.collection.insert_one(booking_data)
        booking_data['_id'] = result.inserted_id
        return booking_data
    
    def get_booking_by_id(self, booking_id):
        """Get booking by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(booking_id)})
        except:
            return None
    
    def get_user_bookings(self, user_id):
        """Get all bookings for a user"""
        try:
            bookings = list(self.collection.find({'user_id': user_id}).sort('created_at', -1))
            return bookings
        except:
            return []
    
    def get_all_bookings(self):
        """Get all bookings (for admin)"""
        bookings = list(self.collection.find({}).sort('created_at', -1))
        return bookings
    
    def check_room_availability(self, room_id, checkin_date, checkout_date):
        """Check if room is available for given dates"""
        from datetime import datetime
        
        checkin = datetime.strptime(checkin_date, '%Y-%m-%d')
        checkout = datetime.strptime(checkout_date, '%Y-%m-%d')
        
        # Find overlapping bookings
        # A booking overlaps if:
        # - checkin_date is before checkout AND checkout_date is after checkin
        overlapping = self.collection.find_one({
            'room_id': room_id,
            'status': {'$in': ['confirmed', 'pending']},
            '$or': [
                {
                    'checkin_date': {'$lte': checkout_date},
                    'checkout_date': {'$gte': checkin_date}
                }
            ]
        })
        
        return overlapping is None
    
    def update_booking_status(self, booking_id, status):
        """Update booking status"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.utcnow()
            }
            
            # If status is confirmed, also update payment_status
            if status == 'confirmed':
                update_data['payment_status'] = 'completed'
            
            result = self.collection.update_one(
                {'_id': ObjectId(booking_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_booking(self, booking_id, user_id=None):
        """Delete a booking. If user_id is provided, only delete if booking belongs to that user."""
        try:
            query = {'_id': ObjectId(booking_id)}
            
            # If user_id is provided, ensure booking belongs to that user
            if user_id:
                query['user_id'] = user_id
            
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except:
            return False

