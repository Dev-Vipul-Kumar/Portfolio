import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import (
    ContactForm, FAQSubmitForm, CMSLoginForm,
    SiteProfileForm, SkillForm, ProjectForm,
    ExperienceForm, CertificationForm, TypedRoleForm, FAQItemForm,
)
from .models import (
    SiteProfile, Skill, Project, Experience,
    Certification, ContactMessage, FAQItem, TypedRole,
)

# ─── Helpers ─────────────────────────────────────────────────────────────────

CMS_SESSION_KEY = "cms_authenticated"
CMS_PASSWORD    = getattr(settings, "CMS_PASSWORD", "vipul@cms2025")


def _cms_required(view_fn):
    """Decorator: redirect to CMS login if not authenticated."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get(CMS_SESSION_KEY):
            return redirect("cms_login")
        return view_fn(request, *args, **kwargs)
    wrapper.__name__ = view_fn.__name__
    return wrapper


def _public_ctx():
    """Context shared by every public page."""
    profile = SiteProfile.get()
    return {
        "profile":  profile,
        "skills":   Skill.objects.all(),
        "projects": Project.objects.all(),
        "exp":      Experience.objects.all(),
        "certs":    Certification.objects.all(),
        "roles":    list(TypedRole.objects.values_list("label", flat=True)),
        "faqs":     FAQItem.objects.all(),
    }


# ─── Health check ─────────────────────────────────────────────────────────────

def health_check(request):
    return HttpResponse("OK", status=200)


# ─── Public views ─────────────────────────────────────────────────────────────

def homepage(request):
    return render(request, "Portfolio.html", _public_ctx())


def about(request):
    return render(request, "about.html", _public_ctx())


def Main(request):
    return render(request, "Main.html", _public_ctx())


def contact(request):
    ctx = _public_ctx()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()                   # actually save now
            profile = ctx["profile"]
            full_message = (
                f"New Contact Form Submission:\n\n"
                f"Name: {msg.name}\n"
                f"Email: {msg.email}\n"
                f"Phone: {msg.phone or 'Not provided'}\n"
                f"Preferred Contact: {msg.preferred_contact}\n"
                f"Best Time: {msg.best_time or 'Not specified'}\n\n"
                f"Message:\n{msg.message}"
            )
            try:
                send_mail(
                    subject=f"New message from {msg.name}",
                    message=full_message,
                    from_email=msg.email,
                    recipient_list=[profile.email],
                    fail_silently=False,
                )
            except Exception:
                pass
            messages.success(request, "Thank you for your message. I'll get back to you soon!")
            return redirect("contact")
    else:
        form = ContactForm()
    ctx["form"] = form
    return render(request, "contact.html", ctx)


def faq_view(request):
    ctx = _public_ctx()
    if request.method == "POST":
        form = FAQSubmitForm(request.POST)
        if form.is_valid():
            profile = ctx["profile"]
            try:
                send_mail(
                    subject=f"FAQ Question from {form.cleaned_data['name']}",
                    message=(
                        f"Name: {form.cleaned_data['name']}\n"
                        f"Email: {form.cleaned_data['email']}\n\n"
                        f"Question:\n{form.cleaned_data['question']}"
                    ),
                    from_email=form.cleaned_data["email"],
                    recipient_list=[profile.email],
                    fail_silently=False,
                )
            except Exception:
                pass
            messages.success(request, "Your question has been sent successfully!")
            return redirect("faq")
    else:
        form = FAQSubmitForm()
    ctx["form"] = form
    return render(request, "faq.html", ctx)


# ─── CMS: login / logout ──────────────────────────────────────────────────────

def cms_login(request):
    if request.session.get(CMS_SESSION_KEY):
        return redirect("cms_dashboard")
    error = None
    if request.method == "POST":
        form = CMSLoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == CMS_PASSWORD:
                request.session[CMS_SESSION_KEY] = True
                request.session.set_expiry(60 * 60 * 8)   # 8-hour session
                return redirect("cms_dashboard")
            error = "Incorrect password."
    else:
        form = CMSLoginForm()
    return render(request, "cms/login.html", {"form": form, "error": error})


def cms_logout(request):
    request.session.flush()
    return redirect("cms_login")


# ─── CMS: dashboard ───────────────────────────────────────────────────────────

@_cms_required
def cms_dashboard(request):
    projects  = list(Project.objects.all())
    exp_list  = list(Experience.objects.all())
    faqs_list = list(FAQItem.objects.all())

    projects_json = json.dumps([{
        "pk": p.pk, "name": p.name, "icon": p.icon, "status": p.status,
        "order": p.order, "description": p.description,
        "live_url": p.live_url, "github_url": p.github_url, "tags": p.tags,
    } for p in projects])

    exp_json = json.dumps([{
        "pk": e.pk, "role": e.role, "company": e.company,
        "date_range": e.date_range, "bullets": e.bullets,
        "is_fulltime": e.is_fulltime, "order": e.order,
    } for e in exp_list])

    faqs_json = json.dumps([{
        "pk": f.pk, "question": f.question,
        "answer": f.answer, "order": f.order,
    } for f in faqs_list])

    profile = SiteProfile.get()
    ctx = {
        "profile":        profile,
        "profile_form":   SiteProfileForm(instance=profile),   # always pre-filled
        "skills":         Skill.objects.all(),
        "projects":       projects,
        "exp":            exp_list,
        "certs":          Certification.objects.all(),
        "roles":          TypedRole.objects.all(),
        "faqs":           faqs_list,
        # Use "messages_list" — never "messages" (collides with Django's framework)
        "messages_list":  ContactMessage.objects.all(),
        "unread":         ContactMessage.objects.filter(is_read=False).count(),
        "section":        request.GET.get("section", "profile"),
        "projects_json":  projects_json,
        "exp_json":       exp_json,
        "faqs_json":      faqs_json,
    }
    return render(request, "cms/dashboard.html", ctx)


# ─── CMS: generic CRUD helpers ────────────────────────────────────────────────

def _cms_dashboard_ctx():
    profile   = SiteProfile.get()
    projects  = list(Project.objects.all())
    exp_list  = list(Experience.objects.all())
    faqs_list = list(FAQItem.objects.all())
    return {
        "profile":        profile,
        "profile_form":   SiteProfileForm(instance=profile),   # always pre-filled
        "skills":         Skill.objects.all(),
        "projects":       projects,
        "exp":            exp_list,
        "certs":          Certification.objects.all(),
        "roles":          TypedRole.objects.all(),
        "faqs":           faqs_list,
        "messages_list":  ContactMessage.objects.all(),
        "unread":         ContactMessage.objects.filter(is_read=False).count(),
        "projects_json":  json.dumps([{
            "pk": p.pk, "name": p.name, "icon": p.icon, "status": p.status,
            "order": p.order, "description": p.description,
            "live_url": p.live_url, "github_url": p.github_url, "tags": p.tags,
        } for p in projects]),
        "exp_json": json.dumps([{
            "pk": e.pk, "role": e.role, "company": e.company,
            "date_range": e.date_range, "bullets": e.bullets,
            "is_fulltime": e.is_fulltime, "order": e.order,
        } for e in exp_list]),
        "faqs_json": json.dumps([{
            "pk": f.pk, "question": f.question,
            "answer": f.answer, "order": f.order,
        } for f in faqs_list]),
    }


def _crud_view(request, Model, Form, section, redirect_section=None):
    """Generic add / edit / delete for any CMS model."""
    redir = redirect_section or section
    action = request.POST.get("_action", "")

    if request.method == "POST":
        if action == "delete":
            pk = request.POST.get("pk")
            Model.objects.filter(pk=pk).delete()
            messages.success(request, "Deleted.")
            return redirect(f"/vipul-secret-cms/?section={redir}")

        pk   = request.POST.get("pk") or None   # treat empty string as None
        inst = Model.objects.filter(pk=pk).first() if pk else None
        form = Form(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            messages.success(request, "✓ Saved successfully.")
            return redirect(f"/vipul-secret-cms/?section={redir}")

        # Form invalid — surface errors as messages and re-render
        for field, errs in form.errors.items():
            for err in errs:
                messages.error(request, f"'{field}': {err}")
        ctx = _cms_dashboard_ctx()
        ctx["section"] = section
        return render(request, "cms/dashboard.html", ctx)

    return redirect(f"/vipul-secret-cms/?section={redir}")


@_cms_required
def cms_skills(request):
    return _crud_view(request, Skill, SkillForm, "skills")

@_cms_required
def cms_projects(request):
    return _crud_view(request, Project, ProjectForm, "projects")

@_cms_required
def cms_experience(request):
    return _crud_view(request, Experience, ExperienceForm, "experience")

@_cms_required
def cms_certs(request):
    return _crud_view(request, Certification, CertificationForm, "certs")

@_cms_required
def cms_roles(request):
    return _crud_view(request, TypedRole, TypedRoleForm, "roles")

@_cms_required
def cms_faqs(request):
    return _crud_view(request, FAQItem, FAQItemForm, "faqs")

@_cms_required
def cms_profile_save(request):
    profile = SiteProfile.get()
    if request.method == "POST":
        form = SiteProfileForm(request.POST, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            # Keep full_name in sync automatically
            obj.full_name = f"{obj.first_name} {obj.last_name}".strip()
            obj.save()
            messages.success(request, "✓ Profile updated successfully.")
            return redirect("/vipul-secret-cms/?section=profile")
        # Form invalid — surface every validation error and re-render the
        # dashboard. Bind form.instance to the (unsaved) posted data so the
        # fields retain what the user typed instead of reverting to DB values.
        for field, errs in form.errors.items():
            for err in errs:
                messages.error(request, f"'{field}': {err}")
        # Overlay posted clean values onto profile so template inputs keep
        # the user's typed text even though the save was rejected.
        for field, value in form.cleaned_data.items():
            setattr(profile, field, value)
        ctx = _cms_dashboard_ctx()
        ctx["section"] = "profile"
        ctx["profile"] = profile          # unsaved overlay for the template
        ctx["profile_form"] = form        # bound form with error highlighting
        return render(request, "cms/dashboard.html", ctx)
    return redirect("/vipul-secret-cms/?section=profile")


# ─── CMS: mark message read ───────────────────────────────────────────────────

@_cms_required
@require_POST
def cms_mark_read(request):
    pk = request.POST.get("pk")
    ContactMessage.objects.filter(pk=pk).update(is_read=True)
    return redirect("/vipul-secret-cms/?section=messages")


@_cms_required
@require_POST
def cms_delete_message(request):
    pk = request.POST.get("pk")
    ContactMessage.objects.filter(pk=pk).delete()
    messages.success(request, "Message deleted.")
    return redirect("/vipul-secret-cms/?section=messages")


# ─── CMS: resume upload ───────────────────────────────────────────────────────

@_cms_required
def cms_resume(request):
    if request.method == "POST":
        uploaded = request.FILES.get("resume_pdf")
        if not uploaded:
            messages.error(request, "No file selected.")
            return redirect("/vipul-secret-cms/?section=resume")
        if not uploaded.name.lower().endswith(".pdf"):
            messages.error(request, "Only PDF files are allowed.")
            return redirect("/vipul-secret-cms/?section=resume")
        if uploaded.size > 10 * 1024 * 1024:   # 10 MB hard limit
            messages.error(request, "File too large — maximum size is 10 MB.")
            return redirect("/vipul-secret-cms/?section=resume")

        dest = settings.BASE_DIR / "static" / "Resume.pdf"
        with open(dest, "wb") as fh:
            for chunk in uploaded.chunks():
                fh.write(chunk)

        messages.success(request, "Resume updated successfully.")
    return redirect("/vipul-secret-cms/?section=resume")
