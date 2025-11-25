# FoodShare Pretoria - Flask Application Setup

## Overview

This Flask application has been successfully converted from a static POC to a fully functional server-side rendered application with SQLite database integration.

## Project Structure

```
BFB/
├── app.py                         # Main Flask application
├── templates/                     # Jinja2 templates
│   ├── base.html                 # Base template with nav/footer
│   ├── index.html                # Homepage
│   ├── browse-listings.html      # Listings feed
│   ├── listing.html              # Listing detail
│   ├── create-listing.html       # Create listing form
│   └── impact.html               # Impact tracker
├── static/                        # Static assets
│   ├── css/
│   │   └── styles.css            # Custom styles
│   ├── images/                   # SVG placeholders
│   │   ├── bread.svg
│   │   ├── hero-banner.svg
│   │   ├── lasagna.svg
│   │   └── veggies.svg
│   └── uploads/                  # User-uploaded images
├── db/
│   ├── foodshare-schema-seed.sql # Database schema with seed data
│   └── foodshare.db              # SQLite database (auto-created)
├── README.md                      # Original POC documentation
├── README_FLASK.md               # This file
└── content-mapping.md            # Database mapping guide
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

The database will be automatically initialized when you first run the application. Alternatively, you can manually initialize it:

```bash
cd /Users/theowork/Projects/Personal/BFB
flask --app app init-db
```

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Available Routes

### GET Routes (Pages)

| Route | Description | Template |
|-------|-------------|----------|
| `/` | Homepage with stats | `index.html` |
| `/listings` | Browse all food listings | `browse-listings.html` |
| `/listing/<id>` | View single listing detail | `listing.html` |
| `/create` | Create listing form | `create-listing.html` |
| `/impact` | Impact tracker dashboard | `impact.html` |

### POST Routes (Actions)

| Route | Description | Action |
|-------|-------------|--------|
| `/listing/create` | Create new listing | Inserts listing, handles file upload |
| `/listing/<id>/reserve` | Reserve a listing | Creates reservation (1-hour expiry) |

## Features Implemented

### ✅ Database Integration
- SQLite database with 4 tables: `users`, `listings`, `reservations`, `impact_tracker`
- Automatic database initialization from schema file
- Connection pooling with `sqlite3.Row` for dict-like access

### ✅ Server-Side Rendering
- Jinja2 templates with template inheritance
- Dynamic data rendering from database
- Flash messages for user feedback
- Active navigation state tracking

### ✅ Listing Management
- Browse all listings with reservation status
- View detailed listing information
- Create new listings with form validation
- Image upload support (max 5MB)
- Default placeholder images

### ✅ Reservation System
- Reserve listings with 1-hour expiration
- Check for existing reservations
- Display reservation status on listings
- Prevent double-booking

### ✅ Impact Tracking
- Real-time statistics from database
- Category and role breakdowns
- Environmental impact calculations:
  - CO₂ saved (kg × 3)
  - Water saved (kg × 50 liters)
  - Meals provided (kg ÷ 2)


## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('individual', 'charity', 'restaurant', 'shop')),
    location TEXT
);
```

### Listings Table
```sql
CREATE TABLE listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    quantity TEXT,
    price REAL DEFAULT 0.0,
    is_free INTEGER DEFAULT 0,
    expiry_date TEXT,
    pickup_window TEXT,
    address TEXT,
    category TEXT,
    image_url TEXT,
    listed_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listed_by) REFERENCES users(id)
);
```

### Reservations Table
```sql
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    reserved_by INTEGER NOT NULL,
    reserved_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    FOREIGN KEY (listing_id) REFERENCES listings(id),
    FOREIGN KEY (reserved_by) REFERENCES users(id)
);
```

### Impact Tracker Table
```sql
CREATE TABLE impact_tracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_kg_saved REAL DEFAULT 0,
    total_listings INTEGER DEFAULT 0,
    total_reservations INTEGER DEFAULT 0
);
```

## Seed Data

The database comes pre-populated with:
- **4 users**: Green Deli (restaurant), Sunrise Market (shop), Helping Hands (charity), Theo M. (individual)
- **3 listings**: Lasagna, Bread (reserved), Vegetables
- **1 reservation**: Bread reserved by Helping Hands
- **Impact stats**: 37.5 kg saved, 3 listings, 8 total reservations

## Template Variables

### `index.html`
- `impact_stats`: Impact tracker statistics

### `browse-listings.html`
- `listings`: List of all listings with owner and reservation info

### `listing.html`
- `listing`: Single listing details
- `owner`: Owner/donor information
- `reservation`: Current reservation (if any)

### `create-listing.html`
- `categories`: List of predefined food categories

### `impact.html`
- `impact_stats`: Main statistics
- `category_breakdown`: Listings grouped by category
- `role_breakdown`: Contributors grouped by role
- `environmental_impact`: Calculated environmental metrics

## Current Limitations

### 🔒 No Authentication
- All listings created as user ID 1 (Green Deli)
- All reservations created as user ID 3 (Helping Hands)
- No login/logout functionality

**Future Enhancement**: Implement Flask-Login for user sessions

### 📝 No Form Validation
- Server-side validation is basic (try/catch)
- Client-side uses HTML5 validation only

**Future Enhancement**: Use Flask-WTF for comprehensive validation

### 🔍 No Search/Filter
- All listings displayed without filtering
- No search by location, category, or price

**Future Enhancement**: Add query parameters and search form

### 🗺️ No Map Integration
- Static map placeholder only

**Future Enhancement**: Integrate Google Maps or Mapbox API

## Testing the Application

### 1. View Homepage
Navigate to `http://127.0.0.1:5000/`
- Should display impact statistics (37.5 kg, 3 listings, 8 reservations)

### 2. Browse Listings
Navigate to `http://127.0.0.1:5000/listings`
- Should show 3 listings
- Bread listing should show "Reserved" badge

### 3. View Listing Detail
Click on any listing or go to `http://127.0.0.1:5000/listing/2`
- Should show full details
- Bread (ID 2) should show reservation warning

### 4. Create New Listing
Navigate to `http://127.0.0.1:5000/create`
- Fill out the form
- Upload an image (optional)
- Submit and verify success message

### 5. Reserve a Listing
Go to listing detail page for unreserved item
- Click "Reserve This Item"
- Should create reservation and show success message
- Listing should now show as reserved

### 6. View Impact Tracker
Navigate to `http://127.0.0.1:5000/impact`
- Should display statistics and breakdowns
- Environmental calculations should update with new data

## Troubleshooting

### Database Errors
If you encounter database errors, reinitialize:
```bash
rm db/foodshare.db
python app.py
```

### Upload Errors
Ensure the uploads folder exists:
```bash
mkdir -p static/uploads
```

### Template Not Found
Verify templates are in `templates/` directory

### Static Files Not Loading
Check that static files are in `static/` directory

## Next Steps

To make this a production-ready application:

1. **User Authentication**
   - Add Flask-Login
   - Implement registration/login
   - Role-based permissions

2. **Enhanced Validation**
   - Flask-WTF for forms
   - Server-side validation rules
   - CSRF protection

3. **Search & Filters**
   - Location-based search
   - Category filtering
   - Price range filtering
   - Date range filtering

4. **Map Integration**
   - Google Maps API
   - Geocoding addresses
   - Distance calculations

5. **Notifications**
   - Email notifications for reservations
   - SMS reminders for pickup
   - Expiry warnings

6. **Admin Dashboard**
   - User management
   - Listing moderation
   - Analytics and reports

7. **Deployment**
   - Production WSGI server (Gunicorn)
   - Environment variables for secrets
   - PostgreSQL for production database
   - Cloud hosting (AWS, Azure, Heroku)
   - Domain and SSL certificate

## License

Educational and demonstration purposes.

---

**FoodShare Pretoria** - Fighting Food Waste, One Meal at a Time 🌱
