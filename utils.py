import os
import re
import uuid
from functools import wraps

from flask import session, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader


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
    """Validate and upload an image to Cloudinary. Returns the secure URL or None."""
    if not file_storage or file_storage.filename == "":
        return None

    if not allowed_file(file_storage.filename):
        raise ValueError("Invalid file type. Only JPG, JPEG, PNG and WebP are allowed.")

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

    if not all([
        os.getenv("CLOUDINARY_CLOUD_NAME"),
        os.getenv("CLOUDINARY_API_KEY"),
        os.getenv("CLOUDINARY_API_SECRET")
    ]):
        raise ValueError("Cloudinary configuration is missing.")

    try:
        result = cloudinary.uploader.upload(
            file_storage,
            folder="aman_enterprise",
            public_id=f"{prefix}-{uuid.uuid4().hex[:12]}",
            resource_type="image"
        )
    except Exception as e:
        raise ValueError(f"Image upload failed: {e}")

    return result.get("secure_url")


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email or ""))


def is_valid_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    return 7 <= len(digits) <= 15
