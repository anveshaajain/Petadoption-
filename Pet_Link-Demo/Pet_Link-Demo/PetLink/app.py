from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'petlink_secret_key_2024'

# Database initialization
def init_db():
    try:
        conn = sqlite3.connect('petlink.db')
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                contact TEXT NOT NULL,
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Owners table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                contact TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Create Pets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                breed TEXT NOT NULL,
                age INTEGER NOT NULL,
                health_details TEXT,
                medical_details TEXT,
                adoption_status TEXT DEFAULT 'available',
                image_url TEXT,
                owner_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id),
                FOREIGN KEY (owner_id) REFERENCES owners (id)
            )
        ''')
        
        # Create Adoption Requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adoption_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                pet_id INTEGER,
                status TEXT DEFAULT 'pending',
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (pet_id) REFERENCES pets (id)
            )
        ''')
        
        # Create Care Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS care_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Create Care Post Comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS care_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(post_id) REFERENCES care_posts(id) ON DELETE CASCADE,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Create Pet Likes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pet_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pet_id, user_id),
                FOREIGN KEY(pet_id) REFERENCES pets(id) ON DELETE CASCADE,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Insert default categories
        categories = ['Dogs', 'Cats', 'Birds', 'Others']
        for category in categories:
            cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))
        
        # Insert default owner
        default_owner_password = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO owners (name, email, password, contact) 
            VALUES (?, ?, ?, ?)
        ''', ('Admin Owner', 'admin@petlink.com', default_owner_password, '+1234567890'))
        
        # Insert sample pets
        sample_pets = [
            ('Buddy', 1, 'Golden Retriever', 3, 'Healthy and energetic', 'Vaccinated, neutered', 'available', 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400', 1),
            ('Luna', 2, 'Persian', 2, 'Calm and friendly', 'Vaccinated, spayed', 'available', 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400', 1),
            ('Max', 1, 'German Shepherd', 4, 'Well-trained guard dog', 'All vaccinations up to date', 'available', 'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?w=400', 1),
            ('Whiskers', 2, 'Maine Coon', 1, 'Playful kitten', 'First vaccinations done', 'available', 'https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400', 1),
            ('Charlie', 3, 'Cockatiel', 2, 'Loves to sing', 'Healthy, no medical issues', 'available', 'https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400', 1),
            ('Bella', 1, 'Labrador', 5, 'Great with kids', 'Vaccinated, microchipped', 'available', 'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=400', 1),
            ('Mittens', 2, 'Siamese', 3, 'Independent but loving', 'Vaccinated, spayed', 'available', 'https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400', 1),
            ('Rocky', 1, 'Bulldog', 6, 'Gentle giant', 'Regular health checkups', 'available', 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400', 1),
            ('Tweety', 3, 'Canary', 1, 'Beautiful singer', 'Healthy and active', 'available', 'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400', 1),
            ('Shadow', 4, 'Rabbit', 2, 'Quiet and gentle', 'Vaccinated, litter trained', 'available', 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400', 1)
        ]
        
        for pet in sample_pets:
            cursor.execute('''
                INSERT OR IGNORE INTO pets (name, category_id, breed, age, health_details, medical_details, adoption_status, image_url, owner_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', pet)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Database initialization error: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect('petlink.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def home():
    try:
        conn = get_db_connection()
        pets = conn.execute('''
            SELECT p.*, c.name as category_name 
            FROM pets p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.adoption_status = "available" 
            LIMIT 6
        ''').fetchall()
        conn.close()
        return render_template('index.html', pets=pets)
    except Exception as e:
        print(f"Home route error: {e}")
        return f"Error: {e}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = hash_password(request.form['password'])
            contact = request.form['contact']
            address = request.form['address']
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO users (name, email, password, contact, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, password, contact, address))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
        except Exception as e:
            flash(f'Registration error: {e}', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = hash_password(request.form['password'])
            
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE email = ? AND password = ?',
                (email, password)
            ).fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_type'] = 'user'
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Login error: {e}', 'error')
    
    return render_template('login.html')

@app.route('/owner-login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = hash_password(request.form['password'])
            
            conn = get_db_connection()
            owner = conn.execute(
                'SELECT * FROM owners WHERE email = ? AND password = ?',
                (email, password)
            ).fetchone()
            conn.close()
            
            if owner:
                session['user_id'] = owner['id']
                session['user_name'] = owner['name']
                session['user_type'] = 'owner'
                flash('Owner login successful!', 'success')
                return redirect(url_for('owner_dashboard'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Owner login error: {e}', 'error')
    
    return render_template('owner_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session or session.get('user_type') != 'user':
        flash('Please login to access your profile.', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        
        if request.method == 'POST':
            # Update profile
            name = request.form.get('name', '').strip()
            contact = request.form.get('contact', '').strip()
            address = request.form.get('address', '').strip()
            password = request.form.get('password', '').strip()
            
            if not name or not contact or not address:
                flash('All fields are required!', 'error')
                conn.close()
                return redirect(url_for('profile'))
            
            # Update user info
            if password:
                # Update with new password
                hashed_password = hash_password(password)
                conn.execute('''
                    UPDATE users SET name = ?, contact = ?, address = ?, password = ?
                    WHERE id = ?
                ''', (name, contact, address, hashed_password, session['user_id']))
            else:
                # Update without changing password
                conn.execute('''
                    UPDATE users SET name = ?, contact = ?, address = ?
                    WHERE id = ?
                ''', (name, contact, address, session['user_id']))
            
            conn.commit()
            session['user_name'] = name
            flash('Profile updated successfully!', 'success')
        
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        
        # Get user's adoption requests
        requests = conn.execute('''
            SELECT ar.*, p.name as pet_name, p.breed, c.name as category_name
            FROM adoption_requests ar
            JOIN pets p ON ar.pet_id = p.id
            JOIN categories c ON p.category_id = c.id
            WHERE ar.user_id = ?
            ORDER BY ar.created_at DESC
        ''', (session['user_id'],)).fetchall()
        
        conn.close()
        return render_template('profile.html', user=user, requests=requests)
    except Exception as e:
        flash(f'Profile error: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/adopt')
def adopt():
    try:
        category_filter = request.args.get('category', '')
        user_id = session.get('user_id') if session.get('user_type') == 'user' else None
        
        conn = get_db_connection()
        
        # Get all categories
        categories = conn.execute('SELECT * FROM categories').fetchall()
        
        # Build query based on filter with like counts
        if category_filter:
            if user_id:
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count,
                           MAX(CASE WHEN pl.user_id = ? THEN 1 ELSE 0 END) as is_liked
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE p.adoption_status = "available" AND c.name = ?
                    GROUP BY p.id, p.name, p.category_id, p.breed, p.age, p.health_details, 
                             p.medical_details, p.adoption_status, p.image_url, p.owner_id, 
                             p.created_at, c.name
                    ORDER BY p.created_at DESC
                ''', (user_id, category_filter)).fetchall()
            else:
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count,
                           0 as is_liked
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE p.adoption_status = "available" AND c.name = ?
                    GROUP BY p.id, p.name, p.category_id, p.breed, p.age, p.health_details, 
                             p.medical_details, p.adoption_status, p.image_url, p.owner_id, 
                             p.created_at, c.name
                    ORDER BY p.created_at DESC
                ''', (category_filter,)).fetchall()
        else:
            if user_id:
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count,
                           MAX(CASE WHEN pl.user_id = ? THEN 1 ELSE 0 END) as is_liked
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE p.adoption_status = "available"
                    GROUP BY p.id, p.name, p.category_id, p.breed, p.age, p.health_details, 
                             p.medical_details, p.adoption_status, p.image_url, p.owner_id, 
                             p.created_at, c.name
                    ORDER BY p.created_at DESC
                ''', (user_id,)).fetchall()
            else:
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count,
                           0 as is_liked
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE p.adoption_status = "available"
                    GROUP BY p.id, p.name, p.category_id, p.breed, p.age, p.health_details, 
                             p.medical_details, p.adoption_status, p.image_url, p.owner_id, 
                             p.created_at, c.name
                    ORDER BY p.created_at DESC
                ''').fetchall()
        
        conn.close()
        return render_template('adopt.html', pets=pets, categories=categories, selected_category=category_filter)
    except Exception as e:
        return f"Adopt page error: {e}"

@app.route('/request-adoption/<int:pet_id>', methods=['POST'])
def request_adoption(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Please login to request adoption.'})
    
    try:
        data = request.get_json()
        message = data.get('message', '') if data else ''
        
        # Use default message if none provided
        if not message:
            message = f"I am interested in adopting this pet. Please contact me to discuss further details."
        
        conn = get_db_connection()
        
        # Check if user already requested this pet
        existing = conn.execute(
            'SELECT * FROM adoption_requests WHERE user_id = ? AND pet_id = ?',
            (session['user_id'], pet_id)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'success': False, 'message': 'You have already requested this pet.'})
        
        # Create adoption request
        conn.execute('''
            INSERT INTO adoption_requests (user_id, pet_id, message)
            VALUES (?, ?, ?)
        ''', (session['user_id'], pet_id, message))
        
        conn.commit()
        conn.close()
        
        flash('Adoption request sent', 'success')
        return jsonify({'success': True, 'message': 'Request sent successfully to owner!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/owner-dashboard')
def owner_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'owner':
        flash('Please login as owner to access dashboard.', 'error')
        return redirect(url_for('owner_login'))
    
    try:
        conn = get_db_connection()
        
        # Get owner's pets
        pets = conn.execute('''
            SELECT p.*, c.name as category_name 
            FROM pets p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.owner_id = ?
            ORDER BY p.created_at DESC
        ''', (session['user_id'],)).fetchall()
        
        # Get adoption requests
        requests = conn.execute('''
            SELECT ar.*, p.name as pet_name, p.breed, u.name as user_name, u.email, u.contact
            FROM adoption_requests ar
            JOIN pets p ON ar.pet_id = p.id
            JOIN users u ON ar.user_id = u.id
            WHERE p.owner_id = ?
            ORDER BY ar.created_at DESC
        ''', (session['user_id'],)).fetchall()
        
        # Analytics: Get top pets by request count
        top_pets = conn.execute('''
            SELECT p.id, p.name, p.breed, p.image_url, c.name as category_name,
                   COUNT(ar.id) as request_count,
                   SUM(CASE WHEN ar.status = 'approved' THEN 1 ELSE 0 END) as approved_count
            FROM pets p
            LEFT JOIN adoption_requests ar ON p.id = ar.pet_id
            JOIN categories c ON p.category_id = c.id
            WHERE p.owner_id = ?
            GROUP BY p.id, p.name, p.breed, p.image_url, c.name
            ORDER BY request_count DESC, p.name ASC
            LIMIT 5
        ''', (session['user_id'],)).fetchall()
        
        # Analytics: Get detailed statistics
        stats_row = conn.execute('''
            SELECT 
                COUNT(DISTINCT p.id) as total_pets,
                SUM(CASE WHEN p.adoption_status = 'available' THEN 1 ELSE 0 END) as available_pets,
                SUM(CASE WHEN p.adoption_status = 'adopted' THEN 1 ELSE 0 END) as adopted_pets,
                COUNT(DISTINCT ar.id) as total_requests,
                SUM(CASE WHEN ar.status = 'pending' THEN 1 ELSE 0 END) as pending_requests,
                SUM(CASE WHEN ar.status = 'approved' THEN 1 ELSE 0 END) as approved_requests,
                SUM(CASE WHEN ar.status = 'rejected' THEN 1 ELSE 0 END) as rejected_requests
            FROM pets p
            LEFT JOIN adoption_requests ar ON p.id = ar.pet_id
            WHERE p.owner_id = ?
        ''', (session['user_id'],)).fetchone()
        
        # Convert Row to dict and ensure all values are integers (not None)
        if stats_row:
            stats = {
                'total_pets': stats_row['total_pets'] or 0,
                'available_pets': stats_row['available_pets'] or 0,
                'adopted_pets': stats_row['adopted_pets'] or 0,
                'total_requests': stats_row['total_requests'] or 0,
                'pending_requests': stats_row['pending_requests'] or 0,
                'approved_requests': stats_row['approved_requests'] or 0,
                'rejected_requests': stats_row['rejected_requests'] or 0
            }
        else:
            stats = {
                'total_pets': 0,
                'available_pets': 0,
                'adopted_pets': 0,
                'total_requests': 0,
                'pending_requests': 0,
                'approved_requests': 0,
                'rejected_requests': 0
            }
        
        # Analytics: Get recent activity (last 10 activities)
        recent_activity = []
        
        # Recent adoption requests
        recent_requests = conn.execute('''
            SELECT 'request' as type, ar.created_at, 
                   p.name as pet_name, u.name as user_name, ar.status,
                   'Adoption request ' || ar.status || ' for ' || p.name as description
            FROM adoption_requests ar
            JOIN pets p ON ar.pet_id = p.id
            JOIN users u ON ar.user_id = u.id
            WHERE p.owner_id = ?
            ORDER BY ar.created_at DESC
            LIMIT 5
        ''', (session['user_id'],)).fetchall()
        
        # Recent pet additions
        recent_pets = conn.execute('''
            SELECT 'pet' as type, p.created_at, 
                   p.name as pet_name, NULL as user_name, p.adoption_status as status,
                   'Pet ' || p.name || ' added' as description
            FROM pets p
            WHERE p.owner_id = ?
            ORDER BY p.created_at DESC
            LIMIT 5
        ''', (session['user_id'],)).fetchall()
        
        # Combine and sort activities
        for req in recent_requests:
            recent_activity.append({
                'type': req['type'],
                'created_at': req['created_at'],
                'pet_name': req['pet_name'],
                'user_name': req['user_name'],
                'status': req['status'],
                'description': req['description']
            })
        
        for pet in recent_pets:
            recent_activity.append({
                'type': pet['type'],
                'created_at': pet['created_at'],
                'pet_name': pet['pet_name'],
                'user_name': pet['user_name'],
                'status': pet['status'],
                'description': pet['description']
            })
        
        # Sort by date (most recent first) and limit to 10
        recent_activity.sort(key=lambda x: x['created_at'] if x['created_at'] else '', reverse=True)
        recent_activity = recent_activity[:10]
        
        categories = conn.execute('SELECT * FROM categories').fetchall()
        
        conn.close()
        
        # Convert Row objects to dictionaries for JSON serialization in template
        pets_dict = [dict(pet) for pet in pets]
        top_pets_dict = [dict(pet) for pet in top_pets]
        
        return render_template('owner_dashboard.html', 
                             pets=pets, 
                             pets_json=pets_dict,  # For JavaScript
                             requests=requests, 
                             categories=categories,
                             top_pets=top_pets,
                             stats=stats,
                             recent_activity=recent_activity)
    except Exception as e:
        return f"Owner dashboard error: {e}"

@app.route('/add-pet', methods=['POST'])
def add_pet():
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO pets (name, category_id, breed, age, health_details, medical_details, image_url, owner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['category_id'], data['breed'], data['age'],
            data['health_details'], data['medical_details'], data['image_url'], session['user_id']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Pet added successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/update-pet/<int:pet_id>', methods=['POST'])
def update_pet(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE pets SET name = ?, category_id = ?, breed = ?, age = ?, 
            health_details = ?, medical_details = ?, image_url = ?, adoption_status = ?
            WHERE id = ? AND owner_id = ?
        ''', (
            data['name'], data['category_id'], data['breed'], data['age'],
            data['health_details'], data['medical_details'], data['image_url'],
            data['adoption_status'], pet_id, session['user_id']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Pet updated successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/delete-pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM pets WHERE id = ? AND owner_id = ?', (pet_id, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Pet deleted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/update-request-status/<int:request_id>', methods=['POST'])
def update_request_status(request_id):
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        status = data.get('status')
        
        conn = get_db_connection()
        
        # Update request status
        conn.execute('UPDATE adoption_requests SET status = ? WHERE id = ?', (status, request_id))
        
        # If approved, update pet status
        if status == 'approved':
            request_info = conn.execute(
                'SELECT pet_id FROM adoption_requests WHERE id = ?', (request_id,)
            ).fetchone()
            if request_info:
                conn.execute(
                    'UPDATE pets SET adoption_status = "adopted" WHERE id = ?',
                    (request_info['pet_id'],)
                )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Request {status} successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/search_pets')
def search_pets():
    try:
        query = request.args.get('q', '').strip()
        status = request.args.get('status', 'all').strip()
        
        conn = get_db_connection()
        
        if query:
            search_term = f'%{query}%'
            if status == 'all':
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE (p.name LIKE ? OR p.breed LIKE ?)
                    GROUP BY p.id
                    LIMIT 50
                ''', (search_term, search_term)).fetchall()
            else:
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE (p.name LIKE ? OR p.breed LIKE ?) AND p.adoption_status = ?
                    GROUP BY p.id
                    LIMIT 50
                ''', (search_term, search_term, status)).fetchall()
        else:
            if status == 'all':
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    GROUP BY p.id
                    LIMIT 50
                ''').fetchall()
            else:
                pets = conn.execute('''
                    SELECT p.*, c.name as category_name,
                           COUNT(DISTINCT pl.id) as like_count
                    FROM pets p 
                    JOIN categories c ON p.category_id = c.id 
                    LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                    WHERE p.adoption_status = ?
                    GROUP BY p.id
                    LIMIT 50
                ''', (status,)).fetchall()
        
        conn.close()
        
        # Convert to list of dicts for JSON
        results = []
        for pet in pets:
            results.append({
                'id': pet['id'],
                'name': pet['name'],
                'breed': pet['breed'],
                'age': pet['age'],
                'category_name': pet['category_name'],
                'adoption_status': pet['adoption_status'],
                'image_url': pet['image_url'],
                'health_details': pet['health_details'],
                'like_count': pet['like_count'] or 0
            })
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pet/<int:pet_id>')
def pet_detail(pet_id):
    try:
        conn = get_db_connection()
        user_id = session.get('user_id') if session.get('user_type') == 'user' else None
        
        if user_id:
            pet = conn.execute('''
                SELECT p.*, c.name as category_name, o.name as owner_name, o.contact as owner_contact,
                       COUNT(DISTINCT pl.id) as like_count,
                       MAX(CASE WHEN pl.user_id = ? THEN 1 ELSE 0 END) as is_liked
                FROM pets p 
                JOIN categories c ON p.category_id = c.id 
                LEFT JOIN owners o ON p.owner_id = o.id
                LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                WHERE p.id = ?
                GROUP BY p.id
            ''', (user_id, pet_id)).fetchone()
        else:
            pet = conn.execute('''
                SELECT p.*, c.name as category_name, o.name as owner_name, o.contact as owner_contact,
                       COUNT(DISTINCT pl.id) as like_count,
                       0 as is_liked
                FROM pets p 
                JOIN categories c ON p.category_id = c.id 
                LEFT JOIN owners o ON p.owner_id = o.id
                LEFT JOIN pet_likes pl ON p.id = pl.pet_id
                WHERE p.id = ?
                GROUP BY p.id
            ''', (pet_id,)).fetchone()
        
        conn.close()
        
        if not pet:
            flash('Pet not found!', 'error')
            return redirect(url_for('adopt'))
        
        return render_template('pet_detail.html', pet=pet)
    except Exception as e:
        flash(f'Error loading pet details: {e}', 'error')
        return redirect(url_for('adopt'))

@app.route('/care')
def care_list():
    try:
        conn = get_db_connection()
        posts = conn.execute('''
            SELECT cp.*, u.name as author_name,
                   (SELECT COUNT(*) FROM care_comments WHERE post_id = cp.id) as comment_count
            FROM care_posts cp
            JOIN users u ON cp.user_id = u.id
            ORDER BY cp.created_at DESC
        ''').fetchall()
        conn.close()
        return render_template('care_list.html', posts=posts)
    except Exception as e:
        flash(f'Error loading care tips: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/care/<int:post_id>')
def care_detail(post_id):
    try:
        conn = get_db_connection()
        
        # Get the post
        post = conn.execute('''
            SELECT cp.*, u.name as author_name
            FROM care_posts cp
            JOIN users u ON cp.user_id = u.id
            WHERE cp.id = ?
        ''', (post_id,)).fetchone()
        
        if not post:
            flash('Post not found!', 'error')
            conn.close()
            return redirect(url_for('care_list'))
        
        # Get comments for this post
        comments = conn.execute('''
            SELECT cc.*, u.name as author_name
            FROM care_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.post_id = ?
            ORDER BY cc.created_at ASC
        ''', (post_id,)).fetchall()
        
        conn.close()
        return render_template('care_detail.html', post=post, comments=comments)
    except Exception as e:
        flash(f'Error loading post: {e}', 'error')
        return redirect(url_for('care_list'))

@app.route('/care/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Please login to comment.'})
    
    try:
        data = request.get_json()
        content = data.get('content', '').strip() if data else request.form.get('content', '').strip()
        
        if not content:
            return jsonify({'success': False, 'message': 'Comment cannot be empty!'})
        
        conn = get_db_connection()
        
        # Verify post exists
        post = conn.execute('SELECT id FROM care_posts WHERE id = ?', (post_id,)).fetchone()
        if not post:
            conn.close()
            return jsonify({'success': False, 'message': 'Post not found!'})
        
        # Add comment
        conn.execute('''
            INSERT INTO care_comments (post_id, user_id, content)
            VALUES (?, ?, ?)
        ''', (post_id, session['user_id'], content))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Comment added successfully!',
            'author_name': session.get('user_name', 'User')
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/care/new', methods=['GET', 'POST'])
def care_new():
    if 'user_id' not in session or session.get('user_type') != 'user':
        flash('Please login to create a care tip post.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            
            if not title or not content:
                flash('Title and content are required!', 'error')
                return render_template('care_new.html')
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO care_posts (user_id, title, content)
                VALUES (?, ?, ?)
            ''', (session['user_id'], title, content))
            conn.commit()
            conn.close()
            
            flash('Care tip posted successfully!', 'success')
            return redirect(url_for('care_list'))
        except Exception as e:
            flash(f'Error creating post: {e}', 'error')
    
    return render_template('care_new.html')

@app.route('/owner-dashboard/analytics')
def owner_analytics():
    """API endpoint for owner dashboard analytics data"""
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = get_db_connection()
        
        # Get comprehensive analytics
        analytics = {
            'pets_by_status': {},
            'requests_by_status': {},
            'requests_by_month': [],
            'top_pets': [],
            'category_distribution': []
        }
        
        # Pets by status
        pets_by_status = conn.execute('''
            SELECT adoption_status, COUNT(*) as count
            FROM pets
            WHERE owner_id = ?
            GROUP BY adoption_status
        ''', (session['user_id'],)).fetchall()
        
        for row in pets_by_status:
            analytics['pets_by_status'][row['adoption_status']] = row['count']
        
        # Requests by status
        requests_by_status = conn.execute('''
            SELECT ar.status, COUNT(*) as count
            FROM adoption_requests ar
            JOIN pets p ON ar.pet_id = p.id
            WHERE p.owner_id = ?
            GROUP BY ar.status
        ''', (session['user_id'],)).fetchall()
        
        for row in requests_by_status:
            analytics['requests_by_status'][row['status']] = row['count']
        
        # Top pets with details
        top_pets = conn.execute('''
            SELECT p.id, p.name, p.breed, p.image_url, c.name as category_name,
                   COUNT(ar.id) as request_count,
                   SUM(CASE WHEN ar.status = 'approved' THEN 1 ELSE 0 END) as approved_count,
                   SUM(CASE WHEN ar.status = 'pending' THEN 1 ELSE 0 END) as pending_count
            FROM pets p
            LEFT JOIN adoption_requests ar ON p.id = ar.pet_id
            JOIN categories c ON p.category_id = c.id
            WHERE p.owner_id = ?
            GROUP BY p.id, p.name, p.breed, p.image_url, c.name
            ORDER BY request_count DESC
            LIMIT 10
        ''', (session['user_id'],)).fetchall()
        
        analytics['top_pets'] = [dict(row) for row in top_pets]
        
        # Category distribution
        category_dist = conn.execute('''
            SELECT c.name, COUNT(p.id) as pet_count
            FROM categories c
            LEFT JOIN pets p ON c.id = p.category_id AND p.owner_id = ?
            GROUP BY c.id, c.name
            ORDER BY pet_count DESC
        ''', (session['user_id'],)).fetchall()
        
        analytics['category_distribution'] = [dict(row) for row in category_dist]
        
        conn.close()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/like-pet/<int:pet_id>', methods=['POST'])
def like_pet(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Please login to like pets.'})
    
    try:
        conn = get_db_connection()
        
        # Check if already liked
        existing = conn.execute(
            'SELECT * FROM pet_likes WHERE pet_id = ? AND user_id = ?',
            (pet_id, session['user_id'])
        ).fetchone()
        
        if existing:
            # Unlike
            conn.execute(
                'DELETE FROM pet_likes WHERE pet_id = ? AND user_id = ?',
                (pet_id, session['user_id'])
            )
            action = 'unliked'
        else:
            # Like
            conn.execute(
                'INSERT INTO pet_likes (pet_id, user_id) VALUES (?, ?)',
                (pet_id, session['user_id'])
            )
            action = 'liked'
        
        # Get updated like count
        like_count = conn.execute(
            'SELECT COUNT(*) as count FROM pet_likes WHERE pet_id = ?',
            (pet_id,)
        ).fetchone()['count']
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'action': action,
            'like_count': like_count,
            'message': f'Pet {action} successfully!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Please login to delete your profile.'})
    
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not password:
            return jsonify({'success': False, 'message': 'Password is required to delete your profile.'})
        
        # Verify password
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        
        # Check if password is correct
        user = conn.execute(
            'SELECT * FROM users WHERE id = ? AND password = ?',
            (session['user_id'], hashed_password)
        ).fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Incorrect password. Profile deletion cancelled.'})
        
        user_id = session['user_id']
        user_name = user['name']
        
        # Delete all adoption requests by this user
        conn.execute('DELETE FROM adoption_requests WHERE user_id = ?', (user_id,))
        
        # Delete the user account
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True, 
            'message': f'Profile deleted successfully. Goodbye {user_name}! You can register again anytime with the same credentials.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting profile: {e}'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🐾 Starting PetLink Application...")
    print("Initializing database...")
    init_db()
    print("Database ready!")
    print("\n" + "="*50)
    print("🌐 PetLink is running!")
    print("📍 Main site: http://localhost:5000")
    print("🔑 Owner login: http://localhost:5000/owner-login")
    print("📧 Demo owner: admin@petlink.com / admin123")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)