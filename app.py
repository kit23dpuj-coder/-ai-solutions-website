from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import sqlite3
import hashlib
import re
from datetime import datetime
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = 'ai_solutions_super_secret_key_2026_secure'

# ===== EMAIL CONFIG (Gmail) =====
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # CHANGE THIS
app.config['MAIL_PASSWORD'] = 'your_app_password'      # CHANGE THIS
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        # Inquiries table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                company TEXT,
                country TEXT NOT NULL,
                job_title TEXT NOT NULL,
                job_details TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                reply TEXT,
                replied_at TIMESTAMP,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Feedback table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Admin table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                twofa_secret TEXT
            )
        ''')
        admin = conn.execute('SELECT * FROM admin WHERE username = "admin"').fetchone()
        if not admin:
            pwd_hash = hashlib.sha256('Admin@2026'.encode()).hexdigest()
            secret = pyotp.random_base32()
            conn.execute('INSERT INTO admin (username, password_hash, twofa_secret) VALUES (?, ?, ?)',
                         ('admin', pwd_hash, secret))
        conn.commit()
init_db()

def generate_qr_code(secret, username):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="AI-Solutions")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ========== PUBLIC PAGES ==========
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/solutions')
def solutions():
    return render_template('solutions.html')

@app.route('/past-work')
def past_work():
    return render_template('past_work.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        if not all([name, email, rating]):
            flash('Please fill name, email and rating.', 'danger')
            return redirect(url_for('feedback'))
        with get_db() as conn:
            conn.execute('INSERT INTO feedback (name, email, rating, comment) VALUES (?,?,?,?)',
                         (name, email, int(rating), comment))
            conn.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
    with get_db() as conn:
        all_feedback = conn.execute('SELECT * FROM feedback ORDER BY submitted_at DESC').fetchall()
        avg_row = conn.execute('SELECT AVG(rating) as avg FROM feedback').fetchone()
        avg_rating = avg_row['avg'] if avg_row['avg'] else 0
    return render_template('feedback.html', feedbacks=all_feedback, avg_rating=avg_rating)

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')
        country = request.form.get('country')
        job_title = request.form.get('job_title')
        job_details = request.form.get('job_details')
        
        if not all([name, email, phone, country, job_title, job_details]):
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('contact'))
        
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('contact'))
        
        phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not re.match(r'^[0-9]{10}$', phone_clean):
            flash('Phone must be exactly 10 digits (e.g., 9841234567).', 'danger')
            return redirect(url_for('contact'))
        
        with get_db() as conn:
            conn.execute('''
                INSERT INTO inquiries (name, email, phone, company, country, job_title, job_details)
                VALUES (?,?,?,?,?,?,?)
            ''', (name, email, phone, company, country, job_title, job_details))
            conn.commit()
        
        try:
            msg = Message(
                subject=f"New Inquiry from {name}",
                recipients=['admin@aisolutions.com']
            )
            msg.body = f"""
            New Inquiry Received!
            
            Name: {name}
            Email: {email}
            Phone: {phone}
            Company: {company or 'N/A'}
            Country: {country}
            Job Title: {job_title}
            
            Requirements:
            {job_details}
            
            Please login to admin dashboard to reply.
            """
            mail.send(msg)
        except Exception as e:
            print(f"Email error: {e}")
        
        flash('Your inquiry has been submitted. We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/chatbot-page')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_api():
    import json
    data = request.get_json()
    msg = data.get('message', '').lower()
    
    responses = {
        'hello': 'Hello! I am AI-Solutions virtual assistant. How can I help you today? 😊',
        'hi': 'Hi there! Welcome to AI-Solutions. Ask me about our AI services, demos, or contact us for more info.',
        'hey': 'Hey! How can I assist you today?',
        'good morning': 'Good morning! ☀️ How can I help you today?',
        'good evening': 'Good evening! 🌙 How can I assist you?',
        'what do you do': 'AI-Solutions provides AI-powered virtual assistants, rapid prototyping, employee analytics, and custom AI models for businesses worldwide.',
        'services': 'We offer: 1️⃣ AI Virtual Assistant 2️⃣ Rapid Prototyping 3️⃣ Employee Analytics 4️⃣ Secure AI Gateway 5️⃣ Custom AI Models 6️⃣ Cloud AI Deployment.',
        'about': 'AI-Solutions is a Sunderland-based startup that leverages AI to improve digital employee experience and speed up innovation.',
        'virtual assistant': 'Our AI Virtual Assistant provides 24/7 intelligent support, natural conversations, and instant resolutions. It integrates with Slack, Teams, and web platforms.',
        'prototyping': 'Rapid Prototyping helps you test AI ideas in days, not months. We build affordable prototypes to accelerate your product design.',
        'analytics': 'Employee Analytics provides real-time insights into digital employee experience and productivity, helping you identify friction points.',
        'pricing': 'Our AI Assistant starts at $499/month. For custom solutions, contact us for a personalized quote.',
        'demo': 'To schedule a demo, please fill the Contact Us form. Our team will reach out within 24 hours.',
        'schedule demo': 'Visit our Contact page and submit your details. We will arrange a personalized demo for you.',
        'contact': 'You can reach us via the Contact Us form or email us at hello@aisolutions.com.',
        'human': 'Connecting you to a human agent. Please wait... Our team will contact you within 2 hours. 📧',
        'talk to agent': 'I am transferring you to a human representative. Expect an email within 2 hours.',
        'help': 'You can ask me about: 📌 Our AI Services 📌 Demo 📌 Pricing 📌 Virtual Assistant 📌 Prototyping 📌 Contact Information 📌 Human Agent',
        'thank you': 'You\'re welcome! 😊 Feel free to ask anything else.',
        'thanks': 'Glad to help! 😊',
        'bye': 'Goodbye! Have a great day. Come back if you need anything. 👋',
    }
    
    for keyword, response in responses.items():
        if keyword in msg:
            return {'response': response}
    
    return {'response': "I'm still learning! Please visit our Contact Us page for detailed inquiries, or ask me about: services, demo, pricing, virtual assistant, prototyping, or help."}

# ========== ADMIN ==========
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with get_db() as conn:
            admin = conn.execute('SELECT * FROM admin WHERE username = ?', (username,)).fetchone()
        if admin:
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            if pwd_hash == admin['password_hash']:
                qr_img = generate_qr_code(admin['twofa_secret'], username)
                session['2fa_temp_username'] = username
                session['2fa_qr'] = qr_img
                flash('Scan QR code with Google Authenticator', 'info')
                return redirect(url_for('admin_2fa'))
        flash('Invalid username or password.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/2fa', methods=['GET', 'POST'])
def admin_2fa():
    if '2fa_temp_username' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        user_code = request.form.get('code')
        username = session.get('2fa_temp_username')
        with get_db() as conn:
            admin = conn.execute('SELECT * FROM admin WHERE username = ?', (username,)).fetchone()
        if admin:
            totp = pyotp.TOTP(admin['twofa_secret'])
            if totp.verify(user_code):
                session['admin_logged_in'] = True
                session.pop('2fa_temp_username', None)
                session.pop('2fa_qr', None)
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Invalid 2FA code.', 'danger')
    return render_template('admin_2fa.html', qr_img=session.get('2fa_qr', ''))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    with get_db() as conn:
        inquiries = conn.execute('SELECT * FROM inquiries ORDER BY submitted_at DESC').fetchall()
        feedbacks = conn.execute('SELECT * FROM feedback ORDER BY submitted_at DESC').fetchall()
    return render_template('admin_dashboard.html', 
                           inquiries=inquiries, 
                           feedbacks=feedbacks,
                           total_inquiries=len(inquiries),
                           total_feedbacks=len(feedbacks))

@app.route('/admin/reply/<int:id>', methods=['POST'])
def admin_reply(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    reply_text = request.form.get('reply')
    if reply_text:
        with get_db() as conn:
            inquiry = conn.execute('SELECT * FROM inquiries WHERE id = ?', (id,)).fetchone()
            conn.execute('UPDATE inquiries SET reply = ?, status = "replied", replied_at = CURRENT_TIMESTAMP WHERE id = ?',
                         (reply_text, id))
            conn.commit()
        
        if inquiry:
            try:
                msg = Message(
                    subject=f"Response to your inquiry - AI-Solutions",
                    recipients=[inquiry['email']]
                )
                msg.body = f"""
                Dear {inquiry['name']},
                
                Thank you for contacting AI-Solutions.
                
                Our team has reviewed your inquiry:
                
                Your Request: {inquiry['job_details']}
                
                Our Response:
                {reply_text}
                
                We will email you soon with further details.
                
                If you have any further questions, please reply to this email or contact us at hello@aisolutions.com.
                
                Best regards,
                AI-Solutions Team
                """
                mail.send(msg)
                flash('Reply sent successfully! Customer will receive an email.', 'success')
            except Exception as e:
                flash('Reply saved. We will email you soon.', 'success')
                print(f"Reply email error: {e}")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:id>')
def delete_inquiry(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    with get_db() as conn:
        conn.execute('DELETE FROM inquiries WHERE id = ?', (id,))
        conn.commit()
    flash('Inquiry deleted.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

# ========== RUN SERVER WITH AUTO-REDIRECT ==========
if __name__ == '__main__':
    import webbrowser
    import threading
    threading.Timer(1.5, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)