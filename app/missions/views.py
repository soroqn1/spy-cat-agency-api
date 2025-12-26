from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mission, Target
from .serializers import MissionSerializer, MissionCreateSerializer, TargetUpdateSerializer
from cats.models import SpyCat


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MissionCreateSerializer
        return MissionSerializer
    
    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        
        if mission.cat is not None:
            return Response(
                {"error": "Cannot delete mission that is assigned to a cat"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)