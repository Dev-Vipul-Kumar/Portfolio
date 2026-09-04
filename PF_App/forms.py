from django import forms
from .models import (
    ContactMessage, FAQItem, SiteProfile,
    Skill, Project, Experience, Certification, TypedRole
)

# ─── Public forms ────────────────────────────────────────────────────────────

class ContactForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'Your phone number (optional)'})
    )
    preferred_contact = forms.ChoiceField(
        choices=[('', 'Select preferred contact method'), ('email', 'Email'), ('phone', 'Phone')],
        widget=forms.Select(attrs={'class': 'f-input f-select', 'id': 'preferred-contact'})
    )
    best_time = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'e.g. Weekday mornings (optional)'})
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'preferred_contact', 'best_time', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'Your full name'}),
            'email':   forms.EmailInput(attrs={'class': 'f-input', 'placeholder': 'your@email.com'}),
            'message': forms.Textarea(attrs={'class': 'f-textarea', 'placeholder': 'Tell me about your project or question…', 'rows': 5}),
        }


class FAQSubmitForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'Your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'f-input', 'placeholder': 'your@email.com'})
    )
    question = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'f-textarea', 'placeholder': 'What would you like to know?', 'rows': 5})
    )


# ─── CMS Admin forms ─────────────────────────────────────────────────────────

class CMSLoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'f-input', 'placeholder': 'Enter CMS password', 'autofocus': True})
    )


class SiteProfileForm(forms.ModelForm):
    class Meta:
        model = SiteProfile
        # full_name is auto-derived in the view from first_name + last_name
        exclude = ['id', 'full_name']
        widgets = {
            'first_name':       forms.TextInput(attrs={'class': 'f-input'}),
            'last_name':        forms.TextInput(attrs={'class': 'f-input'}),
            'tagline':          forms.TextInput(attrs={'class': 'f-input'}),
            'hero_description': forms.Textarea(attrs={'class': 'f-textarea', 'rows': 3}),
            'about_bio_1':      forms.Textarea(attrs={'class': 'f-textarea', 'rows': 3}),
            'about_bio_2':      forms.Textarea(attrs={'class': 'f-textarea', 'rows': 3}),
            'about_bio_3':      forms.Textarea(attrs={'class': 'f-textarea', 'rows': 3}),
            'location':         forms.TextInput(attrs={'class': 'f-input'}),
            'education':        forms.TextInput(attrs={'class': 'f-input'}),
            'email':            forms.EmailInput(attrs={'class': 'f-input'}),
            'github_url':       forms.URLInput(attrs={'class': 'f-input'}),
            'github_handle':    forms.TextInput(attrs={'class': 'f-input'}),
            'linkedin_url':     forms.URLInput(attrs={'class': 'f-input'}),
            'linkedin_handle':  forms.TextInput(attrs={'class': 'f-input'}),
            'languages':        forms.TextInput(attrs={'class': 'f-input'}),
            'resume_note':      forms.TextInput(attrs={'class': 'f-input'}),
            'footer_copy':      forms.TextInput(attrs={'class': 'f-input'}),
            'stat_projects':    forms.TextInput(attrs={'class': 'f-input'}),
            'stat_internships': forms.TextInput(attrs={'class': 'f-input'}),
            'stat_technologies':forms.TextInput(attrs={'class': 'f-input'}),
            'stat_experience':  forms.TextInput(attrs={'class': 'f-input'}),
            'is_available':     forms.CheckboxInput(attrs={'class': 'f-checkbox'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'percentage', 'order']
        widgets = {
            'name':       forms.TextInput(attrs={'class': 'f-input'}),
            'percentage': forms.NumberInput(attrs={'class': 'f-input', 'min': 0, 'max': 100}),
            'order':      forms.NumberInput(attrs={'class': 'f-input'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'icon', 'live_url', 'github_url', 'tags', 'order']
        widgets = {
            'name':        forms.TextInput(attrs={'class': 'f-input'}),
            'description': forms.Textarea(attrs={'class': 'f-textarea', 'rows': 3}),
            'status':      forms.Select(attrs={'class': 'f-input f-select'}),
            'icon':        forms.TextInput(attrs={'class': 'f-input'}),
            'live_url':    forms.URLInput(attrs={'class': 'f-input'}),
            'github_url':  forms.URLInput(attrs={'class': 'f-input'}),
            'tags':        forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'Django, Python, SQLite3'}),
            'order':       forms.NumberInput(attrs={'class': 'f-input'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['role', 'company', 'date_range', 'is_fulltime', 'bullets', 'order']
        widgets = {
            'role':       forms.TextInput(attrs={'class': 'f-input'}),
            'company':    forms.TextInput(attrs={'class': 'f-input'}),
            'date_range': forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'January 2025 - May 2025 · Delhi, India'}),
            'is_fulltime':forms.CheckboxInput(attrs={'class': 'f-checkbox'}),
            'bullets':    forms.Textarea(attrs={'class': 'f-textarea', 'rows': 5, 'placeholder': 'One bullet per line'}),
            'order':      forms.NumberInput(attrs={'class': 'f-input'}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuer', 'icon', 'order']
        widgets = {
            'name':   forms.TextInput(attrs={'class': 'f-input'}),
            'issuer': forms.TextInput(attrs={'class': 'f-input'}),
            'icon':   forms.TextInput(attrs={'class': 'f-input'}),
            'order':  forms.NumberInput(attrs={'class': 'f-input'}),
        }


class TypedRoleForm(forms.ModelForm):
    class Meta:
        model = TypedRole
        fields = ['label', 'order']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'f-input', 'placeholder': 'e.g. Django Developer'}),
            'order': forms.NumberInput(attrs={'class': 'f-input'}),
        }


class FAQItemForm(forms.ModelForm):
    class Meta:
        model = FAQItem
        fields = ['question', 'answer', 'order']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'f-input'}),
            'answer':   forms.Textarea(attrs={'class': 'f-textarea', 'rows': 3}),
            'order':    forms.NumberInput(attrs={'class': 'f-input'}),
        }
