from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import productSerializer
# from .models import Gallery
# from .models import Profile
# from .models import Albums
# from .models import AlbumsType
# from .models import Payment


import os

# Create your views here.

# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
    user.is_active = True
    user.is_staff = False
    user.save()
    return Response("new user created")

# ----------------------------------------Product crud -start--------------------------------------------------


# @permission_classes([IsAuthenticated])
class ProductView(APIView):

    def get(self, request):
        if request.user.is_authenticated: 
            my_model = Product.objects.all()
            serializer = productSerializer(my_model, many=True)
            return Response(serializer.data)
        return Response("please login")


    def post(self, request):
        # usr =request.user
        # print(usr)
        serializer = productSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
     
        my_model = Product.objects.get(pk=pk)
        serializer = productSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        my_model = Product.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Product CRUD - end


# ---------------------------------------------------Payment post-----------------------------------------------------------


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'

# class PaymentView(APIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

#     def post(self, request, *args, **kwargs):
#         # Calculate the total amount based on the items in the shopping cart
#         total_amount = sum(item.price * item.quantity for item in request.data['items'])

#         # Add the total amount to the payment data
#         request.data['amount'] = total_amount

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# # ----------------------------------------Galley crud -start---------------------------------------------------------

# class GallerySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gallery
#         fields = '__all__'


    

# @permission_classes([IsAuthenticated])
# class GalleryView(APIView):

#     def get(self, request):
#             usr = request.user
#             my_model = usr.gallery_set.all()
#             serializer = GallerySerializer(my_model, many=True)
#             return Response(serializer.data)

#     def post(self, request):
#         # usr =request.user
#         # print(usr)
#         serializer = GallerySerializer(data=request.data, context={'user': request.user})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
#     def put(self, request, pk):
     
#         my_model = Gallery.objects.get(pk=pk)
#         serializer = GallerySerializer(my_model, data=request.data)
#         if os.path.isfile(my_model.image.path):
#             os.remove(my_model.image.path)
#             my_model.delete()
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
#     def delete(self, request, pk):
#         my_model = Gallery.objects.get(pk=pk)
#         if os.path.isfile(my_model.image.path):
#             os.remove(my_model.image.path)
#         my_model.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # Gallery CRUD - end


# # ----------------------------------------Profile crud -start---------------------------------------------------------

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'

    
# @permission_classes([IsAuthenticated])
# class ProfileView(APIView):

#     def get(self, request):
#             usr = request.user
#             my_model = usr.profile_set.all()
#             serializer = ProfileSerializer(my_model, many=True)
#             return Response(serializer.data)

#     def post(self, request):
#         # usr =request.user
#         # print(usr)
#         serializer = ProfileSerializer(data=request.data, context={'user': request.user})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
#     def put(self, request, pk):
#         my_model = Profile.objects.get(pk=pk)
#         serializer = ProfileSerializer(my_model, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

# # Profile CRUD - end


# # ----------------------------------------Albums crud -start---------------------------------------------------------

# class AlbumsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Albums
#         fields = '__all__'

    
# @permission_classes([IsAuthenticated])
# class AlbumsView(APIView):

#     def get(self, request):
#             usr = request.user
#             my_model = usr.albums_set.all()
#             serializer = AlbumsSerializer(my_model, many=True)
#             return Response(serializer.data)
    
# # ----------------------------------------Albums crud -end---------------------------------------------------------

# # ----------------------------------------Albums type crud -start---------------------------------------------------------

# class AlbumsTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AlbumsType
#         fields = '__all__'

    
# @permission_classes([IsAuthenticated])
# class AlbumsTypeView(APIView):

#     def get(self, request):
#             usr = request.user
#             my_model = usr.albumstypes_set.all()
#             serializer = AlbumsTypeSerializer(my_model, many=True)
#             return Response(serializer.data)
    
# ----------------------------------------Albums type crud -end---------------------------------------------------------