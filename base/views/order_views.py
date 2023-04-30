from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import ShippingAddressSerializer

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # (1) Create order

        order = Order.objects.create(
            user=user,
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

      
        # Calculate the delivery time
        delivery_time = timezone.now() + timedelta(days=6)

        # (3) Create order items adn set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(id=i["id"])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=i['price'],
                image=product.proimage,
            )

            # (4) Update stock

            product.count_in_stock -= item.quantity
            product.save()
        # Set the delivery time and mark the order as delivered
        order.deliveredAt = delivery_time
        order.isDelivered = False
        order.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addshipping(request):
    user = request.user
    data = request.data

    # Check if the user already has a shipping address
    try:
        shipping = ShippingAddress.objects.get(user=user)
        return Response({'message': 'Shipping address already exists.'})
    except ShippingAddress.DoesNotExist:
        # Create shipping address
        shipping = ShippingAddress.objects.create(
            user=user,
            address=data['address'],
            city=data['city'],
            postalCode=data['postalCode'],
            country=data['country'],
            phone=data['phone']
        )
        return Response({'message': 'Shipping address added successfully.'})
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateshipping(request):
    user = request.user
    data = request.data
    # Check if the user has a shipping address
    try:
        shipping = ShippingAddress.objects.get(user=user)
    except ShippingAddress.DoesNotExist:
        return Response({'message': 'No shipping address found.'})

    # Update shipping address fields
    shipping.address = data.get('address', shipping.address)
    shipping.city = data.get('city', shipping.city)
    shipping.postalCode = data.get('postalCode', shipping.postalCode)
    shipping.country = data.get('country', shipping.country)
    shipping.phone = data.get('phone', shipping.phone)
    shipping.save()

    return Response({'message': 'Shipping address updated successfully.'})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
  
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)

# get my shipping address
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getMyShippingAddressbyid(request, pk):
#     user = request.user
#     try:
#         order = user.order_set.get(_id=pk)
#         shipping = ShippingAddress.objects.get(order=order)
#         shipping_list = [shipping]
#         serializer = ShippingAddressSerializer(shipping_list, many=True)
#         return Response(serializer.data)
#     except Order.DoesNotExist:
#         return Response({'detail': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#     except ShippingAddress.DoesNotExist:
#         return Response({'detail': 'Shipping address does not exist.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyShippinginfo(request):
    user = request.user
    try:
        shipping = ShippingAddress.objects.get(user=user)
        serializer = ShippingAddressSerializer(shipping)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'detail': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except ShippingAddress.DoesNotExist:
        return Response({'detail': 'Shipping address does not exist.'}, status=status.HTTP_404_NOT_FOUND)



# delete
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response([serializer.data])  # Wrap data in a list
        else:
            Response({'detail': 'Not authorized to view this order'},
                    status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was paid')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')
