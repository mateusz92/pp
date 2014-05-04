from django import forms
from main.models import User, Comment, Category, User, Perk
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core import validators


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('login','email','password')
        labels={
            'login': ('Login'),
            'email': ('Email'),
            'password': ('Haslo'),
        }
        widgets={
            'password': forms.PasswordInput()
        }

    confirmpassword = forms.CharField(label='Potwierdz haslo', widget=forms.PasswordInput())



class ProjectRegisterForm(forms.Form):
    title=forms.CharField(label='Nazwa projektu',widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_description=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    funding_goal=forms.IntegerField(label='Oczekiwana kwota wsparcia', widget=forms.NumberInput(attrs={'class': 'form-control','min':'0','max': '1000000', 'step': '10','type':'range','value':'0','onmousemove': 'valuechange()','width': 300}))
    description=forms.CharField(label='Opis projektu', widget=forms.Textarea(attrs={'style': 'visibility: hidden'}))
    category=forms.ModelChoiceField(queryset=Category.objects.all(),label='Kategoria',initial=1)

class ProjectPerks(forms.Form):
    perk_description=forms.CharField(label='Krotki opis progu',widget=forms.Textarea(attrs={'class': 'form-control'}))
    perk_value=forms.IntegerField(label='Oczekiwana kwota wsparcia', widget=forms.NumberInput(attrs={'min':'0','max': '1000000', 'step': '10','type':'range','value':'0','onmousemove': 'perkvaluechange()'}))

class ComentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class Signin(forms.ModelForm):
    class Meta:
        model=User
        fields=('login','password',)

class SupportForm(forms.ModelForm):
    class Meta:
        model=Perk
        fields=('amount',)
        labels={
            'amount' :('Kwota')
        }
amount=forms.DecimalField(label='Kwota', widget=forms.NumberInput)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment

class UserCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
