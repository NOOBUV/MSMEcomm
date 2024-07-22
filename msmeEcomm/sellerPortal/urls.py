from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('hello/', views.HelloWorldView.as_view(), name='hello-world'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='product')
]
