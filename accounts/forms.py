from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from accounts.models import Account

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()


class ProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "avatar",
        )

    username = forms.CharField()
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()