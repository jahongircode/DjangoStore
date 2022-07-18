from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import SearchForm, RegisterForm

#TgBot connection
from .handless import bot


def main_page(request):
    #Вывод всех названий
    all_products = Product.objects.all()

    search_bar = SearchForm()

    #Вывод всех названий категорий
    all_categories = Category.objects.all()

    context = {'products': all_products,
               'categories': all_categories,
               'form': search_bar}

    if request.method == 'POST':
        product_to_find = request.POST.get('search_product')

        try:
            search_result = Product.objects.get(product_name=product_to_find)

            return redirect(f'/{search_result.id}')

        except:
            return redirect('/')

    return render(request, 'index.html', context)


def about(request):
    return HttpResponse('About us')


def contacts(request):
    return HttpResponse('Contacts')


def content(request):
    return HttpResponse('content')

def get_full_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        Cart.objects.create(user_id=request.user.id, user_product=product, user_product_quantity=request.POST.get('counter'))
        return redirect(f'/{pk}')


    return render(request, 'about_product.html', {'product': product})

def get_full_category(request, pk):
    all_products = Product.objects.filter(product_category=pk)

    return render(request, 'category_product.html', {'products': all_products})



def get_user_cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        main_text = 'Новый заказ\n\n'

        for i in user_cart:
            main_text += f'Товар: {i.user_product}\nКоличество: {i.user_product_quantity}\n'

        bot.send_message(1172999069, main_text)
        user_cart.delete()
        return redirect('/')

    return render(request, 'user_cart.html', {'cart': user_cart})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def delete_item_from_cart(request, pk):
    user_cart = Cart.objects.filter(user_id = request.user.id, user_product=pk)
    user_cart.delete()

    return redirect('/cart')