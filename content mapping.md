# FoodShare POC - Content Mapping Document

**Purpose:** This document maps static HTML elements to database columns for future backend integration. Use this as a reference when converting the static POC to a dynamic, database-driven application.

---

## 📊 Database Schema Reference

### Tables
1. **users** - User accounts
2. **listings** - Food listings
3. **reservations** - Reserved items
4. **impact_tracker** - Aggregate statistics

---

## 🗺️ Mapping Guide

### Page: `index.html` - Listing Feed

Each listing card displays data from the `listings` and `users` tables, with optional data from `reservations`.

#### Card Structure → Database Mapping

| HTML Element | CSS Class/ID | Database Source | Notes |
|-------------|--------------|-----------------|-------|
| Card image | `.card-img-top` | `listings.image_url` | Display image from path/URL |
| Category badge | `.badge-category` | `listings.category` | Map category to badge color class |
| Price badge | `.badge-price` or `.badge-free` | `listings.price`, `listings.is_free` | If `is_free=1`, show "FREE" badge; else show "R {price}" |
| Title link | `.listing-card-title` (in `<a>`) | `listings.title` | Link to `listing.html?id={listings.id}` |
| Short description | `.listing-card-description` | `listings.description` | Truncate to ~2 lines (CSS or backend) |
| Quantity | `.listing-card-meta` | `listings.quantity` | Display with icon |
| Expiry date | `.listing-card-meta` | `listings.expiry_date` | Format as needed (YYYY-MM-DD) |
| Pickup window | `.listing-card-meta` | `listings.pickup_window` | Display as-is |
| Location | `.listing-card-meta` | `listings.address` | Can truncate to suburb only if preferred |
| Reserved status | `.alert-warning` (conditional) | `reservations.expires_at` | Show only if `JOIN reservations ON listings.id = reservations.listing_id` returns a row |
| Reserve button | `.btn-primary` | N/A | Link to reservation handler; disable if reserved |

#### SQL Query Example

```sql
SELECT 
    l.id,
    l.title,
    l.description,
    l.category,
    l.quantity,
    l.price,
    l.is_free,
    l.expiry_date,
    l.pickup_window,
    l.address,
    l.image_url,
    l.listed_by,
    u.name AS owner_name,
    u.role AS owner_role,
    r.expires_at AS reserved_until
FROM listings l
LEFT JOIN users u ON l.listed_by = u.id
LEFT JOIN reservations r ON l.id = r.listing_id AND r.expires_at > CURRENT_TIMESTAMP
ORDER BY l.created_at DESC;
```

#### Template Pseudocode

```python
{% for listing in listings %}
<article class="col-12 col-md-6 col-lg-4">
    <div class="card listing-card">
        <img src="{{ listing.image_url }}" alt="{{ listing.title }}">
        <div class="card-body">
            <span class="badge badge-category {{ listing.category|lower|slugify }}">
                {{ listing.category }}
            </span>
            
            {% if listing.is_free %}
                <span class="badge badge-free">FREE</span>
            {% else %}
                <span class="badge badge-price">R {{ listing.price }}</span>
            {% endif %}
            
            <h2>
                <a href="listing.html?id={{ listing.id }}">{{ listing.title }}</a>
            </h2>
            
            <p>{{ listing.description|truncate(100) }}</p>
            
            <div>Quantity: {{ listing.quantity }}</div>
            <div>Expires: {{ listing.expiry_date }}</div>
            <div>Pickup: {{ listing.pickup_window }}</div>
            <div>Location: {{ listing.address }}</div>
            
            {% if listing.reserved_until %}
            <div class="alert alert-warning">
                Reserved — until {{ listing.reserved_until }}
            </div>
            {% endif %}
            
            <a href="reserve.html?id={{ listing.id }}" class="btn btn-primary">
                Reserve
            </a>
        </div>
    </div>
</article>
{% endfor %}
```

---

### Page: `listing.html` - Item Detail

Displays full details of a single listing.

#### Element → Database Mapping

| HTML Element | CSS Class/ID | Database Source | Notes |
|-------------|--------------|-----------------|-------|
| Detail image | `.detail-image` | `listings.image_url` | Full-size image |
| Category badge | `.badge-category` | `listings.category` | Same as card view |
| Price/FREE badge | `.badge-price` or `.badge-free` | `listings.price`, `listings.is_free` | Same logic as card view |
| Page title (H1) | `.display-6` | `listings.title` | Main heading |
| Reserved alert | `.alert-warning` (conditional) | `reservations.expires_at` | Show only if reserved |
| Full description | `.detail-value` | `listings.description` | Complete text, no truncation |
| Quantity | `.detail-value` | `listings.quantity` | Display with icon |
| Expiry date | `.detail-value` | `listings.expiry_date` | Format as needed |
| Pickup window | `.detail-value` | `listings.pickup_window` | Display as-is |
| Address | `<address>` | `listings.address` | Full address with line breaks |
| Map placeholder | `.map-placeholder` | `listings.address` | Replace with map API using address |
| Owner name | `<h3>` in owner section | `users.name` (via `listings.listed_by`) | Display name |
| Owner role | `.badge` in owner section | `users.role` | Display role badge |
| Owner location | Text in owner section | `users.location` | Display user's general location |
| Owner icon | Icon class | `users.role` | Map role to icon (shop, restaurant, charity, person) |

#### SQL Query Example

```sql
SELECT 
    l.*,
    u.name AS owner_name,
    u.role AS owner_role,
    u.location AS owner_location,
    r.expires_at AS reserved_until,
    r.reserved_by
FROM listings l
LEFT JOIN users u ON l.listed_by = u.id
LEFT JOIN reservations r ON l.id = r.listing_id AND r.expires_at > CURRENT_TIMESTAMP
WHERE l.id = ?;
```

#### Role → Icon Mapping

```python
role_icons = {
    'restaurant': 'bi-shop',
    'shop': 'bi-cart3',
    'charity': 'bi-heart',
    'individual': 'bi-person-circle'
}
```

---

### Page: `create-listing.html` - Create Listing Form

Form fields map directly to `listings` table columns.

#### Form Field → Database Column Mapping

| Form Field | Input Name | Database Column | Validation | Notes |
|-----------|-----------|-----------------|------------|-------|
| Listing Title | `title` | `listings.title` | Required, max 200 chars | Text input |
| Description | `description` | `listings.description` | Required, max 1000 chars | Textarea |
| Category | `category` | `listings.category` | Required, from predefined list | Select dropdown |
| Quantity | `quantity` | `listings.quantity` | Required | Text input (e.g., "5 kg", "10 loaves") |
| Price | `price` | `listings.price` | Optional, numeric ≥ 0 | Number input |
| Is Free checkbox | `is_free` | `listings.is_free` | Boolean | Checkbox (1 if checked, 0 if not) |
| Expiry Date | `expiry_date` | `listings.expiry_date` | Required, future date | Date input |
| Pickup Window | `pickup_window` | `listings.pickup_window` | Required | Text input (e.g., "09:00 - 18:00") |
| Pickup Address | `address` | `listings.address` | Required | Text input |
| Image Upload | `image` | `listings.image_url` | Optional, image file | File input; store path after upload |
| (Hidden) Listed By | N/A | `listings.listed_by` | Auto-filled | Current user's ID from session |
| (Auto) Created At | N/A | `listings.created_at` | Auto-filled | Server timestamp on INSERT |

#### Category Options (Predefined)

Match these to your dropdown `<option>` values:
- Prepared Meals
- Bakery
- Produce
- Dairy
- Meat & Poultry
- Packaged Foods
- Other

#### Form Submission Handler Pseudocode

```python
def create_listing(request):
    # Get current user from session
    user_id = request.session['user_id']
    
    # Handle image upload
    image_file = request.FILES.get('image')
    if image_file:
        image_url = save_uploaded_file(image_file, 'uploads/listings/')
    else:
        image_url = 'assets/images/default-placeholder.svg'
    
    # Convert is_free checkbox to integer
    is_free = 1 if request.POST.get('is_free') else 0
    
    # Insert into database
    cursor.execute("""
        INSERT INTO listings (
            title, description, category, quantity, price, is_free,
            expiry_date, pickup_window, address, image_url, listed_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request.POST['title'],
        request.POST['description'],
        request.POST['category'],
        request.POST['quantity'],
        float(request.POST.get('price', 0)),
        is_free,
        request.POST['expiry_date'],
        request.POST['pickup_window'],
        request.POST['address'],
        image_url,
        user_id
    ))
    
    db.commit()
    return redirect('index.html')
```

---

### Page: `impact.html` - Impact Tracker

Displays aggregate statistics from `impact_tracker` table and calculated breakdowns.

#### Statistic → Database Mapping

| Display Element | CSS Class | Database Source | Notes |
|----------------|-----------|-----------------|-------|
| Total Food Saved | `.impact-stat-value` | `impact_tracker.total_kg_saved` | Display with "kg" unit |
| Active Listings | `.impact-stat-value` | `impact_tracker.total_listings` OR `COUNT(*)` from `listings` | Real-time count preferred |
| Total Reservations | `.impact-stat-value` | `impact_tracker.total_reservations` OR `COUNT(*)` from `reservations` | Historical count |
| Category breakdown | `.breakdown-item` | Aggregate query on `listings.category` | Group by category, count |
| Role breakdown | `.breakdown-item` | Aggregate query on `users.role` | Group by role, count |
| CO₂ emissions | Calculated | `total_kg_saved * 3` | Rough estimate |
| Water saved | Calculated | `total_kg_saved * 50` | Rough estimate (liters) |
| Meals provided | Calculated | `total_kg_saved / 2` | Rough estimate (2kg per meal) |

#### SQL Queries

**Impact Tracker Stats:**
```sql
SELECT 
    total_kg_saved,
    total_listings,
    total_reservations
FROM impact_tracker
WHERE id = 1;
```

**Category Breakdown:**
```sql
SELECT 
    category,
    COUNT(*) AS count
FROM listings
GROUP BY category
ORDER BY count DESC;
```

**Role Breakdown:**
```sql
SELECT 
    u.role,
    COUNT(DISTINCT u.id) AS count
FROM users u
INNER JOIN listings l ON u.id = l.listed_by
GROUP BY u.role
ORDER BY count DESC;
```

**Real-time Active Listings Count:**
```sql
SELECT COUNT(*) AS active_listings
FROM listings
WHERE expiry_date >= DATE('now');
```

#### Environmental Calculations

```python
total_kg_saved = impact_data['total_kg_saved']

environmental_impact = {
    'co2_kg': round(total_kg_saved * 3, 1),      # ~3 kg CO₂ per kg food
    'water_liters': round(total_kg_saved * 50, 0),  # ~50L water per kg food
    'meals': round(total_kg_saved / 2, 0)        # ~2 kg per meal
}
```

---

## 🔄 Reservation Logic

### Creating a Reservation

When a user clicks "Reserve" on a listing:

1. Check if listing is already reserved:
   ```sql
   SELECT * FROM reservations 
   WHERE listing_id = ? 
   AND expires_at > CURRENT_TIMESTAMP;
   ```

2. If not reserved, create reservation:
   ```sql
   INSERT INTO reservations (listing_id, reserved_by, expires_at)
   VALUES (?, ?, datetime('now', '+1 hour'));
   ```

3. Update listing status or filter in queries using `LEFT JOIN`.

### Expiring Reservations

Run a scheduled job (cron, celery, etc.) to clean up expired reservations:

```sql
DELETE FROM reservations 
WHERE expires_at <= CURRENT_TIMESTAMP;
```

Or keep them for historical tracking:

```sql
UPDATE reservations 
SET status = 'expired'
WHERE expires_at <= CURRENT_TIMESTAMP 
AND status = 'active';
```

---

## 🎨 Dynamic Badge Styling

### Category Badge Color Mapping

Map `listings.category` to CSS classes:

```python
category_classes = {
    'Prepared Meals': 'prepared-meals',
    'Bakery': 'bakery',
    'Produce': 'produce',
    'Dairy': 'dairy',
    'Meat & Poultry': 'meat-poultry',
    'Packaged Foods': 'packaged-foods',
    'Other': 'other'
}
```

Apply in template:
```html
<span class="badge badge-category {{ category_classes[listing.category] }}">
    {{ listing.category }}
</span>
```

### Role Badge/Icon Mapping

Map `users.role` to icons and colors:

```python
role_config = {
    'restaurant': {
        'icon': 'bi-shop',
        'color': 'warning',
        'label': 'Restaurant'
    },
    'shop': {
        'icon': 'bi-cart3',
        'color': 'info',
        'label': 'Shop'
    },
    'charity': {
        'icon': 'bi-heart',
        'color': 'danger',
        'label': 'Charity'
    },
    'individual': {
        'icon': 'bi-person-circle',
        'color': 'success',
        'label': 'Individual'
    }
}
```

---

## 🔐 Authentication & User Context

### User Session Data

When implementing user authentication, store in session:

```python
session['user_id'] = user.id
session['user_name'] = user.name
session['user_role'] = user.role
```

### Conditional UI Elements

**Show "Create Listing" only if logged in:**
```html
{% if user.is_authenticated %}
    <li class="nav-item">
        <a class="nav-link" href="create-listing.html">Create Listing</a>
    </li>
{% endif %}
```

**Show "Edit" button only if listing owner:**
```html
{% if listing.listed_by == current_user.id %}
    <a href="edit-listing.html?id={{ listing.id }}" class="btn btn-secondary">
        Edit Listing
    </a>
{% endif %}
```

---

## 📱 API Endpoints (Future)

### Suggested RESTful API structure

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | `/api/listings` | Get all listings | N/A | JSON array of listings |
| GET | `/api/listings/:id` | Get single listing | N/A | JSON object |
| POST | `/api/listings` | Create listing | Listing data | Created listing JSON |
| PUT | `/api/listings/:id` | Update listing | Updated fields | Updated listing JSON |
| DELETE | `/api/listings/:id` | Delete listing | N/A | Success message |
| POST | `/api/reservations` | Reserve listing | `listing_id` | Reservation JSON |
| GET | `/api/impact` | Get impact stats | N/A | Impact data JSON |

---

## 🗺️ Map Integration

Replace the static map placeholder with a real map:

### Google Maps Example

```html
<div id="map" style="width: 100%; height: 300px;"></div>

<script>
function initMap() {
    const location = { lat: -25.7479, lng: 28.2293 }; // Parse from listing.address
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: location,
    });
    new google.maps.Marker({
        position: location,
        map: map,
        title: "{{ listing.title }}"
    });
}
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
```

### Mapbox Example

```html
<div id="map" style="width: 100%; height: 300px;"></div>

<script src='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js'></script>
<script>
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [28.2293, -25.7479], // Parse from listing.address
    zoom: 15
});

new mapboxgl.Marker()
    .setLngLat([28.2293, -25.7479])
    .addTo(map);
</script>
```

---

## 🔍 Search & Filter (Future)

### Filter by Category

```sql
SELECT * FROM listings
WHERE category = ?
AND expiry_date >= DATE('now')
ORDER BY created_at DESC;
```

### Search by Title/Description

```sql
SELECT * FROM listings
WHERE (title LIKE '%' || ? || '%' OR description LIKE '%' || ? || '%')
AND expiry_date >= DATE('now')
ORDER BY created_at DESC;
```

### Filter by Price

```sql
-- Free items only
SELECT * FROM listings
WHERE is_free = 1
AND expiry_date >= DATE('now');

-- Priced items only
SELECT * FROM listings
WHERE is_free = 0
AND expiry_date >= DATE('now');
```

### Filter by Location (Suburb)

```sql
SELECT * FROM listings
WHERE address LIKE '%' || ? || '%'
AND expiry_date >= DATE('now');
```

---

## 📊 Data Validation Rules

### Server-Side Validation Checklist

- **Title:** Required, 3-200 characters
- **Description:** Required, 10-1000 characters
- **Category:** Required, must be in predefined list
- **Quantity:** Required, 1-100 characters
- **Price:** Optional, numeric ≥ 0, max 2 decimal places
- **Is Free:** Boolean (0 or 1)
- **Expiry Date:** Required, must be future date (≥ today)
- **Pickup Window:** Required, 5-100 characters
- **Address:** Required, 10-200 characters
- **Image URL:** Optional, valid image path/URL
- **Listed By:** Required, must be valid user ID from session

---

## 🧪 Test Data Scenarios

Use these scenarios to test backend integration:

1. **Free listing with reservation:** Bread listing (ID 2)
2. **Priced listing, no reservation:** Lasagna (ID 1), Veggies (ID 3)
3. **Expired listing:** Create listing with `expiry_date` in past
4. **Multiple listings by same user:** Sunrise Market has 2 listings
5. **All four user roles:** Test each role (restaurant, shop, charity, individual)
6. **Impact updates:** Insert reservation, check if stats update

---

## 📚 Additional Resources

- **Bootstrap 5.3 Docs:** https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons:** https://icons.getbootstrap.com/
- **SQLite Documentation:** https://www.sqlite.org/docs.html
- **HTML5 Form Validation:** https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation

---

**This mapping document should serve as a complete reference for backend developers to wire up the static POC to a live database.**
