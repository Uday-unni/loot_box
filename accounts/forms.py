from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def save(self,commit=True):
        user=super(UserRegisterForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user


