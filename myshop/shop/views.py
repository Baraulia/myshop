from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView

from .forms import CategoryForm, ProductForm, GenreForm, BookForm, BlogForm, UserFormRegistration, UserFormRegistration2
from .models import Category, Product, Book, Genre, Blog, ExtendUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def product_list(request,category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    books=Book.objects.filter(available=True)
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products= products.filter(category=category)
        books=Book.objects.filter()


    content= {'category':category,
              'categories':categories,
              'products':products,
              'books':books}
    return  render(request,'shop/product/list.html',content)

def product_detail(request,id,slug):
    product=get_object_or_404(Product,id=id,slug=slug,available=True)
    content={'product':product}
    return render(request,'shop/product/detail.html',content)

class CategoryCreate(View):
    def get(self,request):
        form=CategoryForm()
        return render(request,'shop/product/create_category.html',context={'form':form})
    def post(self,request):
        bound_form=CategoryForm(request.POST)
        if bound_form.is_valid():
            category = bound_form.save()
            return redirect(category)
        return render(request, 'shop/product/create_category.html', context={'form': bound_form})

class ProductCreate(View):
    def get(self,request):
        form_product=ProductForm()
        return render(request,'shop/product/create_product.html', context={'form_product':form_product})
    def post(self,request):
        bound_form=ProductForm(request.POST, request.FILES)
        if bound_form.is_valid():
            product = bound_form.save()
            product.save()
            return redirect(product)
        return render(request, 'shop/product/create_product.html', context={'form_product': bound_form})
def index(request):
    data=request.POST
    if data['pass1']==data['pass2']:
        user=ExtendUser.objects.create(data)
        user.save
def book_list_l(request, category_slug):
    ganr=None
    genris=Genre.objects.all()
    books=Book.objects.filter(available=True)
    category=get_object_or_404(Category,slug=category_slug)
    categories = Category.objects.all()

    context= {'categories':categories,
             'ganr':ganr,
              'genris':genris,
              'books':books,
              'category':category}
    return  render(request,'shop/product/list_genre.html',context)


def book_list(request,genre_slug=None):
    ganr = None
    genris=Genre.objects.all()
    books=Book.objects.filter(available=True)
    category=get_object_or_404(Category,name='Книги')
    categories=Category.objects.all()
    if genre_slug:
        ganr=get_object_or_404(Genre,slug=genre_slug)
        books=Book.objects.filter(genres=ganr.id)

    context= {'category':category,
              'categories':categories,
             'ganr':ganr,
              'genris':genris,
              'books':books

}

    return  render(request,'shop/product/list_genre.html',context)

def book_detail(request,book_slug):
    book=get_object_or_404(Book,slug=book_slug,available=True)
    genres = Genre.objects.filter(genre=book.id)
    print(genres)
    category = get_object_or_404(Category, name='Книги')
    categories = Category.objects.all()
    genris = Genre.objects.all()

    context={'book':book,'category':category,'categories':categories,'genris':genris,'genres':genres}
    return render(request,'shop/product/detail_book.html',context)
class GenreCreate(View):
    def get(self,request):
        form=GenreForm()
        category = Category.objects.get(name='Книги')
        form.initial['category'] = category.id
        return render(request,'shop/product/create_genre.html',context={'form':form})
    def post(self,request):
        bound_form=GenreForm(request.POST)

        if bound_form.is_valid():
            genre = bound_form.save()
            genre.save()
            return redirect(genre)
        return render(request, 'shop/product/create_genre.html', context={'form': bound_form})

class BookCreate(View):
    def get(self,request):
        form_book=BookForm()
        return render(request,'shop/product/create_book.html', context={'form_book':form_book})
    def post(self,request):
        bound_form=BookForm(request.POST, request.FILES)
        if bound_form.is_valid():
            book = bound_form.save()
            book.save()
            return redirect(book)
        return render(request, 'shop/product/create_book.html', context={'form_book': bound_form})

class ShopLoginView(LoginView):
    template_name = 'shop/user/login.html'
    redirect_field_name = 'shop/user/profile.html'
@login_required
def profile(request):
    return  render(request,'shop/user/profile.html')
class Blog_view(View):
    def get(self,request):
        form_blog = BlogForm()
        messages = Blog.objects.all()
        paginator = Paginator(messages, 3)
        if 'page' in request.GET:
            page_num=request.GET['page']
        else:
            page_num=1
        page=paginator.get_page(page_num)
        if request.user.pk:
            author=ExtendUser.objects.get(pk=request.user.pk)
            form_blog.initial['author']=author
        return render(request,'shop/product/blog.html', context={'form_blog':form_blog, 'messages':page.object_list,'page':page})
    def post(self,request):
        bound_form=BlogForm(request.POST, request.FILES)
        messages = Blog.objects.all()
        if bound_form.is_valid():
            message=bound_form.save()
            return redirect(message)
        return render(request, 'shop/product/blog.html', context={'form_blog': bound_form, 'messages':messages})
def blog_detail (request,message_id):
    message = get_object_or_404(Blog, id=message_id)
    categories = Category.objects.all()
    context = {'message': message, 'categories': categories}
    return render(request, 'shop/product/detail_blog.html', context)
class ShopLogoutView(LoginRequiredMixin,LogoutView):
    next_page = '/'
class ShopUserRegisterView(View):
    def get(self,request):
        Form_form = UserFormRegistration2()
        ModelForm_form = UserFormRegistration()
        context = {'form': ModelForm_form, 'form2': Form_form}
        return render(request, 'shop/user/user_register.html',context)
    def post(self,request):
        if 'model_form' in request.POST:
            bound_form=UserFormRegistration(request.POST)

        else:
            bound_form=UserFormRegistration2(request.POST)

        if bound_form.is_valid():
            bound_form.valid_password()
            bound_form.clean()
            bound_form.save()


        return redirect('shop:product_list')












