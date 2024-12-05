from django import forms
from .models import Book, Rating
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['titre', 'auteur', 'genre', 'synopsis', 'couverture']

    def clean_couverture(self):
        couverture = self.cleaned_data.get('couverture')
        valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
        if couverture:
            if couverture.content_type not in valid_mime_types:
                raise forms.ValidationError("Unsupported file type. Please upload a JPEG, PNG, or GIF image.")
        return couverture

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

class UserForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        help_text=""  
    )
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self) : 
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        return user
