from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import make_aware, is_aware
from django.utils.dateparse import parse_datetime

from payments.models import Payment
from payments.api.serializers import PaymentSerializer

class PaymentApiViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['table', 'statusPayment']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener fechas de la solicitud
        date_range = self.request.query_params.get('created_at__range', '').split(',')
        start_date = date_range[0] if date_range else None
        end_date = date_range[1] if len(date_range) > 1 else None

        print(f"Start Date: {start_date}, End Date: {end_date}")

        # Aplicar el filtro solo si ambas fechas están presentes
        if start_date and end_date:
            # Convertir las fechas a objetos datetime
            start_datetime = parse_datetime(start_date)
            end_datetime = parse_datetime(end_date)

            # Asegurarse de que las fechas sean objetos datetime y aplicar la zona horaria si es necesario
            if start_datetime:
                start_date_utc = make_aware(start_datetime) if not is_aware(start_datetime) else start_datetime
            else:
                start_date_utc = None

            if end_datetime:
                end_date_utc = make_aware(end_datetime) if not is_aware(end_datetime) else end_datetime
            else:
                end_date_utc = None

            print(f"Start Date (UTC): {start_date_utc}, End Date (UTC): {end_date_utc}")

            # Aplicar el filtro
            if start_date_utc and end_date_utc:
                queryset = queryset.filter(created_at__range=(start_date_utc, end_date_utc))

        return queryset
