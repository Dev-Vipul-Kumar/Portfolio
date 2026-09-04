from django.contrib import admin
from django.urls import path
from PF_App import views as v

urlpatterns = [
    # Django built-in admin (keep available)
    path("admin/", admin.site.urls),

    # ── Public pages ──────────────────────────────────────────
    path("",        v.homepage,   name="home"),
    path("about/",  v.about,      name="about"),
    path("Main/",   v.Main,       name="Main"),
    path("contact/",v.contact,    name="contact"),
    path("FAQ/",    v.faq_view,   name="faq"),
    path("healthz/",v.health_check),

    # ── Secret CMS ────────────────────────────────────────────
    # URL is intentionally obscure — not linked anywhere public
    path("vipul-secret-cms/",          v.cms_dashboard,    name="cms_dashboard"),
    path("vipul-secret-cms/login/",    v.cms_login,        name="cms_login"),
    path("vipul-secret-cms/logout/",   v.cms_logout,       name="cms_logout"),

    # CMS save endpoints (POST only, redirect back to dashboard)
    path("vipul-secret-cms/profile/",    v.cms_profile_save, name="cms_profile"),
    path("vipul-secret-cms/skills/",     v.cms_skills,       name="cms_skills"),
    path("vipul-secret-cms/projects/",   v.cms_projects,     name="cms_projects"),
    path("vipul-secret-cms/experience/", v.cms_experience,   name="cms_experience"),
    path("vipul-secret-cms/certs/",      v.cms_certs,        name="cms_certs"),
    path("vipul-secret-cms/roles/",      v.cms_roles,        name="cms_roles"),
    path("vipul-secret-cms/faqs/",       v.cms_faqs,         name="cms_faqs"),
    path("vipul-secret-cms/mark-read/",  v.cms_mark_read,        name="cms_mark_read"),
    path("vipul-secret-cms/delete-msg/", v.cms_delete_message,   name="cms_delete_message"),
    path("vipul-secret-cms/resume/",     v.cms_resume,           name="cms_resume"),
]
