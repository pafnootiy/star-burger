import json
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# # foodcartapp
# from foodcartapp.models import Product, Order, OrderDetails
from .models import Product, Order, OrderDetails


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)

    print(dumped_products)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    ''' Регистрирую заказ от покупателя '''

    try: # доработать тесты на ошибки 
        if request.data['products'] or request.data['firstname'] or request.data['lastname'] or request.data['phonenumber'] or request.data['address'] is None:
            content = {'error': 'products: this field cannot be empty'}
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if request.data['products'] == []:
            content = {'error': 'products: this list cannot be empty'}
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.data['products'] > 100:
            content = {'error': 'invalid primary key'}
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.data['firstname'] == []:
            content = {'error': 'firstname: Not a valid string'}
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        else:
            customer = Order.objects.create(
                firstname=request.data['firstname'],
                lastname=request.data['lastname'],
                phonenumber=request.data['phonenumber'],
                address=request.data['address'],
            )

            for item in request.data['products']:

                product = Product.objects.get(id=item['product'])
                OrderDetails.objects.create(
                    order=customer,
                    product=product,
                    quantity=item['quantity'],

                )

            return Response(request.data)

    except TypeError:
        content = {'error': 'products is not a list, it is str'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except KeyError:
        content = {'error': 'products: required field'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
