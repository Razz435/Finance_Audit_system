from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Project, Audit, Transaction, Finding, User
from datetime import datetime, date
from functools import wraps

main_bp = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
@login_required
def dashboard():
    # Get statistics for dashboard
    total_projects = Project.query.filter_by(user_id=current_user.id).count() if current_user.role == 'user' else Project.query.count()
    total_audits = Audit.query.count()
    total_budget = db.session.query(db.func.sum(Project.budget_amount)).scalar() or 0
    total_actual = db.session.query(db.func.sum(Project.actual_amount)).scalar() or 0
    
    # Recent projects
    if current_user.role == 'admin':
        recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
        recent_audits = Audit.query.order_by(Audit.created_at.desc()).limit(5).all()
    else:
        recent_projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_at.desc()).limit(5).all()
        recent_audits = Audit.query.join(Project).filter(Project.user_id == current_user.id).order_by(Audit.created_at.desc()).limit(5).all()
    
    # Projects by status
    active_projects = Project.query.filter_by(status='active').count()
    completed_projects = Project.query.filter_by(status='completed').count()
    
    # High risk projects
    high_risk_projects = Project.query.filter_by(risk_level='high').count()
    
    return render_template('index.html', 
                         total_projects=total_projects,
                         total_audits=total_audits,
                         total_budget=total_budget,
                         total_actual=total_actual,
                         recent_projects=recent_projects,
                         recent_audits=recent_audits,
                         active_projects=active_projects,
                         completed_projects=completed_projects,
                         high_risk_projects=high_risk_projects)

@main_bp.route('/projects')
@login_required
def projects():
    if current_user.role == 'admin':
        projects_list = Project.query.order_by(Project.created_at.desc()).all()
    else:
        projects_list = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=projects_list)

@main_bp.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        project = Project(
            project_name=request.form.get('project_name'),
            project_code=request.form.get('project_code'),
            description=request.form.get('description'),
            budget_amount=float(request.form.get('budget_amount')),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
            status=request.form.get('status'),
            risk_level=request.form.get('risk_level'),
            department=request.form.get('department'),
            user_id=current_user.id
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project added successfully!', 'success')
        return redirect(url_for('main.projects'))
    
    return render_template('add_project.html')

@main_bp.route('/project/<int:id>')
@login_required
def project_detail(id):
    project = Project.query.get_or_404(id)
    
    # Check permissions
    if current_user.role != 'admin' and project.user_id != current_user.id:
        flash('You do not have permission to view this project.', 'danger')
        return redirect(url_for('main.projects'))
    
    audits = Audit.query.filter_by(project_id=id).all()
    transactions = Transaction.query.filter_by(project_id=id).all()
    
    return render_template('project_detail.html', project=project, audits=audits, transactions=transactions)

@main_bp.route('/project/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if current_user.role != 'admin' and project.user_id != current_user.id:
        flash('You do not have permission to edit this project.', 'danger')
        return redirect(url_for('main.projects'))
    
    if request.method == 'POST':
        project.project_name = request.form.get('project_name')
        project.description = request.form.get('description')
        project.budget_amount = float(request.form.get('budget_amount'))
        project.actual_amount = float(request.form.get('actual_amount'))
        project.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        project.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None
        project.status = request.form.get('status')
        project.risk_level = request.form.get('risk_level')
        project.department = request.form.get('department')
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.project_detail', id=project.id))
    
    return render_template('add_project.html', project=project)

@main_bp.route('/project/<int:id>/delete')
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    
    if current_user.role != 'admin' and project.user_id != current_user.id:
        flash('You do not have permission to delete this project.', 'danger')
        return redirect(url_for('main.projects'))
    
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.projects'))

@main_bp.route('/audits')
@login_required
def audits():
    if current_user.role == 'admin':
        audits_list = Audit.query.order_by(Audit.created_at.desc()).all()
    else:
        audits_list = Audit.query.join(Project).filter(Project.user_id == current_user.id).order_by(Audit.created_at.desc()).all()
    return render_template('audits.html', audits=audits_list)

@main_bp.route('/audit/add', methods=['GET', 'POST'])
@login_required
def add_audit():
    if current_user.role == 'admin':
        projects = Project.query.all()
    else:
        projects = Project.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        audit = Audit(
            audit_name=request.form.get('audit_name'),
            audit_type=request.form.get('audit_type'),
            audit_date=datetime.strptime(request.form.get('audit_date'), '%Y-%m-%d').date(),
            findings=request.form.get('findings'),
            recommendations=request.form.get('recommendations'),
            status=request.form.get('status'),
            risk_score=float(request.form.get('risk_score')) if request.form.get('risk_score') else 0.0,
            compliance_score=float(request.form.get('compliance_score')) if request.form.get('compliance_score') else 0.0,
            project_id=int(request.form.get('project_id')),
            user_id=current_user.id
        )
        
        db.session.add(audit)
        db.session.commit()
        
        flash('Audit added successfully!', 'success')
        return redirect(url_for('main.audits'))
    
    return render_template('add_audit.html', projects=projects)

@main_bp.route('/reports')
@login_required
def reports():
    # Generate financial reports
    projects = Project.query.all() if current_user.role == 'admin' else Project.query.filter_by(user_id=current_user.id).all()
    
    total_budget = sum(p.budget_amount for p in projects)
    total_actual = sum(p.actual_amount for p in projects)
    total_variance = total_budget - total_actual
    
    # Projects by status
    status_counts = {}
    for status in ['active', 'completed', 'on_hold', 'cancelled']:
        status_counts[status] = len([p for p in projects if p.status == status])
    
    # Risk distribution
    risk_counts = {}
    for risk in ['low', 'medium', 'high', 'critical']:
        risk_counts[risk] = len([p for p in projects if p.risk_level == risk])
    
    # Audit statistics
    audits = Audit.query.all() if current_user.role == 'admin' else Audit.query.join(Project).filter(Project.user_id == current_user.id).all()
    avg_risk_score = sum(a.risk_score for a in audits) / len(audits) if audits else 0
    avg_compliance = sum(a.compliance_score for a in audits) / len(audits) if audits else 0
    
    return render_template('reports.html',
                         total_budget=total_budget,
                         total_actual=total_actual,
                         total_variance=total_variance,
                         status_counts=status_counts,
                         risk_counts=risk_counts,
                         avg_risk_score=avg_risk_score,
                         avg_compliance=avg_compliance,
                         total_projects=len(projects),
                         total_audits=len(audits))

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.email = request.form.get('email')
        
        if request.form.get('new_password'):
            if current_user.check_password(request.form.get('current_password')):
                current_user.set_password(request.form.get('new_password'))
                flash('Password updated successfully!', 'success')
            else:
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('main.profile'))
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html')

@main_bp.route('/api/stats')
@login_required
def api_stats():
    # API endpoint for charts and statistics
    projects = Project.query.filter_by(user_id=current_user.id).all() if current_user.role == 'user' else Project.query.all()
    
    stats = {
        'total_projects': len(projects),
        'total_budget': sum(p.budget_amount for p in projects),
        'total_actual': sum(p.actual_amount for p in projects),
        'projects_by_status': {},
        'budget_utilization': []
    }
    
    for status in ['active', 'completed', 'on_hold']:
        stats['projects_by_status'][status] = len([p for p in projects if p.status == status])
    
    for project in projects[:10]:  # Last 10 projects
        stats['budget_utilization'].append({
            'name': project.project_name,
            'budget': project.budget_amount,
            'actual': project.actual_amount
        })
    
    return jsonify(stats)