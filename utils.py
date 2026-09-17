import os
import re
import uuid
from functools import wraps

from flask import session, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Please log in to access the admin panel.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return wrapper


def super_admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Please log in to access the admin panel.", "warning")
            return redirect(url_for("admin.login"))
        if session.get("admin_role") != "Super Admin":
            flash("You do not have permission to access that page.", "danger")
            return redirect(url_for("admin.dashboard"))
        return f(*args, **kwargs)
    return wrapper


def allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file_storage, prefix="img"):
    """Validate and save an uploaded image. Returns the public path or None."""
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_file(file_storage.filename):
        raise ValueError("Invalid file type. Only JPG, JPEG, PNG and WebP are allowed.")

    safe_name = secure_filename(file_storage.filename)
    ext = safe_name.rsplit(".", 1)[-1].lower()
    unique_name = f"{prefix}-{uuid.uuid4().hex[:12]}.{ext}"
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_name)
    file_storage.save(file_path)
    return f"/static/uploads/{unique_name}"


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email or ""))


def is_valid_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    return 7 <= len(digits) <= 15
