from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, Resource, Category
from utils.file_handler import allowed_file, save_unique_file

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/dashboard')
@login_required
def dashboard():
    resources = Resource.query.order_by(Resource.uploaded_at.desc()).limit(20).all()
    categories = Category.query.all()
    return render_template('dashboard.html', resources=resources, categories=categories)

@resources_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        subject = request.form.get('subject')
        description = request.form.get('description')
        
        if not file or not allowed_file(file.filename):
            flash('Invalid file extension.', 'danger')
            return redirect(url_for('resources.upload'))
            
        saved_filename = save_unique_file(file, current_app.config['UPLOAD_FOLDER'])
        
        new_resource = Resource(
            title=title,
            file_path=saved_filename,
            subject=subject,
            description=description,
            category_id=category_id,
            user_id=current_user.id
        )
        db.session.add(new_resource)
        db.session.commit()
        
        flash('Resource uploaded successfully!', 'success')
        return redirect(url_for('resources.dashboard'))
        
    categories = Category.query.all()
    return render_template('upload.html', categories=categories)