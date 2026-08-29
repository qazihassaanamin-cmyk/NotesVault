from flask import Blueprint, render_template, request
from models import Resource, Category

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category_id')
    
    results = Resource.query
    if query:
        results = results.filter(Resource.title.ilike(f'%{query}%') | Resource.subject.ilike(f'%{query}%'))
    if category_id:
        results = results.filter_by(category_id=category_id)
        
    resources = results.order_by(Resource.uploaded_at.desc()).all()
    categories = Category.query.all()
    return render_template('search_results.html', resources=resources, query=query, categories=categories)