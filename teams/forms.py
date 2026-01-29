from django import forms
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Acme Corp'})
        }

class InviteMemberForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username to invite'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username does not exist.")
        return username
