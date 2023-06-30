from rest_framework.serializers import ModelSerializer
from foodcartapp.models import Product
from foodcartapp.models import Product, OrderDetails,Order


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


    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product = Product.objects.get(name=product_data['product'])
            OrderDetails.objects.create(
                order=order,
                product=product,
                quantity=product_data['quantity'],
                product_price=product.price
            )
        return order
