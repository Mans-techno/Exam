from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Brand, Car, Rent
from .serializers import BrandSerializer, CarSerializer, RentSerializer


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.select_related('brand_id').order_by('-created_at')
    serializer_class = CarSerializer


class CarDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class RentListCreateView(ListCreateAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class RentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
