from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from base.models import Review
from base.models import Product
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from base.serializers import ProductSerializer




class ProductView(APIView):
    def get(self, request):
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request):
    user = request.user
    data = request.data
    product_id = data['product']
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        content = {'detail': 'Product not found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    # product = Product.objects.get(name=name)

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            name=user.username,
            product=product,
            rating=data['rating'],
            comment=data['comment'],
        )
  

    reviews = product.review_set.all()
    product.numReviews = len(reviews)

    total = 0
    for i in reviews:
        total += i.rating

    product.rating = total / len(reviews)
    product.save()

    return Response({'detail': 'Review Added'})



