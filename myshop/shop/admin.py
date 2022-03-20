from django.contrib import admin
from .models import Category, Product, Genre, Book, ExtendUser,Blog


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','stock','available','created','updated']
    list_filter = ['available','created','updated']
    list_editable = ['price','stock','available']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product,ProductAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ['name','slug','author','price','stock','available','year','sheets','published_by']
    list_filter = ['available']
    list_editable = ['price','stock','available']
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Book,BookAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

# class ExtendUserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'password']


admin.site.register(Genre,GenreAdmin)
admin.site.register(ExtendUser)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['author','content']


admin.site.register(Blog, BlogAdmin)



