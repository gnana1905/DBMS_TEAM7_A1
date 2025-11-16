"""
Seed script to populate MongoDB with sample data
Run this script after starting MongoDB and Flask server
"""
from pymongo import MongoClient
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# MongoDB connection
MONGO_URI = 'mongodb://localhost:27017/easestay'
client = MongoClient(MONGO_URI)
db = client.easestay

def seed_rooms():
    """Seed rooms collection with 45 diverse room types"""
    print("Seeding rooms...")
    
    rooms = [
        {
            'name': 'Luxury King Suite',
            'type': 'suite',
            'price': 7999,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Spacious suite with king bed, city view, and premium amenities',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'Mini Bar', 'TV', 'Ocean View', 'Balcony'],
            'status': 'available',
            'roomNumber': '301',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Double Room',
            'type': 'deluxe',
            'price': 5499,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Comfortable room with double beds and modern amenities',
            'capacity': 3,
            'amenities': ['WiFi', 'AC', 'TV', 'Balcony', 'Work Desk'],
            'status': 'available',
            'roomNumber': '205',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Executive Business Room',
            'type': 'executive',
            'price': 6499,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Perfect for business travelers with work desk and premium WiFi',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Work Desk', 'Coffee Maker', 'Printer'],
            'status': 'available',
            'roomNumber': '412',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Family Suite',
            'type': 'family',
            'price': 8999,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Large suite perfect for families with multiple bedrooms',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', 'Kitchenette', '2 Bathrooms', 'Balcony'],
            'status': 'available',
            'roomNumber': '501',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Premium Ocean View',
            'type': 'premium',
            'price': 9999,
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Luxurious room with stunning ocean views and private balcony',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Ocean View', 'Balcony', 'Mini Bar', 'Jacuzzi'],
            'status': 'available',
            'roomNumber': '201',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Standard Single Room',
            'type': 'standard',
            'price': 2999,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Comfortable single room for solo travelers',
            'capacity': 1,
            'amenities': ['WiFi', 'AC', 'TV'],
            'status': 'available',
            'roomNumber': '101',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Presidential Suite',
            'type': 'suite',
            'price': 14999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Ultra-luxury suite with separate living area and dining room',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', 'Private Bar', 'Jacuzzi', 'Butler Service', 'City View'],
            'status': 'available',
            'roomNumber': '701',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Honeymoon Suite',
            'type': 'suite',
            'price': 11999,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Romantic suite with heart-shaped bed and champagne service',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Jacuzzi', 'Romantic Decor', 'Room Service', 'Ocean View'],
            'status': 'available',
            'roomNumber': '601',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Twin Room',
            'type': 'deluxe',
            'price': 5999,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Spacious room with two twin beds',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Balcony', 'Mini Fridge'],
            'status': 'available',
            'roomNumber': '206',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Superior Room',
            'type': 'superior',
            'price': 4499,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Well-appointed room with modern amenities',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Work Desk'],
            'status': 'available',
            'roomNumber': '102',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Garden View Room',
            'type': 'standard',
            'price': 3999,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Peaceful room overlooking the hotel gardens',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Garden View', 'Balcony'],
            'status': 'available',
            'roomNumber': '103',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Penthouse Suite',
            'type': 'suite',
            'price': 17999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Exclusive top-floor suite with panoramic city views',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', 'Private Terrace', 'Jacuzzi', 'Butler Service', '360° View'],
            'status': 'available',
            'roomNumber': '801',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Triple Room',
            'type': 'deluxe',
            'price': 6999,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Spacious room with three beds for families',
            'capacity': 3,
            'amenities': ['WiFi', 'AC', 'TV', 'Balcony', 'Sofa'],
            'status': 'available',
            'roomNumber': '207',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Junior Suite',
            'type': 'suite',
            'price': 8499,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Comfortable suite with separate sitting area',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Sitting Area', 'Mini Bar', 'City View'],
            'status': 'available',
            'roomNumber': '302',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Executive Suite',
            'type': 'suite',
            'price': 10999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Luxurious suite with dedicated workspace and premium amenities',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Office Space', 'Meeting Table', 'Printer', 'Coffee Maker'],
            'status': 'available',
            'roomNumber': '413',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Standard Double Room',
            'type': 'standard',
            'price': 3499,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Comfortable double room with essential amenities',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV'],
            'status': 'available',
            'roomNumber': '104',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Ocean Front Suite',
            'type': 'suite',
            'price': 12999,
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Exclusive suite directly facing the ocean with private balcony',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Ocean Front', 'Private Balcony', 'Jacuzzi', 'Mini Bar'],
            'status': 'available',
            'roomNumber': '202',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe King Room',
            'type': 'deluxe',
            'price': 6299,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Spacious room with king-size bed and premium amenities',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Balcony', 'Mini Bar', 'Work Desk'],
            'status': 'available',
            'roomNumber': '208',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Corner Suite',
            'type': 'suite',
            'price': 9499,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Unique corner suite with windows on two sides',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Corner View', 'Balcony', 'Sitting Area'],
            'status': 'available',
            'roomNumber': '303',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Premium King Room',
            'type': 'premium',
            'price': 7499,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Premium room with king bed and city skyline view',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'City View', 'Balcony', 'Mini Bar', 'Work Desk'],
            'status': 'available',
            'roomNumber': '209',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Grand Family Suite',
            'type': 'suite',
            'price': 13999,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Extra-large suite with multiple bedrooms for large families',
            'capacity': 6,
            'amenities': ['WiFi', 'AC', 'TV', '3 Bedrooms', 'Kitchenette', '2 Bathrooms', 'Living Room'],
            'status': 'available',
            'roomNumber': '502',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Studio Apartment',
            'type': 'apartment',
            'price': 4999,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Self-contained studio with kitchenette and living area',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Kitchenette', 'Dining Area', 'Work Desk'],
            'status': 'available',
            'roomNumber': '105',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Queen Room',
            'type': 'deluxe',
            'price': 5799,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Elegant room with queen-size bed and modern decor',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Balcony', 'Mini Fridge'],
            'status': 'available',
            'roomNumber': '210',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Royal Suite',
            'type': 'suite',
            'price': 16999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Opulent suite with royal treatment and premium services',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', 'Private Dining', 'Jacuzzi', 'Butler Service', 'Royal Decor'],
            'status': 'available',
            'roomNumber': '702',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Standard Twin Room',
            'type': 'standard',
            'price': 3299,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Comfortable room with two twin beds',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV'],
            'status': 'available',
            'roomNumber': '106',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Studio',
            'type': 'deluxe',
            'price': 5299,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Modern studio with kitchenette and living space',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Kitchenette', 'Dining Table', 'Work Desk'],
            'status': 'available',
            'roomNumber': '211',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Premium Suite with Terrace',
            'type': 'suite',
            'price': 11499,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Luxurious suite with private rooftop terrace',
            'capacity': 3,
            'amenities': ['WiFi', 'AC', 'TV', 'Private Terrace', 'Jacuzzi', 'Outdoor Seating', 'City View'],
            'status': 'available',
            'roomNumber': '304',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Business Twin Room',
            'type': 'business',
            'price': 6799,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Professional room with twin beds and work setup',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Work Desk', 'Printer', 'Coffee Maker', 'Business Services'],
            'status': 'available',
            'roomNumber': '414',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Family Room',
            'type': 'family',
            'price': 8999,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Spacious family room with connecting doors option',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', 'Sofa Bed', 'Mini Fridge', 'Balcony', 'Family Friendly'],
            'status': 'available',
            'roomNumber': '503',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'City View King Room',
            'type': 'premium',
            'price': 7799,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Premium room with king bed and stunning city skyline views',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'City View', 'Balcony', 'Mini Bar', 'Work Desk'],
            'status': 'available',
            'roomNumber': '212',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Accessible Deluxe Room',
            'type': 'deluxe',
            'price': 5499,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Wheelchair accessible room with all necessary accommodations',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Accessible Bathroom', 'Lowered Surfaces', 'Roll-in Shower'],
            'status': 'available',
            'roomNumber': '107',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Grand Deluxe Suite',
            'type': 'suite',
            'price': 12499,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Expansive suite with separate living and dining areas',
            'capacity': 3,
            'amenities': ['WiFi', 'AC', 'TV', 'Living Room', 'Dining Area', 'Kitchenette', 'Balcony'],
            'status': 'available',
            'roomNumber': '305',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Standard Single with Balcony',
            'type': 'standard',
            'price': 3799,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Single room with private balcony and garden view',
            'capacity': 1,
            'amenities': ['WiFi', 'AC', 'TV', 'Balcony', 'Garden View'],
            'status': 'available',
            'roomNumber': '108',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Executive King Room',
            'type': 'executive',
            'price': 7999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Executive room with king bed and premium business amenities',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Executive Desk', 'Printer', 'Coffee Maker', 'Lounge Access'],
            'status': 'available',
            'roomNumber': '415',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Queen with Jacuzzi',
            'type': 'deluxe',
            'price': 8999,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Romantic room with queen bed and private Jacuzzi',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Jacuzzi', 'Romantic Decor', 'Mini Bar', 'City View'],
            'status': 'available',
            'roomNumber': '213',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Presidential Penthouse',
            'type': 'suite',
            'price': 19999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Ultimate luxury penthouse with panoramic views and butler service',
            'capacity': 6,
            'amenities': ['WiFi', 'AC', 'TV', 'Private Elevator', 'Rooftop Terrace', 'Jacuzzi', 'Butler Service', 'Private Bar', '360° View'],
            'status': 'available',
            'roomNumber': '901',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Standard Double with View',
            'type': 'standard',
            'price': 3999,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Standard room with double bed and scenic views',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Scenic View', 'Balcony'],
            'status': 'available',
            'roomNumber': '109',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Connecting Rooms',
            'type': 'deluxe',
            'price': 10499,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Two connecting deluxe rooms perfect for families or groups',
            'capacity': 6,
            'amenities': ['WiFi', 'AC', 'TV', 'Connecting Door', '2 Bathrooms', 'Sofa Beds', 'Balcony'],
            'status': 'available',
            'roomNumber': '214-215',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Premium Corner King',
            'type': 'premium',
            'price': 8499,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Corner room with king bed and windows on two sides',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Corner View', 'Balcony', 'Mini Bar', 'Work Desk'],
            'status': 'available',
            'roomNumber': '216',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Luxury Honeymoon Villa',
            'type': 'suite',
            'price': 15999,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Private villa-style suite with outdoor Jacuzzi and romantic ambiance',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Private Villa', 'Outdoor Jacuzzi', 'Private Garden', 'Romantic Decor', 'Butler Service'],
            'status': 'available',
            'roomNumber': '602',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Standard Quad Room',
            'type': 'standard',
            'price': 4499,
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Spacious room with four beds for groups',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', '4 Beds', 'Shared Bathroom'],
            'status': 'available',
            'roomNumber': '110',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Premium Suite',
            'type': 'suite',
            'price': 13499,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Premium suite with separate bedroom, living room, and dining area',
            'capacity': 4,
            'amenities': ['WiFi', 'AC', 'TV', 'Separate Bedroom', 'Living Room', 'Dining Area', 'Kitchenette', 'Balcony'],
            'status': 'available',
            'roomNumber': '306',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Executive Accessible Suite',
            'type': 'suite',
            'price': 8999,
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Accessible executive suite with full accessibility features',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Wheelchair Accessible', 'Accessible Bathroom', 'Roll-in Shower', 'Work Desk'],
            'status': 'available',
            'roomNumber': '416',
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Deluxe Pool View Room',
            'type': 'deluxe',
            'price': 6999,
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'description': 'Deluxe room with direct pool view and balcony access',
            'capacity': 2,
            'amenities': ['WiFi', 'AC', 'TV', 'Pool View', 'Balcony', 'Mini Bar', 'Pool Access'],
            'status': 'available',
            'roomNumber': '217',
            'created_at': datetime.utcnow()
        }
    ]
    
    # Clear existing rooms
    db.rooms.delete_many({})
    
    # Insert rooms
    result = db.rooms.insert_many(rooms)
    print(f"Inserted {len(result.inserted_ids)} rooms")

def seed_users():
    """Seed users collection"""
    print("Seeding users...")
    
    users = [
        {
            'email': 'admin@easestay.com',
            'password': generate_password_hash('admin123'),
            'firstName': 'Admin',
            'lastName': 'User',
            'phone': '+91 9876543210',
            'role': 'admin',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'staff@easestay.com',
            'password': generate_password_hash('staff123'),
            'firstName': 'Staff',
            'lastName': 'Member',
            'phone': '+91 9876543211',
            'role': 'staff',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'guest@easestay.com',
            'password': generate_password_hash('guest123'),
            'firstName': 'Guest',
            'lastName': 'User',
            'phone': '+91 9876543212',
            'role': 'guest',
            'created_at': datetime.utcnow()
        }
    ]
    
    # Clear existing users
    db.users.delete_many({})
    
    # Insert users
    result = db.users.insert_many(users)
    print(f"Inserted {len(result.inserted_ids)} users")

def main():
    """Main seed function"""
    try:
        print("=" * 50)
        print("EaseStay Database Seeding")
        print("=" * 50)
        
        seed_rooms()
        seed_users()
        
        print("=" * 50)
        print("Seeding completed successfully!")
        print("=" * 50)
        print("\nTest Credentials:")
        print("Admin: admin@easestay.com / admin123")
        print("Staff: staff@easestay.com / staff123")
        print("Guest: guest@easestay.com / guest123")
        print(f"\nTotal Rooms Created: 45")
        
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
    finally:
        client.close()

if __name__ == '__main__':
    main()
