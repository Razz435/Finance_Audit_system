from database import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, auditor, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    projects = db.relationship('Project', backref='owner', lazy=True)
    audits = db.relationship('Audit', backref='auditor', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    project_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    budget_amount = db.Column(db.Float, nullable=False)
    actual_amount = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, on_hold, cancelled
    risk_level = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    audits = db.relationship('Audit', backref='project', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='project', lazy=True, cascade='all, delete-orphan')
    
    @property
    def budget_utilization(self):
        if self.budget_amount > 0:
            return (self.actual_amount / self.budget_amount) * 100
        return 0
    
    @property
    def variance(self):
        return self.budget_amount - self.actual_amount
    
    def __repr__(self):
        return f'<Project {self.project_code}>'

class Audit(db.Model):
    __tablename__ = 'audits'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_name = db.Column(db.String(200), nullable=False)
    audit_type = db.Column(db.String(50), nullable=False)  # internal, external, compliance, financial
    audit_date = db.Column(db.Date, nullable=False)
    findings = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, rejected
    risk_score = db.Column(db.Float, default=0.0)
    compliance_score = db.Column(db.Float, default=0.0)
    audit_file = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    findings_list = db.relationship('Finding', backref='audit', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Audit {self.audit_name}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))  # labor, materials, equipment, services, other
    vendor = db.Column(db.String(100))
    invoice_number = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    receipt_file = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Transaction {self.id} - {self.amount}>'

class Finding(db.Model):
    __tablename__ = 'findings'
    
    id = db.Column(db.Integer, primary_key=True)
    finding_type = db.Column(db.String(50))  # non-compliance, financial_irregularity, process_gap, other
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    description = db.Column(db.Text, nullable=False)
    corrective_action = db.Column(db.Text)
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    resolved_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
    
    def __repr__(self):
        return f'<Finding {self.id} - {self.finding_type}>'