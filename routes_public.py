from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import query, execute
from utils import is_valid_email, is_valid_phone

public_bp = Blueprint("public", __name__)


def get_settings():
    rows = query("SELECT setting_key, setting_value FROM website_settings")
    return {r["setting_key"]: r["setting_value"] for r in rows}





@public_bp.route("/")
def index():
    services = query("SELECT * FROM services WHERE status='Active' ORDER BY created_at DESC LIMIT 6")
    equipment = query("SELECT * FROM equipment WHERE status='Active' ORDER BY created_at DESC LIMIT 6")
    projects = query("SELECT * FROM projects WHERE status='Active' ORDER BY project_date DESC LIMIT 6")
    testimonials = query("SELECT * FROM testimonials WHERE status='Active' ORDER BY created_at DESC LIMIT 6")
    return render_template(
        "index.html",
        services=services,
        equipment=equipment,
        projects=projects,
        testimonials=testimonials,
    )


@public_bp.route("/about")
def about():
    return render_template("about.html")


@public_bp.route("/services")
def services():
    services = query("SELECT * FROM services WHERE status='Active' ORDER BY name ASC")
    return render_template("services.html", services=services)


@public_bp.route("/equipment")
def equipment():
    category = request.args.get("category", "").strip()
    if category:
        rows = query(
            "SELECT * FROM equipment WHERE status='Active' AND category=%s ORDER BY name ASC",
            (category,),
        )
    else:
        rows = query("SELECT * FROM equipment WHERE status='Active' ORDER BY category ASC, name ASC")
    categories = query("SELECT DISTINCT category FROM equipment WHERE status='Active' ORDER BY category ASC")
    return render_template("equipment.html", equipment=rows, categories=categories, active_category=category)


@public_bp.route("/projects")
def projects():
    rows = query("SELECT * FROM projects WHERE status='Active' ORDER BY project_date DESC")
    return render_template("projects.html", projects=rows)


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    services = query("SELECT name FROM services WHERE status='Active' ORDER BY name ASC")
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        company = request.form.get("company", "").strip()
        service_required = request.form.get("service_required", "").strip()
        message = request.form.get("message", "").strip()

        errors = []
        if not name:
            errors.append("Full name is required.")
        if not phone or not is_valid_phone(phone):
            errors.append("A valid phone number is required.")
        if email and not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not message:
            errors.append("Message is required.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "contact.html", services=services, form_data=request.form
            )

        execute(
            """INSERT INTO enquiries (name, phone, email, company, service_required, message, status)
               VALUES (%s, %s, %s, %s, %s, %s, 'New')""",
            (name, phone, email, company, service_required, message),
        )
        flash("Thank you! Your enquiry has been submitted successfully.", "success")
        return redirect(url_for("public.contact"))

    return render_template("contact.html", services=services, form_data={})


@public_bp.route("/api/equipment/<int:equipment_id>")
def api_equipment_detail(equipment_id):
    row = query("SELECT * FROM equipment WHERE id=%s AND status='Active'", (equipment_id,), fetchone=True)
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row)


@public_bp.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@public_bp.app_errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403


@public_bp.app_errorhandler(500)
def server_error(e):
    return render_template("errors/500.html"), 500
