from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    status = db.Column(db.String(20), nullable=False, default='To Do')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/tasks', methods=['GET', 'POST'])
@jwt_required()
def manage_tasks():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.get_json()
        task = Task(
            title=data['title'],
            description=data.get('description'),
            due_date=data.get('due_date'),
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'To Do'),
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority,
        'status': task.status
    } for task in tasks]), 200

if __name__ == '__main__':
    app.run(debug=True)
