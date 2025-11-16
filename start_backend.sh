#!/bin/bash

echo "============================================"
echo "EaseStay - Quick Start Script"
echo "============================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "Python found!"
echo ""

echo "Checking MongoDB connection..."
python3 -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017').server_info()" &> /dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: MongoDB might not be running on localhost:27017"
    echo "Please make sure MongoDB is running before starting the server"
    echo ""
fi

echo "Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Dependencies installed!"
echo ""

read -p "Do you want to seed the database? (Y/N): " seed_choice
if [[ $seed_choice == "Y" || $seed_choice == "y" ]]; then
    echo "Seeding database..."
    python3 seed_data.py
    echo ""
fi

echo "Starting Flask server..."
echo "Server will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py

