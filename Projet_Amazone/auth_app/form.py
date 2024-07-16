from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser
from datetime import datetime
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
    )
    first_name = forms.CharField(
        label="Nom",
        required=True
    )
    last_name = forms.CharField(
        label="Prenom",
        required=True
    )
    date_of_birth = forms.DateField(
        label="Date de Naissance",
        required=True,
        widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1))
    )
    phone = forms.CharField(
        label="Numero de telephone",
        max_length=15,
        required=True
    )
    address = forms.CharField(
        label="Addresse",
        max_length=50,
        required=True
    )
    postal_code = forms.CharField(
        label="Code postal",
        max_length=10,
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone', 'date_of_birth', 'email', 'address', 'postal_code')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("Le nom doit contenir uniquement des lettres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Le prénom doit contenir uniquement des lettres.")
        return last_name

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age = (datetime.now().date() - date_of_birth).days / 365.25
        if age < 18:
            raise forms.ValidationError("Vous devez avoir au moins 18 ans.")
        return date_of_birth

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Canadian phone number pattern: +1 123-456-7890 or 123-456-7890
        pattern = re.compile(r'^(?:\+1\s?)?\(?[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not pattern.match(phone):
            raise forms.ValidationError("Le numéro de téléphone doit être valide et au bon format.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not re.match(r'^\d+ [a-zA-Z0-9 ]+$', address):
            raise forms.ValidationError("Veuillez entrer une adresse valide.")
        return address

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', postal_code):
            raise forms.ValidationError("Veuillez entrer un code postal valide au Canada (format: A1A 1A1).")
        return postal_code

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class CustomUserChangeForm(UserChangeForm):
    password = None  
    email = forms.EmailField(
        label="Email",
        required=True
    )
    first_name = forms.CharField(
        label="Nom",
        required=True
    )
    last_name = forms.CharField(
        label="Prenom",
        required=True
    )
    date_of_birth = forms.DateField(
        label="Date de Naissance",
        required=True,
        widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1))
    )
    phone = forms.CharField(
        label="Numero de telephone",
        max_length=15,
        required=True
    )
    address = forms.CharField(
        label="Addresse",
        max_length=50,
        required=True
    )
    postal_code = forms.CharField(
        label="Code postal",
        max_length=10,
        required=True
    )

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone', 'date_of_birth', 'email', 'address', 'postal_code', 'is_staff', 'is_superuser')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.email == email:
            return email
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("Le nom doit contenir uniquement des lettres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Le prénom doit contenir uniquement des lettres.")
        return last_name

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age = (datetime.now().date() - date_of_birth).days / 365.25
        if age < 18:
            raise forms.ValidationError("Vous devez avoir au moins 18 ans.")
        return date_of_birth

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = re.compile(r'^(?:\+1\s?)?\(?[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not pattern.match(phone):
            raise forms.ValidationError("Le numéro de téléphone doit être valide et doit être au format canadien.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not re.match(r'^\d+ [a-zA-Z0-9 ]+$', address):
            raise forms.ValidationError("Veuillez entrer une adresse valide.")
        return address

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', postal_code):
            raise forms.ValidationError("Veuillez entrer un code postal valide au Canada (format: A1A 1A1).")
        return postal_code
    
class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Le mot de passe actuel est incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password2', "Les mots de passe ne correspondent pas.")
        return cleaned_data
    

class CustomUserChangeFormClient(UserChangeForm):
    password = None  
    email = forms.EmailField(
        label="Email",
        required=True
    )
    first_name = forms.CharField(
        label="Nom",
        required=True
    )
    last_name = forms.CharField(
        label="Prenom",
        required=True
    )
    date_of_birth = forms.DateField(
        label="Date de Naissance",
        required=True,
        widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1))
    )
    phone = forms.CharField(
        label="Numero de telephone",
        max_length=15,
        required=True
    )
    address = forms.CharField(
        label="Addresse",
        max_length=50,
        required=True
    )
    postal_code = forms.CharField(
        label="Code postal",
        max_length=10,
        required=True
    )

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone', 'date_of_birth', 'email', 'address', 'postal_code')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.email == email:
            return email
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("Le nom doit contenir uniquement des lettres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Le prénom doit contenir uniquement des lettres.")
        return last_name

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age = (datetime.now().date() - date_of_birth).days / 365.25
        if age < 18:
            raise forms.ValidationError("Vous devez avoir au moins 18 ans.")
        return date_of_birth

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = re.compile(r'^(?:\+1\s?)?\(?[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not pattern.match(phone):
            raise forms.ValidationError("Le numéro de téléphone doit être valide et doit être au format canadien.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not re.match(r'^\d+ [a-zA-Z0-9 ]+$', address):
            raise forms.ValidationError("Veuillez entrer une adresse valide.")
        return address

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', postal_code):
            raise forms.ValidationError("Veuillez entrer un code postal valide au Canada (format: A1A 1A1).")
        return postal_code
    