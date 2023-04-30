# from base.views.product_views import createProductReview
from base.views.order_views import updateshipping
from base.views.order_views import addshipping
from base.views.order_views import getMyShippinginfo
from base.views.product_views import createProductReview
from base.views.order_views import addOrderItems, getMyOrders, getOrderById, getOrders, updateOrderToDelivered, updateOrderToPaid
from base.views.product_views import ProductView
from base.views.login_views import register
from base.serializers import MyTokenObtainPairView
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('products/', ProductView.as_view() ,name='product_list'),
    path('login/', MyTokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    # admin : not neccessery
    path('getorders', getOrders, name='orders'),
    path('add/', addOrderItems, name='add'),
    path('addshipping/', addshipping, name='addshipping'),
    path('updshipping/', updateshipping, name='updshipping'),

    
    # work
    path('myorders/', getMyOrders, name='myorders'),
    # path('myshippingorders/<str:pk>', getMyShippingAddressbyid, name='myorders'),
    path('myshippinginfo/', getMyShippinginfo, name='shipping-info'),

    path('reviews/', createProductReview, name="create-review"),


    # not checked:
    path('deliver/<str:pk>', updateOrderToDelivered, name='order-delivered'),
    path('getorderbyid/<str:pk>', getOrderById, name='user-order'),
    path('pay/<str:pk>', updateOrderToPaid, name='pay'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
