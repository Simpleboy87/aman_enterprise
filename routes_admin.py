from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
)
from werkzeug.security import generate_password_hash, check_password_hash

from db import query, execute
from utils import login_required, super_admin_required, save_upload, is_valid_email

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ============================================================
# AUTH
# ============================================================

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        admin = query("SELECT * FROM admins WHERE email=%s", (email,), fetchone=True)

        if admin and admin["status"] == "Active" and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["name"]
            session["admin_role"] = admin["role"]
            session.permanent = bool(request.form.get("remember"))
            flash(f"Welcome back, {admin['name']}!", "success")
            return redirect(url_for("admin.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


# ============================================================
# DASHBOARD
# ============================================================

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "total_enquiries": query("SELECT COUNT(*) c FROM enquiries", fetchone=True)["c"],
        "new_enquiries": query("SELECT COUNT(*) c FROM enquiries WHERE status='New'", fetchone=True)["c"],
        "total_services": query("SELECT COUNT(*) c FROM services", fetchone=True)["c"],
        "total_equipment": query("SELECT COUNT(*) c FROM equipment", fetchone=True)["c"],
        "total_projects": query("SELECT COUNT(*) c FROM projects", fetchone=True)["c"],
        "total_testimonials": query("SELECT COUNT(*) c FROM testimonials", fetchone=True)["c"],
        "total_admins": query("SELECT COUNT(*) c FROM admins", fetchone=True)["c"],
    }
    recent_enquiries = query("SELECT * FROM enquiries ORDER BY created_at DESC LIMIT 5")
    return render_template("admin/dashboard.html", stats=stats, recent_enquiries=recent_enquiries)


# ============================================================
# SERVICES
# ============================================================

@admin_bp.route("/services")
@login_required
def services_list():
    rows = query("SELECT * FROM services ORDER BY created_at DESC")
    return render_template("admin/services.html", services=rows)


@admin_bp.route("/services/add", methods=["POST"])
@login_required
def services_add():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "fa-solid fa-gears").strip()
    if not name:
        flash("Service name is required.", "danger")
        return redirect(url_for("admin.services_list"))

    image_path = None
    try:
        image_path = save_upload(request.files.get("image"), prefix="service")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.services_list"))

    execute(
        "INSERT INTO services (name, description, icon, image, status) VALUES (%s,%s,%s,%s,'Active')",
        (name, description, icon, image_path),
    )
    flash("Service added successfully.", "success")
    return redirect(url_for("admin.services_list"))


@admin_bp.route("/services/edit/<int:item_id>", methods=["POST"])
@login_required
def services_edit(item_id):
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "").strip()

    image_path = None
    try:
        image_path = save_upload(request.files.get("image"), prefix="service")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.services_list"))

    if image_path:
        execute(
            "UPDATE services SET name=%s, description=%s, icon=%s, image=%s WHERE id=%s",
            (name, description, icon, image_path, item_id),
        )
    else:
        execute(
            "UPDATE services SET name=%s, description=%s, icon=%s WHERE id=%s",
            (name, description, icon, item_id),
        )
    flash("Service updated successfully.", "success")
    return redirect(url_for("admin.services_list"))


@admin_bp.route("/services/delete/<int:item_id>", methods=["POST"])
@login_required
def services_delete(item_id):
    execute("DELETE FROM services WHERE id=%s", (item_id,))
    flash("Service deleted.", "info")
    return redirect(url_for("admin.services_list"))


@admin_bp.route("/services/toggle/<int:item_id>", methods=["POST"])
@login_required
def services_toggle(item_id):
    row = query("SELECT status FROM services WHERE id=%s", (item_id,), fetchone=True)
    if row:
        new_status = "Inactive" if row["status"] == "Active" else "Active"
        execute("UPDATE services SET status=%s WHERE id=%s", (new_status, item_id))
    return redirect(url_for("admin.services_list"))


# ============================================================
# EQUIPMENT
# ============================================================

@admin_bp.route("/equipment")
@login_required
def equipment_list():
    rows = query("SELECT * FROM equipment ORDER BY created_at DESC")
    return render_template("admin/equipment.html", equipment=rows)


@admin_bp.route("/equipment/add", methods=["POST"])
@login_required
def equipment_add():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    specifications = request.form.get("specifications", "").strip()
    availability = request.form.get("availability", "Available")

    if not name or not category:
        flash("Equipment name and category are required.", "danger")
        return redirect(url_for("admin.equipment_list"))

    image_path = None
    try:
        image_path = save_upload(request.files.get("image"), prefix="equip")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.equipment_list"))

    execute(
        """INSERT INTO equipment (name, category, description, specifications, image, availability, status)
           VALUES (%s,%s,%s,%s,%s,%s,'Active')""",
        (name, category, description, specifications, image_path, availability),
    )
    flash("Equipment added successfully.", "success")
    return redirect(url_for("admin.equipment_list"))


@admin_bp.route("/equipment/edit/<int:item_id>", methods=["POST"])
@login_required
def equipment_edit(item_id):
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    specifications = request.form.get("specifications", "").strip()
    availability = request.form.get("availability", "Available")

    image_path = None
    try:
        image_path = save_upload(request.files.get("image"), prefix="equip")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.equipment_list"))

    if image_path:
        execute(
            """UPDATE equipment SET name=%s, category=%s, description=%s, specifications=%s,
               image=%s, availability=%s WHERE id=%s""",
            (name, category, description, specifications, image_path, availability, item_id),
        )
    else:
        execute(
            """UPDATE equipment SET name=%s, category=%s, description=%s, specifications=%s,
               availability=%s WHERE id=%s""",
            (name, category, description, specifications, availability, item_id),
        )
    flash("Equipment updated successfully.", "success")
    return redirect(url_for("admin.equipment_list"))


@admin_bp.route("/equipment/delete/<int:item_id>", methods=["POST"])
@login_required
def equipment_delete(item_id):
    execute("DELETE FROM equipment WHERE id=%s", (item_id,))
    flash("Equipment deleted.", "info")
    return redirect(url_for("admin.equipment_list"))


@admin_bp.route("/equipment/toggle/<int:item_id>", methods=["POST"])
@login_required
def equipment_toggle(item_id):
    row = query("SELECT status FROM equipment WHERE id=%s", (item_id,), fetchone=True)
    if row:
        new_status = "Inactive" if row["status"] == "Active" else "Active"
        execute("UPDATE equipment SET status=%s WHERE id=%s", (new_status, item_id))
    return redirect(url_for("admin.equipment_list"))


# ============================================================
# PROJECTS
# ============================================================

@admin_bp.route("/projects")
@login_required
def projects_list():
    rows = query("SELECT * FROM projects ORDER BY created_at DESC")
    return render_template("admin/projects.html", projects=rows)


@admin_bp.route("/projects/add", methods=["POST"])
@login_required
def projects_add():
    name = request.form.get("name", "").strip()
    location = request.form.get("location", "").strip()
    project_type = request.form.get("project_type", "").strip()
    description = request.form.get("description", "").strip()
    project_date = request.form.get("project_date") or None

    if not name:
        flash("Project name is required.", "danger")
        return redirect(url_for("admin.projects_list"))

    image_path = None
    try:
        image_path = save_upload(request.files.get("image"), prefix="project")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.projects_list"))

    execute(
        """INSERT INTO projects (name, location, project_type, description, project_date, image, status)
           VALUES (%s,%s,%s,%s,%s,%s,'Active')""",
        (name, location, project_type, description, project_date, image_path),
    )
    flash("Project added successfully.", "success")
    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/edit/<int:item_id>", methods=["POST"])
@login_required
def projects_edit(item_id):
    name = request.form.get("name", "").strip()
    location = request.form.get("location", "").strip()
    project_type = request.form.get("project_type", "").strip()
    description = request.form.get("description", "").strip()
    project_date = request.form.get("project_date") or None

    image_path = None
    try:
        image_path = save_upload(request.files.get("image"), prefix="project")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.projects_list"))

    if image_path:
        execute(
            """UPDATE projects SET name=%s, location=%s, project_type=%s, description=%s,
               project_date=%s, image=%s WHERE id=%s""",
            (name, location, project_type, description, project_date, image_path, item_id),
        )
    else:
        execute(
            """UPDATE projects SET name=%s, location=%s, project_type=%s, description=%s,
               project_date=%s WHERE id=%s""",
            (name, location, project_type, description, project_date, item_id),
        )
    flash("Project updated successfully.", "success")
    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/delete/<int:item_id>", methods=["POST"])
@login_required
def projects_delete(item_id):
    execute("DELETE FROM projects WHERE id=%s", (item_id,))
    flash("Project deleted.", "info")
    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/toggle/<int:item_id>", methods=["POST"])
@login_required
def projects_toggle(item_id):
    row = query("SELECT status FROM projects WHERE id=%s", (item_id,), fetchone=True)
    if row:
        new_status = "Inactive" if row["status"] == "Active" else "Active"
        execute("UPDATE projects SET status=%s WHERE id=%s", (new_status, item_id))
    return redirect(url_for("admin.projects_list"))


# ============================================================
# TESTIMONIALS
# ============================================================

@admin_bp.route("/testimonials")
@login_required
def testimonials_list():
    rows = query("SELECT * FROM testimonials ORDER BY created_at DESC")
    return render_template("admin/testimonials.html", testimonials=rows)


@admin_bp.route("/testimonials/add", methods=["POST"])
@login_required
def testimonials_add():
    customer_name = request.form.get("customer_name", "").strip()
    company = request.form.get("company", "").strip()
    testimonial = request.form.get("testimonial", "").strip()
    rating = request.form.get("rating", 5)

    if not customer_name or not testimonial:
        flash("Customer name and testimonial text are required.", "danger")
        return redirect(url_for("admin.testimonials_list"))

    photo_path = None
    try:
        photo_path = save_upload(request.files.get("photo"), prefix="testimonial")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.testimonials_list"))

    execute(
        """INSERT INTO testimonials (customer_name, company, testimonial, rating, photo, status)
           VALUES (%s,%s,%s,%s,%s,'Active')""",
        (customer_name, company, testimonial, rating, photo_path),
    )
    flash("Testimonial added successfully.", "success")
    return redirect(url_for("admin.testimonials_list"))


@admin_bp.route("/testimonials/edit/<int:item_id>", methods=["POST"])
@login_required
def testimonials_edit(item_id):
    customer_name = request.form.get("customer_name", "").strip()
    company = request.form.get("company", "").strip()
    testimonial = request.form.get("testimonial", "").strip()
    rating = request.form.get("rating", 5)

    photo_path = None
    try:
        photo_path = save_upload(request.files.get("photo"), prefix="testimonial")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.testimonials_list"))

    if photo_path:
        execute(
            "UPDATE testimonials SET customer_name=%s, company=%s, testimonial=%s, rating=%s, photo=%s WHERE id=%s",
            (customer_name, company, testimonial, rating, photo_path, item_id),
        )
    else:
        execute(
            "UPDATE testimonials SET customer_name=%s, company=%s, testimonial=%s, rating=%s WHERE id=%s",
            (customer_name, company, testimonial, rating, item_id),
        )
    flash("Testimonial updated successfully.", "success")
    return redirect(url_for("admin.testimonials_list"))


@admin_bp.route("/testimonials/delete/<int:item_id>", methods=["POST"])
@login_required
def testimonials_delete(item_id):
    execute("DELETE FROM testimonials WHERE id=%s", (item_id,))
    flash("Testimonial deleted.", "info")
    return redirect(url_for("admin.testimonials_list"))


@admin_bp.route("/testimonials/toggle/<int:item_id>", methods=["POST"])
@login_required
def testimonials_toggle(item_id):
    row = query("SELECT status FROM testimonials WHERE id=%s", (item_id,), fetchone=True)
    if row:
        new_status = "Inactive" if row["status"] == "Active" else "Active"
        execute("UPDATE testimonials SET status=%s WHERE id=%s", (new_status, item_id))
    return redirect(url_for("admin.testimonials_list"))


# ============================================================
# ENQUIRIES
# ============================================================

@admin_bp.route("/enquiries")
@login_required
def enquiries_list():
    status_filter = request.args.get("status", "").strip()
    search = request.args.get("q", "").strip()

    sql = "SELECT * FROM enquiries WHERE 1=1"
    params = []
    if status_filter:
        sql += " AND status=%s"
        params.append(status_filter)
    if search:
        sql += " AND (name LIKE %s OR phone LIKE %s OR email LIKE %s OR company LIKE %s)"
        like = f"%{search}%"
        params.extend([like, like, like, like])
    sql += " ORDER BY created_at DESC"

    rows = query(sql, params)
    return render_template(
        "admin/enquiries.html", enquiries=rows, status_filter=status_filter, search=search
    )


@admin_bp.route("/enquiries/view/<int:item_id>")
@login_required
def enquiries_view(item_id):
    enquiry = query("SELECT * FROM enquiries WHERE id=%s", (item_id,), fetchone=True)
    if not enquiry:
        flash("Enquiry not found.", "danger")
        return redirect(url_for("admin.enquiries_list"))
    return render_template("admin/enquiry_detail.html", enquiry=enquiry)


@admin_bp.route("/enquiries/status/<int:item_id>", methods=["POST"])
@login_required
def enquiries_status(item_id):
    new_status = request.form.get("status")
    valid = {"New", "Contacted", "In Progress", "Completed", "Cancelled"}
    if new_status in valid:
        execute("UPDATE enquiries SET status=%s WHERE id=%s", (new_status, item_id))
        flash("Enquiry status updated.", "success")
    return redirect(request.referrer or url_for("admin.enquiries_list"))


@admin_bp.route("/enquiries/delete/<int:item_id>", methods=["POST"])
@login_required
def enquiries_delete(item_id):
    execute("DELETE FROM enquiries WHERE id=%s", (item_id,))
    flash("Enquiry deleted.", "info")
    return redirect(url_for("admin.enquiries_list"))


# ============================================================
# ADMIN USER MANAGEMENT (Super Admin only)
# ============================================================

@admin_bp.route("/admins")
@super_admin_required
def admins_list():
    rows = query("SELECT id, name, email, role, status, created_at FROM admins ORDER BY created_at DESC")
    return render_template("admin/admins.html", admins=rows)


@admin_bp.route("/admins/add", methods=["POST"])
@super_admin_required
def admins_add():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    role = request.form.get("role", "Admin")

    if not name or not email or not password:
        flash("Name, email and password are all required.", "danger")
        return redirect(url_for("admin.admins_list"))
    if not is_valid_email(email):
        flash("Please enter a valid email address.", "danger")
        return redirect(url_for("admin.admins_list"))

    existing = query("SELECT id FROM admins WHERE email=%s", (email,), fetchone=True)
    if existing:
        flash("An admin with that email already exists.", "danger")
        return redirect(url_for("admin.admins_list"))

    password_hash = generate_password_hash(password)
    execute(
        "INSERT INTO admins (name, email, password_hash, role, status) VALUES (%s,%s,%s,%s,'Active')",
        (name, email, password_hash, role),
    )
    flash("Admin user created successfully.", "success")
    return redirect(url_for("admin.admins_list"))


@admin_bp.route("/admins/toggle/<int:item_id>", methods=["POST"])
@super_admin_required
def admins_toggle(item_id):
    if item_id == session.get("admin_id"):
        flash("You cannot deactivate your own account.", "danger")
        return redirect(url_for("admin.admins_list"))
    row = query("SELECT status FROM admins WHERE id=%s", (item_id,), fetchone=True)
    if row:
        new_status = "Inactive" if row["status"] == "Active" else "Active"
        execute("UPDATE admins SET status=%s WHERE id=%s", (new_status, item_id))
    return redirect(url_for("admin.admins_list"))


@admin_bp.route("/admins/delete/<int:item_id>", methods=["POST"])
@super_admin_required
def admins_delete(item_id):
    if item_id == session.get("admin_id"):
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin.admins_list"))
    execute("DELETE FROM admins WHERE id=%s", (item_id,))
    flash("Admin user deleted.", "info")
    return redirect(url_for("admin.admins_list"))


@admin_bp.route("/admins/change-password/<int:item_id>", methods=["POST"])
@super_admin_required
def admins_change_password(item_id):
    new_password = request.form.get("password", "")
    if len(new_password) < 6:
        flash("Password must be at least 6 characters.", "danger")
        return redirect(url_for("admin.admins_list"))
    execute(
        "UPDATE admins SET password_hash=%s WHERE id=%s",
        (generate_password_hash(new_password), item_id),
    )
    flash("Password updated successfully.", "success")
    return redirect(url_for("admin.admins_list"))


@admin_bp.route("/profile/change-password", methods=["POST"])
@login_required
def my_change_password():
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    admin = query("SELECT * FROM admins WHERE id=%s", (session["admin_id"],), fetchone=True)

    if not admin or not check_password_hash(admin["password_hash"], current_password):
        flash("Current password is incorrect.", "danger")
    elif len(new_password) < 6:
        flash("New password must be at least 6 characters.", "danger")
    else:
        execute(
            "UPDATE admins SET password_hash=%s WHERE id=%s",
            (generate_password_hash(new_password), session["admin_id"]),
        )
        flash("Password changed successfully.", "success")
    return redirect(url_for("admin.dashboard"))


# ============================================================
# WEBSITE SETTINGS
# ============================================================

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        fields = [
            "company_name", "phone", "whatsapp", "email", "address", "business_hours",
            "facebook_url", "instagram_url", "linkedin_url", "google_maps_url",
            "hero_heading", "hero_subheading", "hero_description", "about_content",
            "years_experience", "total_projects", "equipment_units", "customer_focus",
        ]
        for key in fields:
            value = request.form.get(key, "").strip()
            execute(
                """INSERT INTO website_settings (setting_key, setting_value) VALUES (%s,%s)
                   ON DUPLICATE KEY UPDATE setting_value=%s""",
                (key, value, value),
            )

        try:
            logo_path = save_upload(request.files.get("logo"), prefix="logo")
            if logo_path:
                execute(
                    """INSERT INTO website_settings (setting_key, setting_value) VALUES ('logo', %s)
                       ON DUPLICATE KEY UPDATE setting_value=%s""",
                    (logo_path, logo_path),
                )
        except ValueError as e:
            flash(str(e), "danger")

        flash("Website settings updated successfully.", "success")
        return redirect(url_for("admin.settings"))

    rows = query("SELECT setting_key, setting_value FROM website_settings")
    settings_map = {r["setting_key"]: r["setting_value"] for r in rows}
    return render_template("admin/settings.html", settings=settings_map)
