from django.contrib import admin
from .models import (
    SiteProfile, TypedRole, Skill, Project,
    Experience, Certification, ContactMessage, FAQItem
)

@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_available')

    def has_add_permission(self, request):
        # Only one SiteProfile row should ever exist (pk=1).
        # Prevent creating a second row via the admin.
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Deleting the single row would break the live site.
        return False

@admin.register(TypedRole)
class TypedRoleAdmin(admin.ModelAdmin):
    list_display = ('label', 'order')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'order')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'order')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'date_range', 'order')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'order')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'is_read')
    readonly_fields = ('submitted_at',)

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
