from django.contrib import admin



# ====================================================================================
# def view_orders(request):
#     orders = Order.objects.filter(status='NEW')\
#         .fetch_with_price().fetch_with_suitable_restaurants()

#     order_addresses = [order.address for order in orders]
#     restaurant_addresses = [
#         restaurant.address for restaurant in Restaurant.objects.all()
#     ]
#     locations = get_or_create_locations(
#         *order_addresses, *restaurant_addresses
#     )
#     for order in orders:
#         order_location = locations.get(order.address, None)
#         for restaurant in order.suitable_restaurants:
#             restaurant_location = locations.get(restaurant.address, None)
#             if not (order_location and restaurant_location):
#                 restaurant.distance = 0
#                 restaurant.readable_distance = 0
#                 continue
#             restaurant.distance = distance(
#                 order_location, restaurant_location
#             ).km
#             restaurant.readable_distance = generate_human_readable_distance(
#                 restaurant.distance
#             )
#         sorted_suitable_restaurants = sorted(
#             order.suitable_restaurants,
#             key=lambda restaurant: restaurant.distance
#         )
#         order.suitable_restaurants = sorted_suitable_restaurants
# ===================================================================================================
