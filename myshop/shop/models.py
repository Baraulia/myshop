from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name =models.CharField(max_length=200,db_index=True)
    slug= models.SlugField(max_length=200,db_index=True,unique=True)
    class Meta:
        ordering=('name',)
        verbose_name='Категория'
        verbose_name_plural='Категории'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        if self.slug != "knigi":
            return  reverse('shop:product_list_by_category',
                            args=[self.slug])

        else:
            return reverse('shop:genre_list',args=[self.slug])


class Product(models.Model):
    category=models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200,db_index=True)
    image =models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description =models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock =models.PositiveIntegerField()
    available= models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('name',)
        index_together=(('id','slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return  reverse('shop:product_detail',
                        args=[self.id,self.slug])



class Genre(models.Model):
    category = models.ForeignKey(Category, default='Книги',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book_list',
                           args=[self.slug])


class Book(models.Model):
    CHOICES=(
        (1989,'1989'),(1990,'1990'),(1991,'1991'),(1992,'1992'),(1993,'1993'),(1994,'1994'),(1995,'1995'),(1996,'1996'),
        (1997, '1997'), (1998, '1998'), (1999, '1999'), (2000, '2000'), (2001, '2001'), (2002, '2002'), (2003, '2003'),
        (2004, '2004'), (2005, '2005'), (2006, '2006'), (2007, '2007'),(2008, '2008'), (2009, '2009'), (2010, '2010'),
        (2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015'), (2016, '2016'), (2017, '2017'),
        (2018, '2018'),(2019, '2019'), (2020, '2020'), (2021, '2021'),
    )
    genres=models.ManyToManyField(Genre,related_name='genre')
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200)
    image =models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    author =models.CharField(max_length=200, db_index=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock =models.PositiveIntegerField()
    available= models.BooleanField(default=True)
    year= models.PositiveIntegerField(choices=CHOICES)
    description=models.TextField(blank=True)
    sheets=models.PositiveIntegerField()
    published_by=models.CharField(max_length=200)

    class Meta:
        ordering=('name',)
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return  reverse('shop:book_detail',
                        args=[self.slug])

class ExtendUser(AbstractUser):
    telefon = models.CharField(max_length=50,db_index=True,unique=True)
    messages=models.BooleanField(default=True,verbose_name="Сообщение о новых товарах")
    is_activated=models.BooleanField(default=True, db_index=True)
    class Meta(AbstractUser.Meta):
        pass

class Blog(models.Model):
    author = models.ForeignKey(ExtendUser,on_delete=models.CASCADE)
    content=models.TextField(verbose_name="Текст сообщения")
    image=models.ImageField(upload_to='blog/%Y/%m/%d',blank=True)
    created=models.DateTimeField(auto_now_add=True,db_index=True,verbose_name='Опубликовано')
    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'
        ordering = ['created']
    def get_absolute_url(self):
        return  reverse('shop:blog_detail',
                        args=[self.id])