-- AMAN ENTERPRISE - Database Schema
CREATE DATABASE IF NOT EXISTS aman_enterprise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aman_enterprise;

-- ============ ADMINS ============
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Super Admin','Admin') NOT NULL DEFAULT 'Admin',
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- ============ SERVICES ============
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    icon VARCHAR(100) DEFAULT 'fa-solid fa-gears',
    image VARCHAR(255),
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- ============ EQUIPMENT ============
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    specifications TEXT,
    image VARCHAR(255),
    availability ENUM('Available','Booked','Under Maintenance') NOT NULL DEFAULT 'Available',
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- ============ PROJECTS ============
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(150),
    project_type VARCHAR(100),
    description TEXT,
    project_date DATE,
    image VARCHAR(255),
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- ============ TESTIMONIALS ============
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    company VARCHAR(150),
    testimonial TEXT NOT NULL,
    rating TINYINT DEFAULT 5,
    photo VARCHAR(255),
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- ============ ENQUIRIES ============
CREATE TABLE IF NOT EXISTS enquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150),
    company VARCHAR(150),
    service_required VARCHAR(150),
    message TEXT,
    status ENUM('New','Contacted','In Progress','Completed','Cancelled') NOT NULL DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB;

-- ============ WEBSITE SETTINGS ============
CREATE TABLE IF NOT EXISTS website_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============ DEFAULT SETTINGS ============
INSERT INTO website_settings (setting_key, setting_value) VALUES
('company_name', 'AMAN ENTERPRISE'),
('logo', ''),
('phone', '+91 98765 43210'),
('whatsapp', '919876543210'),
('email', 'info@amanenterprise.in'),
('address', 'Plot No. 45, Industrial Area, Phase II, New Delhi, India'),
('business_hours', 'Mon - Sat: 9:00 AM - 7:00 PM'),
('facebook_url', 'https://facebook.com'),
('instagram_url', 'https://instagram.com'),
('linkedin_url', 'https://linkedin.com'),
('google_maps_url', 'https://maps.google.com'),
('hero_heading', 'AMAN ENTERPRISE'),
('hero_subheading', 'Reliable Crane & Heavy Machinery Solutions'),
('hero_description', 'Providing dependable crane, heavy machinery and industrial equipment solutions with a strong focus on safety, reliability and professional service.'),
('about_content', 'AMAN ENTERPRISE provides crane and heavy machinery solutions for construction, industrial and infrastructure requirements across the region. With well-maintained equipment, an experienced team, and a strong focus on safety and timely delivery, we have become a trusted partner for contractors and industries alike.'),
('years_experience', '10+'),
('total_projects', '100+'),
('equipment_units', '50+'),
('customer_focus', '100%')
ON DUPLICATE KEY UPDATE setting_key = setting_key;

-- ============ SAMPLE ADMIN ============
-- Default login: admin@amanenterprise.in / Admin@123
-- (password_hash generated with werkzeug.security.generate_password_hash)
INSERT INTO admins (name, email, password_hash, role, status) VALUES
('Aman Sharma', 'admin@amanenterprise.in', 'scrypt:32768:8:1$8110c0Zdn1pbxEBc$95a390ffa0fc5c3c8c17f9108adf627f1cbe67e2d594cf01674b213877f381ae31d6fac13e2749d8441ad612307fa685e7d1e9add9101c14433a9081f79eb9d7', 'Super Admin', 'Active')
ON DUPLICATE KEY UPDATE email = email;

-- ============ SAMPLE SERVICES ============
INSERT INTO services (name, description, icon, image, status) VALUES
('Crane Services', 'Professional crane solutions for lifting and material handling requirements across construction and industrial sites.', 'fa-solid fa-truck-crane', '/static/uploads/service-crane.jpg', 'Active'),
('Heavy Machinery Rental', 'Reliable heavy equipment rental for construction and industrial projects of every scale.', 'fa-solid fa-truck-monster', '/static/uploads/service-rental.jpg', 'Active'),
('Material Handling', 'Safe and efficient material handling solutions for factories, warehouses and job sites.', 'fa-solid fa-boxes-stacked', '/static/uploads/service-material.jpg', 'Active'),
('Construction Equipment', 'A wide range of construction equipment solutions for infrastructure and building projects.', 'fa-solid fa-helmet-safety', '/static/uploads/service-construction.jpg', 'Active'),
('Industrial Equipment', 'Dependable machinery support tailored to industrial and manufacturing requirements.', 'fa-solid fa-industry', '/static/uploads/service-industrial.jpg', 'Active'),
('Equipment Transportation', 'Safe transportation and movement of heavy machinery with specialized trailers.', 'fa-solid fa-truck-front', '/static/uploads/service-transport.jpg', 'Active');

-- ============ SAMPLE EQUIPMENT ============
INSERT INTO equipment (name, category, description, specifications, image, availability, status) VALUES
('50-Ton Hydraulic Crane', 'Hydraulic Cranes', 'High-capacity hydraulic crane suited for heavy lifting on construction and industrial sites.', 'Capacity: 50 Tons | Model: HC-50X | Boom Length: 42m', '/static/uploads/eq-hydraulic-crane.jpg', 'Available', 'Active'),
('Mobile Crane 25T', 'Mobile Cranes', 'Versatile mobile crane for quick deployment across job sites.', 'Capacity: 25 Tons | Model: MC-25 | Max Height: 35m', '/static/uploads/eq-mobile-crane.jpg', 'Available', 'Active'),
('Tower Crane TC-80', 'Tower Cranes', 'Tower crane suited for high-rise construction projects.', 'Capacity: 8 Tons | Model: TC-80 | Height: 60m', '/static/uploads/eq-tower-crane.jpg', 'Booked', 'Active'),
('Forklift 3T', 'Forklifts', 'Reliable forklift for warehouse and site material handling.', 'Capacity: 3 Tons | Model: FL-3000 | Lift Height: 4.5m', '/static/uploads/eq-forklift.jpg', 'Available', 'Active'),
('Hydraulic Excavator', 'Excavators', 'Powerful excavator for digging, grading and demolition work.', 'Bucket Capacity: 1.2 m3 | Model: EX-200 | Operating Weight: 20T', '/static/uploads/eq-excavator.jpg', 'Available', 'Active'),
('Wheel Loader WL-5', 'Loaders', 'Heavy-duty wheel loader for construction and material movement.', 'Bucket Capacity: 3 m3 | Model: WL-5 | Operating Weight: 15T', '/static/uploads/eq-loader.jpg', 'Available', 'Active'),
('Heavy Transport Trailer', 'Heavy Transport Equipment', 'Low-bed trailer for safe transportation of heavy machinery.', 'Capacity: 60 Tons | Axles: 6 | Length: 14m', '/static/uploads/eq-trailer.jpg', 'Available', 'Active');

-- ============ SAMPLE PROJECTS ============
INSERT INTO projects (name, location, project_type, description, project_date, image, status) VALUES
('Metro Rail Viaduct Lifting', 'Delhi NCR', 'Infrastructure', 'Heavy lifting support for precast segment placement on the metro rail corridor.', '2025-11-10', '/static/uploads/proj-metro.jpg', 'Active'),
('Industrial Warehouse Setup', 'Gurugram, Haryana', 'Industrial', 'Material handling and machinery installation for a new industrial warehouse.', '2025-08-22', '/static/uploads/proj-warehouse.jpg', 'Active'),
('Residential Tower Construction', 'Noida, UP', 'Construction', 'Tower crane deployment for a 25-storey residential construction project.', '2025-05-15', '/static/uploads/proj-tower.jpg', 'Active'),
('Bridge Girder Placement', 'Faridabad, Haryana', 'Heavy Lifting', 'Precision heavy lifting for girder placement on a highway bridge project.', '2025-02-03', '/static/uploads/proj-bridge.jpg', 'Active'),
('Factory Equipment Relocation', 'Manesar, Haryana', 'Material Handling', 'Complete relocation and installation of heavy factory machinery.', '2024-12-18', '/static/uploads/proj-factory.jpg', 'Active');

-- ============ SAMPLE TESTIMONIALS ============
INSERT INTO testimonials (customer_name, company, testimonial, rating, photo, status) VALUES
('Rajesh Kumar', 'Kumar Constructions Pvt. Ltd.', 'AMAN ENTERPRISE provided excellent crane services for our high-rise project. Professional team and well-maintained equipment.', 5, '', 'Active'),
('Sunita Verma', 'Verma Infra Projects', 'Timely delivery and safe operations. We have been working with them for over 3 years now.', 5, '', 'Active'),
('Amit Singh', 'Singh Industrial Solutions', 'Reliable heavy machinery rental with great support staff. Highly recommended for industrial projects.', 4, '', 'Active');
