"""
ModelForms for the `resume` app.

Each form excludes fields the user shouldn't set directly (resume FK,
timestamps) and applies Bootstrap CSS classes via `widgets` so templates
can just do `{{ field }}` and get consistently styled inputs.
"""

from django import forms
from .models import Resume, Education, Experience, Project, Skill, Certificate, Language, Hobby


class ResumeForm(forms.ModelForm):
    """Main resume form: personal info + the profile photo (adjusted client-side via the crop widget before upload -- see static/js/photo-cropper.js)."""
    class Meta:
        model = Resume
        exclude = ('user', 'created_at', 'updated_at')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python Developer'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'template': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return phone


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ('resume', 'created_at')
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CGPA / Percentage'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currently_studying': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ('resume', 'created_at')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full-time / Internship / Freelance'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currently_working': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('resume', 'created_at')
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, Bootstrap...'}),
            'project_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ('resume',)
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        exclude = ('resume',)
        widgets = {
            'certificate_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'credential_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ('resume',)
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Hindi'}),
            'can_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_write': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        exclude = ('resume',)
        widgets = {
            'hobby_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Reading'}),
        }
