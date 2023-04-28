from foodcartapp.models import Order, OrderDetails
from rest_framework.serializers import ModelSerializer


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderDetailsSerializer(
        many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname',
                  'phonenumber', 'address']
