from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import  ListCreateAPIView
from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer
from .permissions import IsStaffOrReadOnly
from django.db.models import Q


class CarView(ModelViewSet):
    queryset= Car.objects.all()
    serializer_class = CarSerializer 
    permission_classes = [IsStaffOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
             queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(availability = True)
        
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        
        cond1 = Q(start_date__lt=end_date)
        cond2 = Q(end_date__gt=start_date)
        # not_available = Reservation.objects.filter(
        #     start_date__lt=end, end_date__gt=start
        # ).values_list('car_id', flat=True)  # [1, 2]

        not_available = Reservation.objects.filter(
            cond1 & cond2
        ).values_list('car_id', flat=True)  # [1, 2]
        print(not_available)

        queryset = queryset.exclude(id__in=not_available)

        
        return queryset
    
    
class ReservationView(ListCreateAPIView):
    
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer