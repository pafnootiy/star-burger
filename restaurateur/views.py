from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from geopy.distance import distance
from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from location.geo_location import get_or_create_locations


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {
            item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(
            restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):

    context = []
    orders = Order.objects.count_price().filter(status='unprocessed')
    order_addresses = [order.address for order in orders]
    restaurant_addresses = [
        restaurant.address for restaurant in Restaurant.objects.all()
    ]
    locations = get_or_create_locations(
        *order_addresses, *restaurant_addresses
    )
    restaurant_menu_items = RestaurantMenuItem.objects.select_related(
        'restaurant', 'product'
    )
    for order in orders:
        order_restaurants = []
        for order_product in order.orders.all():
            product_restaurants = set(menu_item.restaurant for menu_item in restaurant_menu_items
                                      if order_product.product == menu_item.product
                                      and menu_item.availability)
            order_restaurants.append(product_restaurants)
        suitable_restaurants = set.intersection(*order_restaurants)

        order_location = locations.get(order.address, None)
        for restaurant in suitable_restaurants:
            restaurant_location = locations.get(restaurant.address, None)
            restaurant_distance = round(distance(
                order_location, restaurant_location).km, 2)

        sorted_suitable_restaurants = sorted(
            suitable_restaurants, key=lambda restaurant: restaurant_distance)

        context.append({
            'id': order.id,
            'status': order.get_status_display(),
            'amount': order.amount,
            'payment': order.get_payment_display(),
            'firstname': order.firstname,
            'lastname': order.lastname,
            'phonenumber': order.phonenumber,
            'address': order.address,
            'comment': order.comment,
            'restaurants': sorted_suitable_restaurants,
            'distance': restaurant_distance,
        })

    return render(request, template_name='order_items.html', context={
        'order_items': context})
