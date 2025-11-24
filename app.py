from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

# Database configuration
DATABASE = os.path.join(app.root_path, 'db', 'foodshare.db')

# Predefined categories
CATEGORIES = [
    'Prepared Meals',
    'Bakery',
    'Produce',
    'Dairy',
    'Meat & Poultry',
    'Packaged Foods',
    'Other'
]

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initialize the database from schema file"""
    schema_path = os.path.join(app.root_path, 'db', 'foodshare-schema-seed.sql')
    
    if os.path.exists(schema_path):
        conn = get_db_connection()
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    else:
        print(f"Schema file not found at {schema_path}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Routes

@app.route('/')
def index():
    """Homepage with impact statistics"""
    conn = get_db_connection()
    
    # Get impact statistics
    impact_stats = conn.execute('SELECT * FROM impact_tracker WHERE id = 1').fetchone()
    
    conn.close()
    
    return render_template('index.html', impact_stats=impact_stats)

@app.route('/listings')
def browse_listings():
    """Browse all available food listings"""
    conn = get_db_connection()
    
    # Get all listings with user info and reservation status
    listings = conn.execute('''
        SELECT 
            l.*,
            u.name AS owner_name,
            u.role AS owner_role,
            r.expires_at AS reservation_expires_at
        FROM listings l
        LEFT JOIN users u ON l.listed_by = u.id
        LEFT JOIN reservations r ON l.id = r.listing_id 
            AND r.expires_at > datetime('now')
        ORDER BY l.created_at DESC
    ''').fetchall()
    
    conn.close()
    
    # Convert to list of dicts with reservation info
    listings_data = []
    for listing in listings:
        listing_dict = dict(listing)
        if listing_dict['reservation_expires_at']:
            listing_dict['reservation'] = {
                'expires_at': listing_dict['reservation_expires_at']
            }
        else:
            listing_dict['reservation'] = None
        listings_data.append(listing_dict)
    
    return render_template('browse-listings.html', listings=listings_data)
