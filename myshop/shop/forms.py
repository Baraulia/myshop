import datetime
from django.contrib import admin

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Category, Product, Genre, Book, Blog, ExtendUser


class CategoryForm(forms.Form):
    name = forms.CharField(label="Введите название категории", max_length=50, widget=forms.TextInput(attrs={'class':'slug'}))
    slug = forms.CharField(label="Введите slug", max_length=50, widget=forms.TextInput(attrs={'class':'slug'}))
    def save(self):
        new_category=Category.objects.create(
            name=self.cleaned_data['name'],
            slug=self.cleaned_data['slug']
    )
        return new_category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(label="Выберите категорию товара", widget=forms.Select(attrs={'class':'slug'}),queryset=Category.objects.all(), empty_label=None)
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'slug'}),label="Укажите название товара",max_length=50)
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class':'slug'}),label="Слаг товара",max_length=50)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'slug'}), required=True)
    description = forms.CharField(label="Укажите описание",widget=forms.Textarea(attrs={'class':'slug'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'slug'}),label="Укажите стоимость товара",max_digits=10, decimal_places=2)
    stock = forms.IntegerField(min_value=0,label="Укажите количество товара на складе",widget=forms.NumberInput(attrs={'class':'slug'}))
    available = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'slug'}), label="Укажите доступен ли товар",required=True)
    class Meta:
        model=Product
        fields=('category', 'name','slug', 'description', 'price','image','stock','available')

class GenreForm(forms.ModelForm):
    name = forms.CharField(label="Введите название жанра", max_length=50, widget=forms.TextInput(attrs={'class':'slug'}))
    slug = forms.CharField(label="Введите slug", max_length=50, widget=forms.TextInput(attrs={'class':'slug'}))
    class Meta:
        model=Genre
        fields=('category','name','slug')
        widgets = {'category': forms.HiddenInput}

class BookForm(forms.ModelForm):
    CHOICES = (
        (1989, '1989'), (1990, '1990'), (1991, '1991'), (1992, '1992'), (1993, '1993'), (1994, '1994'), (1995, '1995'),
        (1996, '1996'),
        (1997, '1997'), (1998, '1998'), (1999, '1999'), (2000, '2000'), (2001, '2001'), (2002, '2002'), (2003, '2003'),
        (2004, '2004'), (2005, '2005'), (2006, '2006'), (2007, '2007'), (2008, '2008'), (2009, '2009'), (2010, '2010'),
        (2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015'), (2016, '2016'), (2017, '2017'),
        (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'),
    )
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'slug'}),label="Укажите название книги",max_length=50)
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class':'slug'}),label="Укажите slug книги",max_length=50)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'slug'}), required=True)
    author = forms.CharField(widget=forms.TextInput(attrs={'class':'slug'}),label="Укажите автора книги",max_length=50)
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'slug'}),label="Укажите стоимость книги",max_digits=10, decimal_places=2)
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={'class':'slug'}),label="Укажите количество книг на складе")
    available = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'slug'}), label="Укажите доступна ли книга",required=True)
    year = forms.ChoiceField(widget=forms.Select(attrs={'class':'slug'}),choices=CHOICES)
    description = forms.CharField(label="Укажите описание",widget=forms.Textarea(attrs={'class':'slug'}))
    sheets = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={'class':'slug'}),label="Укажите количество страниц в книге")
    published_by = forms.CharField(widget=forms.TextInput(attrs={'class':'slug'}),label="Укажите издательство",max_length=50)
    class Meta:
        model=Book
        fields="__all__"

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'slug'}),label="Сообщение")
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'slug'}), required=False)
    class Meta:
        model=Blog
        exclude=('created',)
        widgets={'author':forms.HiddenInput}

class UserFormRegistration(forms.ModelForm):
    username = forms.CharField(help_text=None,widget=forms.TextInput(attrs={'class':'slug'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'slug'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'slug'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'slug'}))
    messages=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'slug'}),initial=True,label="Сообщение о новых товарах")
    telefon=forms.CharField(widget=forms.TextInput(attrs={'class':'slug'}))
    class Meta():
        model=ExtendUser
        fields=('username','email','password1','password2','messages','telefon')
    def valid_password(self):
        password1=self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1!=password2:
            errors = {'password2':ValidationError('Введенные пароли не совпадают', code = 'password_mismatch')}

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.telefon = self.cleaned_data['telefon']
        user.messages = self.cleaned_data['messages']
        user.is_active=True
        user.is_activated=True
        if commit:
            user.save()
            print('2')
        return user
class UserFormRegistration2(forms.Form):
    username = forms.CharField(help_text=None, widget=forms.TextInput(attrs={'class': 'slug'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'slug'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'slug'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'slug'}))
    messages = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'slug'}), initial=True,
                                  label="Сообщение о новых товарах")
    telefon = forms.CharField(widget=forms.TextInput(attrs={'class': 'slug'}))
    def valid_password(self):
        password1=self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1!=password2:
            errors = {'password2':ValidationError('Введенные пароли не совпадают', code = 'password_mismatch')}
    def save(self):
        user=ExtendUser.objects.create_user(username=self.cleaned_data['username'],
                                            telefon=self.cleaned_data['telefon'],
                                            password=self.cleaned_data['password1'],
                                            messages=self.cleaned_data['messages'],
                                            is_active=True, is_activated=True)
        print(1)
        return user





