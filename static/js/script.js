document.addEventListener('DOMContentLoaded', function () {

  // ===== Sticky navbar shrink on scroll =====
  const navbar = document.querySelector('.navbar-aman');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 40) {
        navbar.style.padding = '8px 0';
        navbar.style.boxShadow = '0 6px 20px rgba(0,0,0,0.25)';
      } else {
        navbar.style.padding = '14px 0';
        navbar.style.boxShadow = 'none';
      }
    });
  }

  // ===== Highlight active nav link =====
  const path = window.location.pathname;
  document.querySelectorAll('.navbar-aman .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === path || (href !== '/' && path.startsWith(href))) {
      link.classList.add('active');
    }
  });

  // ===== Smooth scroll for in-page anchors =====
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  // ===== Animated counters (statistics section) =====
  const counters = document.querySelectorAll('.stat-number[data-count]');
  if (counters.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(c => observer.observe(c));
  }

  function animateCounter(el) {
    const raw = el.getAttribute('data-count') || '0';
    const numMatch = raw.match(/[\d.]+/);
    const target = numMatch ? parseFloat(numMatch[0]) : 0;
    const suffix = raw.replace(/[\d.]+/, '');
    let current = 0;
    const duration = 1400;
    const stepTime = 16;
    const steps = duration / stepTime;
    const increment = target / steps;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = (Number.isInteger(target) ? Math.floor(current) : current.toFixed(1)) + suffix;
    }, stepTime);
  }

  // ===== Equipment category filter (client-side helper, form also submits) =====
  const categoryButtons = document.querySelectorAll('.category-filter-btn');
  categoryButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      categoryButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  // ===== Contact form validation (client side, backend also validates) =====
  const enquiryForm = document.getElementById('enquiryForm');
  if (enquiryForm) {
    enquiryForm.addEventListener('submit', function (e) {
      let valid = true;
      const name = enquiryForm.querySelector('[name="name"]');
      const phone = enquiryForm.querySelector('[name="phone"]');
      const message = enquiryForm.querySelector('[name="message"]');

      [name, phone, message].forEach(field => {
        if (field && !field.value.trim()) {
          field.classList.add('is-invalid');
          valid = false;
        } else if (field) {
          field.classList.remove('is-invalid');
        }
      });

      if (!valid) e.preventDefault();
    });
  }

  // ===== Bootstrap form validation styling (admin forms) =====
  document.querySelectorAll('.needs-validation').forEach(form => {
    form.addEventListener('submit', function (e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });

  // ===== Auto-dismiss alerts =====
  document.querySelectorAll('.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      alert.classList.remove('show');
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // ===== Image preview on upload (admin) =====
  document.querySelectorAll('.image-input-preview').forEach(input => {
    input.addEventListener('change', function () {
      const previewId = this.getAttribute('data-preview');
      const preview = document.getElementById(previewId);
      if (preview && this.files && this.files[0]) {
        preview.src = URL.createObjectURL(this.files[0]);
        preview.style.display = 'block';
      }
    });
  });

  // ===== Sidebar toggle (mobile admin) =====
  const sidebarToggle = document.getElementById('sidebarToggle');
  const adminSidebar = document.querySelector('.admin-sidebar');
  if (sidebarToggle && adminSidebar) {
    sidebarToggle.addEventListener('click', () => {
      adminSidebar.classList.toggle('show-mobile');
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const navLinks = document.querySelectorAll('#navMain .nav-link, #navMain .btn-quote');

  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      const navMain = document.getElementById('navMain');

      if (navMain && navMain.classList.contains('show')) {
        const toggler = document.querySelector('.navbar-toggler');

        if (toggler) {
          toggler.click();
        }
      }
    });
  });
});
