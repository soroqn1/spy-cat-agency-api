from rest_framework import viewsets
from .models import SpyCat
from .serializers import SpyCatSerializer, SpyCatUpdateSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SpyCatUpdateSerializer
        return SpyCatSerializer