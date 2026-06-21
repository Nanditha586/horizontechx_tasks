from django import forms
from django.contrib.auth.models import User

#register form: contains username, email and password. The password field is rendered as a password input.
class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "User already exists with this email."
            )

        return email

 
    def clean_password(self):

        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must contain at least 8 characters."
            )

        return password

#login form: contains username and password. The password field is rendered as a password input.


from django import forms

class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder':'Enter Email'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Enter Password'
            }
        )
    )