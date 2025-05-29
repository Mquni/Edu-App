# EduPlatform - Online Learning Management System

EduPlatform is a modern web-based learning management system built with Python Flask. It provides a platform for instructors to create and manage courses, and for students to enroll in and learn from these courses.

![EduPlatform Screenshot](https://img.freepik.com/free-vector/online-learning-isometric-concept_1284-17947.jpg)

## Features

### For Students
- Browse and search courses by category and level
- Enroll in courses
- Track learning progress
- Access course materials and lessons
- View enrolled courses in profile
- Responsive design for all devices

### For Instructors
- Create and manage courses
- Add lessons and course materials
- Track student enrollment
- Manage course content
- Upload course materials
- View teaching statistics

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: 
  - HTML5
  - CSS3
  - Bootstrap 5
  - Font Awesome Icons
  - Google Fonts (Poppins)
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/edu-platform.git
cd edu-platform
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database:
```bash
python init_db.py
```

6. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
edu-platform/
├── app.py                 # Main application file
├── init_db.py            # Database initialization script
├── requirements.txt      # Project dependencies
├── static/              # Static files
│   └── uploads/         # Uploaded course materials
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Home page
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── profile.html     # User profile page
    ├── course_detail.html   # Course details page
    ├── create_course.html   # Course creation page
    ├── create_lesson.html   # Lesson creation page
    └── search.html      # Course search page
```

## Database Models

- **User**: Stores user information and authentication details
- **Course**: Contains course information and instructor details
- **Lesson**: Stores lesson content and course association
- **Enrollment**: Manages student enrollments in courses
- **CourseMaterial**: Handles course-related materials
- **LessonMaterial**: Manages lesson-specific materials

## Features in Detail

### User Authentication
- User registration with role selection (Student/Teacher)
- Secure login system
- Password hashing for security
- User profile management

### Course Management
- Course creation with title, description, category, and level
- Lesson creation and organization
- Material upload functionality
- Course enrollment system

### Search and Filtering
- Search courses by title and description
- Filter by category and difficulty level
- Responsive search results

### User Dashboard
- View enrolled courses
- Track learning progress
- Access course materials
- Manage created courses (for instructors)

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Icons provided by [Font Awesome](https://fontawesome.com/)
- Illustrations from [Freepik](https://www.freepik.com/)
- Fonts from [Google Fonts](https://fonts.google.com/)

## Contact

For any queries or support, please contact:
- Email: support@eduplatform.com
- Phone: +1 234 567 890

## Future Enhancements

- [ ] Add video lesson support
- [ ] Implement course ratings and reviews
- [ ] Add discussion forums
- [ ] Integrate payment system
- [ ] Add course completion certificates
- [ ] Implement real-time notifications
- [ ] Add mobile application
- [ ] Integrate with popular LMS systems
