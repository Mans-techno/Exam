from django.urls import path
from .views import *


urlpatterns = [
    path('brands/', BrandListCreateView.as_view(), name='brand_list_create'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('cars/', CarListCreateView.as_view(), name='car_list_create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('rents/', RentListCreateView.as_view(), name='rent_list_create'),
    path('rents/<int:pk>/', RentDetailView.as_view(), name='rent_detail'),
]
