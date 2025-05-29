from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edu_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_teacher = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))
    courses = db.relationship('Course', backref='instructor', lazy=True)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50))
    level = db.Column(db.String(20))
    lessons = db.relationship('Lesson', backref='course', lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    materials = db.relationship('CourseMaterial', backref='course', lazy=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.Column(db.Integer, default=0)
    materials = db.relationship('LessonMaterial', backref='lesson', lazy=True)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=0)  # Progress percentage

class CourseMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class LessonMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    courses = Course.query.all()
    categories = db.session.query(Course.category).distinct().all()
    return render_template('index.html', courses=courses, categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_teacher = request.form.get('is_teacher') == 'on'
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, is_teacher=is_teacher)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    enrolled_courses = Enrollment.query.filter_by(user_id=current_user.id).all()
    if current_user.is_teacher:
        created_courses = Course.query.filter_by(instructor_id=current_user.id).all()
    else:
        created_courses = []
    return render_template('profile.html', enrolled_courses=enrolled_courses, created_courses=created_courses)

@app.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if not current_user.is_teacher:
        flash('Only teachers can create courses')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        level = request.form.get('level')
        
        course = Course(
            title=title,
            description=description,
            category=category,
            level=level,
            instructor_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        
        flash('Course created successfully!')
        return redirect(url_for('course_detail', course_id=course.id))
    
    return render_template('create_course.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    is_enrolled = False
    if current_user.is_authenticated:
        is_enrolled = Enrollment.query.filter_by(
            user_id=current_user.id,
            course_id=course_id
        ).first() is not None
    return render_template('course_detail.html', course=course, is_enrolled=is_enrolled)

@app.route('/course/<int:course_id>/enroll')
@login_required
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check if user is already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course!')
        return redirect(url_for('course_detail', course_id=course_id))
    
    # Check if user is the course instructor
    if current_user.id == course.instructor_id:
        flash('You cannot enroll in your own course!')
        return redirect(url_for('course_detail', course_id=course_id))
    
    # Create new enrollment
    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    try:
        db.session.add(enrollment)
        db.session.commit()
        flash('Successfully enrolled in the course!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while enrolling in the course. Please try again.')
    
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/course/<int:course_id>/lesson/create', methods=['GET', 'POST'])
@login_required
def create_lesson(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.instructor_id:
        flash('Only the course instructor can add lessons')
        return redirect(url_for('course_detail', course_id=course_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        order = request.form.get('order', type=int)
        
        lesson = Lesson(
            title=title,
            content=content,
            course_id=course_id,
            order=order
        )
        db.session.add(lesson)
        db.session.commit()
        
        flash('Lesson added successfully!')
        return redirect(url_for('course_detail', course_id=course_id))
    
    return render_template('create_lesson.html', course=course)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    level = request.args.get('level', '')
    
    courses = Course.query
    
    if query:
        courses = courses.filter(Course.title.ilike(f'%{query}%') | Course.description.ilike(f'%{query}%'))
    if category:
        courses = courses.filter_by(category=category)
    if level:
        courses = courses.filter_by(level=level)
    
    courses = courses.all()
    categories = db.session.query(Course.category).distinct().all()
    
    return render_template('search.html', courses=courses, categories=categories, query=query, selected_category=category, selected_level=level)

if __name__ == '__main__':
    app.run(debug=True) 