"""Creates shop.db, a small example shop database (made-up customers and orders)."""
import sqlite3

db = sqlite3.connect("shop.db")
db.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    item TEXT NOT NULL,
    total_eur REAL NOT NULL,
    ordered_on TEXT NOT NULL
);
INSERT INTO customers VALUES
    (1, 'Ana Costa', 'Lisbon'), (2, 'Ben Okafor', 'Lagos'), (3, 'Chen Wei', 'Taipei'),
    (4, 'Dora Novak', 'Prague'), (5, 'Emil Hansen', 'Oslo');
INSERT INTO orders VALUES
    (1, 1, 'Desk lamp', 39.0, '2026-08-14'), (2, 1, 'Monitor arm', 89.0, '2026-10-30'),
    (3, 2, 'Keyboard', 120.0, '2026-09-02'), (4, 3, 'USB hub', 25.0, '2026-10-12'),
    (5, 3, 'Webcam', 65.0, '2026-11-03'), (6, 4, 'Desk mat', 19.0, '2026-07-21'),
    (7, 5, 'Headset', 75.0, '2026-11-05'), (8, 2, 'Mouse', 45.0, '2026-08-19');
""")
db.commit()
print("shop.db created: 5 customers, 8 orders")
