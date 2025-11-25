-- USERS
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT CHECK(role IN ('individual','charity','restaurant','shop')) NOT NULL,
    location TEXT
);


-- LISTINGS
CREATE TABLE listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    quantity TEXT,
    price REAL DEFAULT 0.0,
    is_free INTEGER DEFAULT 0, -- 0 false, 1 true
    expiry_date TEXT, -- ISO date YYYY-MM-DD
    pickup_window TEXT, -- human readable e.g., "17:00 - 20:00"
    address TEXT,
    category TEXT,
    image_url TEXT,
    listed_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listed_by) REFERENCES users (id)
);


-- RESERVATIONS
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    reserved_by INTEGER NOT NULL,
    reserved_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    FOREIGN KEY (listing_id) REFERENCES listings (id),
    FOREIGN KEY (reserved_by) REFERENCES users (id)
);


-- IMPACT_TRACKER
CREATE TABLE impact_tracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_kg_saved REAL DEFAULT 0,
    total_listings INTEGER DEFAULT 0,
    total_reservations INTEGER DEFAULT 0
);

-- USERS
INSERT INTO users (id, name, email, role, location) VALUES
(1, 'Green Deli', 'contact@greendeli.co.za', 'restaurant', 'Hatfield'),
(2, 'Sunrise Market', 'info@sunrisemarket.co.za', 'shop', 'Brooklyn'),
(3, 'Helping Hands', 'hello@helpinghands.org', 'charity', 'Arcadia'),
(4, 'Theo M.', 'theo@example.com', 'individual', 'Menlyn');


-- LISTINGS
INSERT INTO listings (id, title, description, quantity, price, is_free, expiry_date, pickup_window, address, category, image_url, listed_by)
VALUES
(1, 'Leftover Lasagna Trays', 'Freshly cooked lasagna portions from today''s lunch service.', '4 trays', 25.00, 0, '2025-10-25', '17:00 - 20:00', '123 Church St, Hatfield', 'Prepared Meals', 'images/lasagna.svg', 1),
(2, 'Day-old Bread Loaves', 'Assorted artisan loaves, still great for toasting.', '10 loaves', 0.00, 1, '2025-10-24', '09:00 - 18:00', '45 Market Rd, Brooklyn', 'Bakery', 'images/bread.svg', 2),
(3, 'Surplus Vegetables Box', 'Mixed vegetables from local suppliers.', '10 kg', 50.00, 0, '2025-10-26', '10:00 - 14:00', '7 Union St, Arcadia', 'Produce', 'images/veggies.svg', 2);


-- RESERVATIONS
INSERT INTO reservations (listing_id, reserved_by, reserved_at, expires_at)
VALUES (2, 3, '2025-10-23 09:00:00', '2025-10-23 10:00:00');


-- IMPACT_TRACKER
INSERT INTO impact_tracker (id, total_kg_saved, total_listings, total_reservations)
VALUES (1, 37.5, 3, 8);