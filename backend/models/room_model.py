from datetime import datetime
from bson import ObjectId

class Room:
    def __init__(self, db_collection):
        self.collection = db_collection
    
    def create_room(self, room_data):
        """Create a new room"""
        room_data['created_at'] = datetime.utcnow()
        room_data['status'] = room_data.get('status', 'available')
        
        result = self.collection.insert_one(room_data)
        room_data['_id'] = result.inserted_id
        return room_data
    
    def get_all_rooms(self):
        """Get all rooms"""
        rooms = list(self.collection.find({}))
        return rooms
    
    def get_available_rooms(self, checkin_date=None, checkout_date=None):
        """Get available rooms, optionally filtered by date range"""
        query = {'status': 'available'}
        
        if checkin_date and checkout_date:
            # Check for bookings that overlap with the requested dates
            # This would require checking bookings collection
            pass
        
        rooms = list(self.collection.find(query))
        return rooms
    
    def get_room_by_id(self, room_id):
        """Get room by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(room_id)})
        except:
            return None
    
    def update_room_status(self, room_id, status):
        """Update room status"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(room_id)},
                {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def update_room(self, room_id, update_data):
        """Update room information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(room_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def mark_room_needs_cleaning(self, room_id):
        """Mark a room as needing cleaning"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(room_id)},
                {'$set': {'needs_cleaning': True, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def mark_room_clean(self, room_id):
        """Mark a room as cleaned"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(room_id)},
                {'$set': {'needs_cleaning': False, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def get_rooms_needing_cleaning(self):
        """Get all rooms that need cleaning"""
        rooms = list(self.collection.find({'needs_cleaning': True}))
        return rooms

