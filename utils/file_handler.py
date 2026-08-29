import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'py', 'txt', 'docx', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_unique_file(file, upload_folder):
    original_filename = secure_filename(file.filename)
    unique_prefix = uuid.uuid4().hex[:8]
    saved_filename = f"{unique_prefix}_{original_filename}"
    
    os.makedirs(upload_folder, exist_ok=True)
    full_path = os.path.join(upload_folder, saved_filename)
    file.save(full_path)
    
    return saved_filename