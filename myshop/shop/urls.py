from django.urls import path

from . import views
from .views import product_detail, CategoryCreate, ProductCreate, book_detail, book_list, book_list_l, ShopLoginView, \
    BookCreate, GenreCreate, Blog_view, blog_detail, profile, ShopLogoutView, ShopUserRegisterView, index
from .views import product_list

app_name = 'shop'
urlpatterns = [
    path('api/',index,name='index'),

    path('accounts/register/',ShopUserRegisterView.as_view(),name='register'),
    path('accounts/login',ShopLoginView.as_view(),name='login'),
    path('', product_list, name='product_list'),
    path(r'^(P<category_slug>[-\w]+[^knigi])/$', product_list, name='product_list_by_category'),
    path(r'^(P<category_slug>/', book_list_l, name='genre_list'),
    path('knigi/', book_list, name='book_list'),
    path('Книги/<slug:genre_slug>/', book_list, name='book_list'),
    path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', product_detail, name='product_detail'),
    path(r'^/(?P<book_slug>[-\w]+)/$', book_detail, name='book_detail'),
    path('category/', CategoryCreate.as_view(), name='category'),
    path('product/', ProductCreate.as_view(), name='product'),
    path('book/', BookCreate.as_view(), name='book'),
    path('genre/', GenreCreate.as_view(), name='genre'),
    path('blog/',Blog_view.as_view(),name='blog'),
    path('blog/<message_id>',blog_detail,name='blog_detail'),
    path('accounts/profile/',profile,name='profile'),
    path('accounts/logout',ShopLogoutView.as_view(),name='logout')

]
