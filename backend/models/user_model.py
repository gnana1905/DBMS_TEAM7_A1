from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, db_collection):
        self.collection = db_collection
    
    def create_user(self, user_data):
        """Create a new user"""
        user_data['password'] = generate_password_hash(user_data['password'])
        user_data['created_at'] = datetime.utcnow()
        user_data['role'] = user_data.get('role', 'guest')
        
        result = self.collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        user_data.pop('password', None)  # Remove password from return
        return user_data
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        from bson import ObjectId
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def verify_password(self, user, password):
        """Verify user password"""
        if user and 'password' in user:
            return check_password_hash(user['password'], password)
        return False
    
    def get_all_users(self):
        """Get all users (for admin)"""
        users = list(self.collection.find({}, {'password': 0}))
        return users
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        from bson import ObjectId
        if 'password' in update_data:
            update_data['password'] = generate_password_hash(update_data['password'])
        
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

