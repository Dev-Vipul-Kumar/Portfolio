from django.db import models


class SiteProfile(models.Model):
    """Single-row table - the owner's core identity data."""
    full_name        = models.CharField(max_length=100, default="Vipul Kumar")
    first_name       = models.CharField(max_length=50,  default="Vipul")
    last_name        = models.CharField(max_length=50,  default="Kumar")
    tagline          = models.CharField(max_length=200, default="BCA student, Django developer, and lifelong builder.")
    hero_description = models.TextField(default="I build clean, fast, and scalable web applications.")
    about_bio_1      = models.TextField(default="", blank=True)
    about_bio_2      = models.TextField(default="", blank=True)
    about_bio_3      = models.TextField(default="", blank=True)
    location         = models.CharField(max_length=100, default="Delhi, India")
    education        = models.CharField(max_length=150, default="BCA · BCIT 2022-25")
    email            = models.EmailField(default="vipulsam1234@gmail.com")
    github_url       = models.URLField(default="https://github.com/Vipul-Kumar-Dev")
    github_handle    = models.CharField(max_length=100, default="Vipul-Kumar-Dev")
    linkedin_url     = models.URLField(default="https://www.linkedin.com/in/vipul-kumar-dev/")
    linkedin_handle  = models.CharField(max_length=100, default="vipul-kumar-dev")
    languages        = models.CharField(max_length=100, default="English, Hindi")
    resume_note      = models.CharField(max_length=200, default="Get the full picture - all my experience, skills, and projects in one clean PDF.")
    footer_copy      = models.CharField(max_length=200, default="© 2025 Vipul Kumar · Built with Django")
    # Stats (hero)
    stat_projects    = models.CharField(max_length=20, default="3+")
    stat_internships = models.CharField(max_length=20, default="2")
    stat_technologies= models.CharField(max_length=20, default="8+")
    stat_experience  = models.CharField(max_length=20, default="1.5y")
    is_available     = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Profile"

    def __str__(self):
        return self.full_name

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class TypedRole(models.Model):
    """Roles that cycle in the hero typing animation."""
    label = models.CharField(max_length=80)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label


class Skill(models.Model):
    name       = models.CharField(max_length=80)
    percentage = models.PositiveSmallIntegerField(default=80)
    order      = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Project(models.Model):
    STATUS_CHOICES = [("live", "Live"), ("wip", "In progress"), ("archived", "Archived")]
    name        = models.CharField(max_length=120)
    description = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default="wip")
    icon        = models.CharField(max_length=10, default="💻", help_text="Emoji icon")
    live_url    = models.URLField(blank=True, default="")
    github_url  = models.URLField(blank=True, default="")
    tags        = models.CharField(max_length=300, default="",
                                   help_text="Comma-separated tags, e.g. Django,Python,SQLite3")
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class Experience(models.Model):
    role        = models.CharField(max_length=120)
    company     = models.CharField(max_length=120)
    date_range  = models.CharField(max_length=100, help_text="e.g. January 2025 - May 2025 · Delhi, India")
    is_fulltime = models.BooleanField(default=False)
    bullets     = models.TextField(help_text="One bullet point per line")
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def bullet_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]


class Certification(models.Model):
    name   = models.CharField(max_length=150)
    issuer = models.CharField(max_length=100)
    icon   = models.CharField(max_length=10, default="🏆", help_text="Emoji icon")
    order  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name              = models.CharField(max_length=100)
    email             = models.EmailField()
    phone             = models.CharField(max_length=15, blank=True, null=True)
    preferred_contact = models.CharField(
        max_length=10,
        choices=[("email", "Email"), ("phone", "Phone")],
        default="email"
    )
    best_time    = models.CharField(max_length=100, blank=True, null=True)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} - {self.submitted_at:%Y-%m-%d %H:%M}"


class FAQItem(models.Model):
    """FAQ entries shown on the FAQ page accordion (replaces hardcoded HTML)."""
    question = models.CharField(max_length=255)
    answer   = models.TextField()
    order    = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
