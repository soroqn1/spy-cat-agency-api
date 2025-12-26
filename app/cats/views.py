from rest_framework import viewsets
from .models import SpyCat
from .serializers import SpyCatSerializer, SpyCatUpdateSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return SpyCatUpdateSerializer
        return super().get_serializer_class()