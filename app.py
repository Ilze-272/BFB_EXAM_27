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