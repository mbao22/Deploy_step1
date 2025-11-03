from flask import Flask, render_template
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE = 'data.db'

# Sample data for demonstration
SAMPLE_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
SAMPLE_COMMENTS = [
    "Great product, highly recommended!",
    "Average experience, could be better.",
    "Excellent service and fast delivery.",
    "Not satisfied with the quality.",
    "Amazing value for money!",
    "Poor customer support.",
    "Fast shipping and good packaging.",
    "Product arrived damaged.",
    "Exceeded my expectations!",
    "Would not buy again."
]
SENTIMENTS = ["positive", "negative", "neutral"]

def get_db_connection():
    """
    Establishes connection to SQLite database
    SQLite creates the database file automatically if it doesn't exist
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_db():
    """
    Creates the reviews table if it doesn't exist
    and seeds it with sample data
    """
    conn = get_db_connection()
    
    # Create reviews table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            comment TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if table is empty and seed with sample data
    count = conn.execute('SELECT COUNT(*) FROM reviews').fetchone()[0]
    
    if count == 0:
        # Generate 30 sample reviews
        reviews = []
        for i in range(30):
            review = (
                random.choice(SAMPLE_NAMES),
                random.choice(SAMPLE_COMMENTS),
                random.choice(SENTIMENTS)
            )
            reviews.append(review)
        
        # Insert sample data
        conn.executemany('''
            INSERT INTO reviews (username, comment, sentiment)
            VALUES (?, ?, ?)
        ''', reviews)
        
        conn.commit()
        print(f"Seeded database with {len(reviews)} sample reviews")
    
    conn.close()

@app.route('/')
def index():
    """
    Main route that displays all reviews in an HTML table
    """
    conn = get_db_connection()
    
    # Fetch all reviews ordered by creation date (newest first)
    reviews = conn.execute('''
        SELECT * FROM reviews 
        ORDER BY created_at DESC
    ''').fetchall()
    
    conn.close()
    
    # Render template with reviews data
    return render_template('index.html', reviews=reviews)

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Start Flask development server
    print("Starting Flask application...")
    print("Database initialized with sample data")
    print("Access the application at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5001)