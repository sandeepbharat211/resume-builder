"""
Data models for the `resume` app.

A Resume belongs to a User and has many related "sections" (Education,
Experience, Project, Skill, Certificate, Language, Hobby) attached via
ForeignKey, each cascading on delete so removing a Resume cleans up all
of its child rows automatically.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Indian mobile numbers: 10 digits, first digit 6-9.
phone_validator = RegexValidator(regex=r'^[6-9]\d{9}$', message="Enter a valid 10-digit mobile number.")

GENDER_CHOICES = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))

TEMPLATE_CHOICES = (
    ("modern", "Modern"),
    ("professional", "Professional"),
    ("creative", "Creative"),
    ("executive", "Executive"),
)


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    full_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="resume_photos/", blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[phone_validator])
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")
    postal_code = models.CharField(max_length=10, blank=True)
    summary = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    website = models.URLField(blank=True)
    template = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default="modern")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.profession})"

    def get_template_color(self):
        """Brand color associated with the resume's chosen template -- used
        to theme buttons/badges/borders throughout the UI."""
        colors = {"modern": "#0d6efd", "professional": "#198754", "creative": "#dc3545", "executive": "#212529"}
        return colors.get(self.template, "#0d6efd")



class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_studying = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experiences")
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=150)
    employment_type = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=200)
    technologies = models.CharField(max_length=250)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.project_name


class Skill(models.Model):
    LEVEL_CHOICES = (
        ("Beginner", "Beginner"), ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"), ("Expert", "Expert"),
    )
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    skill_name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="Intermediate")

    class Meta:
        ordering = ["skill_name"]

    def __str__(self):
        return self.skill_name

    def get_level_percent(self):
        levels = {"Beginner": 30, "Intermediate": 60, "Advanced": 80, "Expert": 95}
        return levels.get(self.level, 60)


class Certificate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="certificates")
    certificate_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    issue_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True)

    class Meta:
        ordering = ["certificate_name"]

    def __str__(self):
        return self.certificate_name


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="languages")
    language = models.CharField(max_length=100)
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=True)
    can_speak = models.BooleanField(default=True)

    class Meta:
        ordering = ["language"]

    def __str__(self):
        return self.language


class Hobby(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="hobbies")
    hobby_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["hobby_name"]

    def __str__(self):
        return self.hobby_name


class SiteVisitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    page = models.CharField(max_length=255, default="/")
    visited_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-visited_at"]

    def __str__(self):
        return f"{self.ip_address} - {self.page} - {self.visited_at}"
