import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from .models import UserProfile


class StyledAuthenticationForm(AuthenticationForm):
    """
    Django's built-in AuthenticationForm doesn't add Bootstrap's
    'form-control' class to its widgets by default -- this subclass adds
    it (and a placeholder) to each field, the same way StyledPasswordChangeForm
    does below, so the login page renders styled inputs out of the box.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter your username', 'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter your password', 'autocomplete': 'current-password',
        })


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email Address', 'autocomplete': 'email',
    }))
    first_name = forms.CharField(
        required=True, min_length=2, max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'First Name', 'pattern': "[A-Za-z ]+",
            'title': 'Only letters and spaces are allowed',
        })
    )
    last_name = forms.CharField(
        required=True, min_length=2, max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Last Name', 'pattern': "[A-Za-z ]+",
            'title': 'Only letters and spaces are allowed',
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username', 'minlength': '4', 'autocomplete': 'username',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password', 'minlength': '8', 'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password', 'minlength': '8', 'autocomplete': 'new-password',
        })

    def clean_first_name(self):
        name = self.cleaned_data['first_name'].strip()
        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError("First name can only contain letters and spaces.")
        return name.title()

    def clean_last_name(self):
        name = self.cleaned_data['last_name'].strip()
        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError("Last name can only contain letters and spaces.")
        return name.title()

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long.")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('photo', 'phone', 'bio', 'city', 'website', 'linkedin', 'github')
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief bio...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
        }

class StyledPasswordChangeForm(PasswordChangeForm):
    """
    Django's built-in PasswordChangeForm doesn't add Bootstrap's
    'form-control' class to its widgets by default -- this subclass adds
    it (and a placeholder) to each field so it matches the rest of the
    app's styling without duplicating all the built-in validation logic.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'old_password': 'Current Password',
            'new_password1': 'New Password',
            'new_password2': 'Confirm New Password',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(name, ''),
                'autocomplete': 'new-password' if name != 'old_password' else 'current-password',
            })
