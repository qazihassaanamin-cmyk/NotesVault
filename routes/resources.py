from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Resource

resources = Blueprint('resources', __name__)

# Public Marketplace View (Shows public free and paid note previews)
@resources.route('/marketplace')
def marketplace():
    subject_filter = request.args.get('subject')
    query = Resource.query.filter_by(is_private=False)
    
    if subject_filter:
        query = query.filter_by(subject=subject_filter)
        
    all_resources = query.order_by(Resource.created_at.desc()).all()
    return render_template('marketplace.html', resources=all_resources)

# Personal User Dashboard (Shows user's uploads + unlocked notes)
@resources.route('/dashboard')
@login_required
def dashboard():
    my_notes = Resource.query.filter_by(user_id=current_user.id).all()
    unlocked_notes = current_user.unlocked_resources
    return render_template('dashboard.html', my_notes=my_notes, unlocked_notes=unlocked_notes)

# Create New Resource
@resources.route('/resource/new', methods=['GET', 'POST'])
@login_required
def create_resource():
    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        description = request.form.get('description')
        resource_link = request.form.get('resource_link')
        is_private = 'is_private' in request.form
        is_paid = 'is_paid' in request.form
        price = float(request.form.get('price', 0.0)) if is_paid else 0.0

        new_resource = Resource(
            title=title,
            subject=subject,
            description=description,
            resource_link=resource_link,
            is_private=is_private,
            is_paid=is_paid,
            price=price,
            user_id=current_user.id
        )
        db.session.add(new_resource)
        db.session.commit()
        flash('Resource published successfully!', 'success')
        return redirect(url_for('resources.dashboard'))

    return render_template('create_resource.html')

# View Resource Detail (Enforces Privacy & Purchase Locks)
@resources.route('/resource/<int:id>')
def view_resource(id):
    resource = Resource.query.get_or_404(id)
    
    # 1. Privacy Check
    if resource.is_private:
        if not current_user.is_authenticated or resource.user_id != current_user.id:
            flash('This note is private to the owner.', 'danger')
            return redirect(url_for('resources.marketplace'))

    # 2. Access Lock Check (Paid notes require ownership or purchase)
    has_access = False
    if current_user.is_authenticated:
        if resource.user_id == current_user.id or resource in current_user.unlocked_resources:
            has_access = True
            
    if not resource.is_paid:
        has_access = True

    return render_template('resource_detail.html', resource=resource, has_access=has_access)

# Unlock / Buy Note Action
@resources.route('/resource/<int:id>/buy', methods=['POST'])
@login_required
def buy_resource(id):
    resource = Resource.query.get_or_404(id)
    if resource not in current_user.unlocked_resources and resource.user_id != current_user.id:
        current_user.unlocked_resources.append(resource)
        db.session.commit()
        flash(f'Successfully unlocked "{resource.title}"!', 'success')
    return redirect(url_for('resources.view_resource', id=resource.id))

# Delete Resource (Owner Only)
@resources.route('/resource/<int:id>/delete', methods=['POST'])
@login_required
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    if resource.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('resources.dashboard'))
        
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted successfully.', 'info')
    return redirect(url_for('resources.dashboard'))