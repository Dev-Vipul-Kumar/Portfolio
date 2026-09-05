"""
python manage.py seed_cms

Populates the database with initial portfolio data ONLY if the table is empty.
Safe to re-run - if data already exists it is left completely untouched so that
any changes made through the CMS are preserved across server restarts and
re-deploys.

To force a full reset (wipes all CMS edits) run:
    python manage.py seed_cms --force
"""
from django.core.management.base import BaseCommand
from PF_App.models import (
    SiteProfile, TypedRole, Skill,
    Project, Experience, Certification, FAQItem
)


class Command(BaseCommand):
    help = "Seed CMS with initial portfolio data (skips if data already exists)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing data with the defaults (use with caution).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        self._profile(force)
        self._roles(force)
        self._skills(force)
        self._projects(force)
        self._experience(force)
        self._certs(force)
        self._faqs(force)
        self.stdout.write(self.style.SUCCESS("✓ CMS seed complete."))

    # ── Profile ──────────────────────────────────────────────────────────────
    def _profile(self, force):
        exists = SiteProfile.objects.filter(pk=1).exists()
        if exists and not force:
            self.stdout.write("  - SiteProfile: already exists, skipping.")
            return

        p, _ = SiteProfile.objects.get_or_create(pk=1)
        p.full_name         = "Vipul Kumar"
        p.first_name        = "Vipul"
        p.last_name         = "Kumar"
        p.tagline           = "BCA student, Django developer, and lifelong builder."
        p.hero_description  = (
            "I build <strong>clean, fast, and scalable</strong> web applications using "
            "Python, Django, and modern JavaScript. Currently a BCA student at BCIT Delhi "
            "- with real production systems already shipped."
        )
        p.about_bio_1 = (
            "I'm <strong>Vipul Kumar</strong>, a software developer based in Delhi. "
            "I specialise in full-stack web applications - Django and Python on the back end, "
            "modern JavaScript on the front."
        )
        p.about_bio_2 = (
            "During my internship at <strong>Indian Aviation Academy</strong> (Jan-May 2025) "
            "I designed and shipped three production tools used daily by academy staff."
        )
        p.about_bio_3 = (
            "Currently pursuing a BCA at BCIT (2022-2025) and exploring the MERN stack "
            "and system design in my spare time."
        )
        p.location          = "Delhi, India"
        p.education         = "BCA · BCIT 2022-25"
        p.email             = "vipulsam1234@gmail.com"
        p.github_url        = "https://github.com/Vipul-Kumar-Dev"
        p.github_handle     = "Vipul-Kumar-Dev"
        p.linkedin_url      = "https://www.linkedin.com/in/vipul-kumar-dev/"
        p.linkedin_handle   = "vipul-kumar-dev"
        p.languages         = "English, Hindi"
        p.resume_note       = "Get the full picture - all my experience, skills, and projects in one clean PDF."
        p.footer_copy       = "© 2025 Vipul Kumar · Built with Django"
        p.stat_projects     = "3+"
        p.stat_internships  = "2"
        p.stat_technologies = "8+"
        p.stat_experience   = "1.5y"
        p.is_available      = True
        p.save()
        self.stdout.write("  ✓ SiteProfile")

    # ── Typed Roles ───────────────────────────────────────────────────────────
    def _roles(self, force):
        if TypedRole.objects.exists() and not force:
            self.stdout.write("  - TypedRoles: already exist, skipping.")
            return

        TypedRole.objects.all().delete()
        data = [
            ("Software Developer",    0),
            ("Django Developer",      1),
            ("Full-Stack Developer",  2),
            ("Problem Solver",        3),
        ]
        for label, order in data:
            TypedRole.objects.create(label=label, order=order)
        self.stdout.write("  ✓ TypedRoles")

    # ── Skills ────────────────────────────────────────────────────────────────
    def _skills(self, force):
        if Skill.objects.exists() and not force:
            self.stdout.write("  - Skills: already exist, skipping.")
            return

        Skill.objects.all().delete()
        data = [
            ("HTML / CSS",     92, 0),
            ("Python",         90, 1),
            ("Django",         88, 2),
            ("Git / GitHub",   85, 3),
            ("MySQL / SQLite", 82, 4),
            ("JavaScript",     80, 5),
            ("MERN Stack",     75, 6),
            ("C / C++",        70, 7),
        ]
        for name, pct, order in data:
            Skill.objects.create(name=name, percentage=pct, order=order)
        self.stdout.write("  ✓ Skills")

    # ── Projects ──────────────────────────────────────────────────────────────
    def _projects(self, force):
        if Project.objects.exists() and not force:
            self.stdout.write("  - Projects: already exist, skipping.")
            return

        Project.objects.all().delete()
        data = [
            {
                "name": "Training Feedback System",
                "description": "Post-training feedback platform for Indian Aviation Academy - role-based login, event-linked analytics, and a real-time admin dashboard.",
                "status": "live",
                "icon": "📋",
                "live_url": "https://trainingfeedbacksystem.onrender.com/",
                "github_url": "https://github.com/Vipul-Kumar-Dev/IAA-Internship.git",
                "tags": "Django,Python,SQLite3,JavaScript",
                "order": 0,
            },
            {
                "name": "IAA CRM - Contract Manager",
                "description": "Full CRM system for IAA featuring multi-role access, contract lifecycle management, renewal reminders, and digital signature support.",
                "status": "wip",
                "icon": "🤝",
                "live_url": "",
                "github_url": "",
                "tags": "Django,Python,SQLite3,JavaScript",
                "order": 1,
            },
            {
                "name": "Invoice Generator",
                "description": "Dynamic PDF invoice generation for training billing - itemised entry, automated tax calculations, and a complete invoice history tracker.",
                "status": "wip",
                "icon": "🧾",
                "live_url": "",
                "github_url": "",
                "tags": "Django,Python,SQLite3,JavaScript",
                "order": 2,
            },
        ]
        for d in data:
            Project.objects.create(**d)
        self.stdout.write("  ✓ Projects")

    # ── Experience ────────────────────────────────────────────────────────────
    def _experience(self, force):
        if Experience.objects.exists() and not force:
            self.stdout.write("  - Experience: already exists, skipping.")
            return

        Experience.objects.all().delete()
        data = [
            {
                "role": "Software Developer Intern",
                "company": "Indian Aviation Academy",
                "date_range": "January 2025 - May 2025 · Delhi, India",
                "is_fulltime": True,
                "bullets": (
                    "Built the Training Feedback System end-to-end with role-based access and real-time analytics.\n"
                    "Designed IAA CRM with digital signature integration and automated contract renewal alerts.\n"
                    "Created the Invoice Generator supporting PDF export, GST automation, and billing history."
                ),
                "order": 0,
            },
            {
                "role": "Web Developer Intern",
                "company": "TheBlackPearls",
                "date_range": "May 2024 - June 2024 · Remote",
                "is_fulltime": False,
                "bullets": (
                    "Developed responsive web interfaces using HTML, CSS, and JavaScript.\n"
                    "Collaborated on front-end features and contributed to UI improvements.\n"
                    "Gained hands-on experience with modern development workflows and version control."
                ),
                "order": 1,
            },
        ]
        for d in data:
            Experience.objects.create(**d)
        self.stdout.write("  ✓ Experience")

    # ── Certifications ────────────────────────────────────────────────────────
    def _certs(self, force):
        if Certification.objects.exists() and not force:
            self.stdout.write("  - Certifications: already exist, skipping.")
            return

        Certification.objects.all().delete()
        data = [
            ("C Language Programming",                     "Naresh IT", "💻", 0),
            ("Java Programming",                           "Udemy",     "☕", 1),
            ("Python & Django Full-Stack Web Development", "Udemy",     "🐍", 2),
            ("React, Node, Express & MongoDB - MERN",      "Udemy",     "⚛️", 3),
        ]
        for name, issuer, icon, order in data:
            Certification.objects.create(name=name, issuer=issuer, icon=icon, order=order)
        self.stdout.write("  ✓ Certifications")

    # ── FAQ Items ─────────────────────────────────────────────────────────────
    def _faqs(self, force):
        if FAQItem.objects.exists() and not force:
            self.stdout.write("  - FAQItems: already exist, skipping.")
            return

        FAQItem.objects.all().delete()
        data = [
            ("What technologies do you work with?",
             "My primary stack is Python and Django for back-end development, with HTML, CSS, and JavaScript on the front end. I also work with the MERN stack (MongoDB, Express, React, Node.js), SQL databases, and Git for version control.",
             0),
            ("Are you available for freelance work?",
             "Yes - I'm currently open to freelance projects, especially Django web applications and full-stack builds. Feel free to reach out via the contact form with project details and a rough timeline.",
             1),
            ("What kind of projects do you take on?",
             "I'm most experienced with web applications: dashboards, CRM systems, data management tools, and APIs. I particularly enjoy projects that solve real operational problems for organisations.",
             2),
            ("How quickly do you respond to messages?",
             "I typically respond within 24 hours on weekdays. For urgent enquiries, email is the fastest route - vipulsam1234@gmail.com.",
             3),
            ("Are you open to full-time roles?",
             "Yes, I'm actively looking for graduate/junior software developer roles. I'm graduating with a BCA in 2025 and looking for positions where I can keep building meaningful products.",
             4),
            ("Can I see your resume?",
             "Absolutely - you can download it directly from this site. The link is in the navigation as well as on the portfolio page.",
             5),
        ]
        for q, a, order in data:
            FAQItem.objects.create(question=q, answer=a, order=order)
        self.stdout.write("  ✓ FAQ Items")
