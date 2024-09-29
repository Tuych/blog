from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 7}))
    captcha = CaptchaField()


class RegisterUserForm(UserCreationForm):   # UserCreationForm dan meros oldi.Chunki biz djangoning User modilidan foydalanamiz
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']

        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-input'}),
                'slug': forms.TextInput(attrs={'class': 'form-input'}),
                'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 7}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'






"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
     formaga classlar yordamida 2 uslubda qushimcha stillar bersak bulsai
     Meta classdan oldin berilgan stillar yordamida ustun data type sini uzgartirish -- forms.CharField(label='Логин
     wedgets - ichida bulsa input typesini uzgartira olamiz --- forms.TextInput(attrs={'class': 'form-input'}

"""