# ==== Import Required Libraries ====
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

# ==== Flask App & Configurations ====
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:FOMM04122004@localhost/project_management'
# Note: Replace 'root' and 'FOMM04122004' with your MySQL username and password
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'FOMM04122004@StakeHolders'

# ==== Initialize Extensions ====
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

# ==== Database Models ====

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    status = db.Column(db.String(50))

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    assigned_to = db.Column(db.String(100))
    status = db.Column(db.String(50))
    priority = db.Column(db.String(50))
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

# Stakeholder Model
class Stakeholder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    notes = db.Column(db.Text)

# Communication Log Model
class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stakeholder_name = db.Column(db.String(100))
    method = db.Column(db.String(50))  # Email, Phone, Meeting etc.
    notes = db.Column(db.Text)
    date = db.Column(db.String(20))


# ==== User Authentication Routes ====

# Register a New User
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login and Generate JWT Token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token})
    return jsonify({"error": "Invalid credentials"}), 401

# ==== User Profile Routes ====
@app.route('/user-info', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })  

# ==== Project Routes ====

# Get All Projects
@app.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    projects = Project.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "description": p.description,
            "start_date": p.start_date,
            "end_date": p.end_date,
            "status": p.status
        } for p in projects
    ])

# Get Project by ID
@app.route('/project/<int:id>', methods=['GET'])
@jwt_required()
def get_project_by_id(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({
        "id": project.id,
        "name": project.name,
        "category": project.category,
        "description": project.description,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "status": project.status
    })

# ==== Task Management Routes ====

# Create New Task
@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    try:
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    task = Task(
        title=data['title'],
        description=data.get('description'),
        assigned_to=data.get('assigned_to'),
        status=data.get('status', 'Pending'),
        priority=data.get('priority', 'Medium'),
        due_date=due_date,
        project_id=data.get('project_id')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task_id": task.id}), 201

# Get All Tasks
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "assigned_to": t.assigned_to,
            "status": t.status,
            "priority": t.priority,
            "due_date": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            "created_at": t.created_at.strftime('%Y-%m-%d %H:%M'),
            "updated_at": t.updated_at.strftime('%Y-%m-%d %H:%M'),
            "project_id": t.project_id
        } for t in tasks
    ])

# Get Task by ID
@app.route('/tasks/<int:id>', methods=['GET'])
@jwt_required()
def get_task_by_id(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "assigned_to": task.assigned_to,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        "created_at": task.created_at.strftime('%Y-%m-%d %H:%M'),
        "updated_at": task.updated_at.strftime('%Y-%m-%d %H:%M'),
        "project_id": task.project_id
    })

# Update Task by ID
@app.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    try:
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.assigned_to = data.get('assigned_to', task.assigned_to)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        if data.get('due_date'):
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

# Delete Task by ID
@app.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

# ==== Stakeholder Management Routes ====

@app.route('/stakeholders', methods=['POST'])
@jwt_required()
def add_stakeholder():
    data = request.get_json()
    stakeholder = Stakeholder(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        role=data['role'],
        organization=data['organization'],
        notes=data.get('notes', '')
    )
    db.session.add(stakeholder)
    db.session.commit()
    return jsonify({"message": "Stakeholder added successfully"}), 201

@app.route('/stakeholders', methods=['GET'])
@jwt_required()
def get_stakeholders():
    stakeholders = Stakeholder.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "email": s.email,
        "phone": s.phone,
        "role": s.role,
        "organization": s.organization,
        "notes": s.notes
    } for s in stakeholders])

# ==== Communication Routes ====

@app.route('/communications', methods=['POST'])
@jwt_required()
def add_communication():
    data = request.get_json()
    communication = Communication(
        stakeholder_name=data['stakeholder_name'],
        method=data['method'],
        notes=data.get('notes', ''),
        date=data.get('date', datetime.today().strftime('%Y-%m-%d'))
    )
    db.session.add(communication)
    db.session.commit()
    return jsonify({"message": "Communication log added"}), 201

@app.route('/communications', methods=['GET'])
@jwt_required()
def get_communications():
    communications = Communication.query.all()
    return jsonify([{
        "id": c.id,
        "stakeholder_name": c.stakeholder_name,
        "method": c.method,
        "notes": c.notes,
        "date": c.date
    } for c in communications])

# ==== Summary Report ====

@app.route('/reports', methods=['GET'])
@jwt_required()
def reports():
    return jsonify({
        "total_projects": Project.query.count(),
        "total_stakeholders": Stakeholder.query.count(),
        "total_communications": Communication.query.count()
    })

# ==== App Entry Point ====
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)