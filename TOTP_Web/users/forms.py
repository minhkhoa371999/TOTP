from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import OTP


# Create your forms here.
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=120)
    password = forms.CharField(required=True, min_length=6)


class OTPForm(forms.Form):
    otp = forms.CharField(required=True, min_length=6)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    serial = forms.CharField(required=True, max_length=10, min_length=10)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            otp_obj = OTP(user_id=user.id)
            otp_obj.serial = self.cleaned_data['serial']
            otp_obj.save()
        return user

