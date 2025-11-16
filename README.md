# EaseStay - Hotel Booking & Management System

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MongoDB (running on localhost:27017)
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure MongoDB is running:
```bash
# Windows (if MongoDB is installed as service, it should be running automatically)
# Or start MongoDB manually:
mongod --dbpath "C:\path\to\your\data\db"
```

4. Seed the database with sample data:
```bash
python seed_data.py
```

5. Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

The frontend files (index.html, style.css, script.js) are in the root directory.

1. Open `index.html` in a web browser or use a local server:

**Option 1: Using Python HTTP Server**
```bash
# From the project root directory
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

**Option 2: Using Live Server (VS Code Extension)**
- Install the "Live Server" extension in VS Code
- Right-click on `index.html` and select "Open with Live Server"

**Option 3: Direct File Opening**
- Simply double-click `index.html` to open in your default browser
- Note: Some features may not work due to CORS restrictions

### API Endpoints

#### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

#### Rooms
- `GET /api/rooms` - Get all rooms
- `GET /api/rooms/available` - Get available rooms (optional query params: checkin, checkout)
- `PUT /api/room/<id>/status` - Update room status (admin only)

#### Bookings
- `POST /api/book` - Create new booking (requires auth)
- `GET /api/bookings` - Get user bookings (requires auth)
- `GET /api/bookings/all` - Get all bookings (admin only)

#### Payments
- `POST /api/payment` - Process payment (requires auth)

#### Feedback
- `POST /api/feedback` - Submit feedback (requires auth)
- `GET /api/feedback` - Get feedback list

### Test Credentials

After running the seed script, you can use these credentials:

**Admin:**
- Email: `admin@easestay.com`
- Password: `admin123`

**Staff:**
- Email: `staff@easestay.com`
- Password: `staff123`

**Guest:**
- Email: `guest@easestay.com`
- Password: `guest123`

### Project Structure

```
EaseStay/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── seed_data.py          # Database seeding script
│   ├── models/
│   │   ├── user_model.py     # User model
│   │   ├── room_model.py     # Room model
│   │   └── booking_model.py  # Booking model
│   └── routes/
│       ├── auth.py           # Authentication routes
│       ├── rooms.py          # Room routes
│       ├── bookings.py      # Booking routes
│       └── feedback.py       # Feedback routes
├── index.html                # Frontend HTML
├── style.css                 # Frontend styles
└── script.js                 # Frontend JavaScript
```

### Troubleshooting

1. **MongoDB Connection Error:**
   - Make sure MongoDB is running: `mongod`
   - Check MongoDB URI in `backend/config.py`

2. **CORS Errors:**
   - Make sure the frontend is being served from an allowed origin
   - Check CORS settings in `backend/config.py`

3. **Import Errors:**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're running from the correct directory

4. **Port Already in Use:**
   - Change the port in `backend/app.py` (line with `app.run()`)

### Development Notes

- JWT tokens expire after 24 hours
- Room statuses: `available`, `occupied`, `maintenance`
- Booking statuses: `pending`, `confirmed`, `cancelled`
- All API responses are in JSON format
- Error responses include an `error` field with the error message

