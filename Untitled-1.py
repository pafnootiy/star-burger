{"products": [{"product": 5, "quantity": 1}, {"product": 6, "quantity": 4}],
        "firstname": "Фридрех", "lastname": "Энгельс ", "phonenumber": "+79037892345", "address": "Москва"}


print(test["products"])

for product in test["products"]:
    print(product)


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['order', 'product', 'quantity', ]


class OrderSerializer(ModelSerializer):
    order_details = OrderDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname',
                  'phonenumber', 'address', 'order_details']


@api_view(['POST'])
def register_order(request):
    ''' Регистрирую заказ от покупателя '''

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer = Order.objects.create(
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
        address=serializer.validated_data['address'],)

    for item in serializer.validated_data['products']:

        product = Product.objects.get(id=item['product'])
        OrderDetails.objects.create(
            order=customer,
            product=product,
            quantity=item['quantity'])

    return Response(serializer.validated_data)







MVP


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderDetailsSerializer(
        many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname',
                  'phonenumber', 'address']


@api_view(['POST'])
def register_order(request):
    ''' Регистрирую заказ от покупателя '''

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer = Order.objects.create(
        firstname=request.data['firstname'],
        lastname=request.data['lastname'],
        phonenumber=request.data['phonenumber'],
        address=request.data['address'],)

    for item in request.data['products']:
        product = Product.objects.get(id=item['product'])
        OrderDetails.objects.create(
            order=customer,
            product=product,
            quantity=item['quantity'])

    return Response(request.data)
