from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserSignupForm(forms.ModelForm):
    """
    Form for user signup.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "role"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Form for user login.
    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput
    )
