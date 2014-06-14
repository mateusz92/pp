from django import forms
from main.models import User, Comment, Category, User, Perk
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators


class UserRegisterForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UserRegisterForm, self).__init__(*args,**kwargs)
        self.fields['login'].widget.attrs['required']=''
        self.fields['email'].widget.attrs['required']=''
        self.fields['password'].widget.attrs['required']=''
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


    confirmpassword = forms.CharField(label='Potwierdz haslo', widget=forms.PasswordInput(attrs={'required': ''}))



class ProjectRegisterForm(forms.Form):
    title=forms.CharField(label='Nazwa projektu',widget=forms.TextInput(attrs={'class': 'form-control', 'required': ''}))
    short_description=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'required': ''}))
    funding_goal=forms.IntegerField(label='Oczekiwana kwota wsparcia', widget=forms.NumberInput(attrs={'min': '0,01', 'max': '100000', 'step': '1','type':'Number','value':'0','onmousemove': 'valuechange()', 'required': ''}))
    description=forms.CharField(label='Opis projektu', widget=forms.Textarea(attrs={'style':'height: 0;visibility: collapse', 'required': ''}))
    category=forms.ModelChoiceField(queryset=Category.objects.all(),label='Kategoria',initial=1)

class ProjectPerks(forms.Form):
    perk_description=forms.CharField(label='Krotki opis progu',widget=forms.Textarea(attrs={'class': 'form-control'}))
    perk_value=forms.IntegerField(label='Oczekiwana kwota wsparcia', widget=forms.NumberInput(attrs={'class': 'form-control','min':'1','style': 'width: 500px','max': '1000000', 'step': '1','type':'range','value':'1','onmousemove': 'perkvaluechange()'}))

class ComentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class Signin(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(Signin, self).__init__(*args,**kwargs)
        self.fields['login'].widget.attrs['required']=''
        self.fields['password'].widget.attrs['required']=''
    class Meta:
        model=User
        fields=('login','password',)
        widgets={
            'password': forms.PasswordInput(),
        }
        labels={
            'password': 'Hasło'
        }
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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('email', 'password',)

class MessageForm(forms.Form):
    subject = forms.CharField(label='Tytuł', max_length=80, widget=forms.TextInput(attrs={'size': '80'}))
    user_to = forms.CharField(label='Odbiorca', max_length=50, widget=forms.TextInput(attrs={'size': '80'}))
    content = forms.CharField(label='Treść', widget=forms.Textarea(attrs={'cols' : '80'}))
