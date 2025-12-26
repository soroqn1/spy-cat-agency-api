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
            return Response({"error": "Cannot delete mission that is assigned to a cat"},status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None): # assign a cat to the mission
        mission = self.get_object()
        cat_id = request.data.get('cat_id')
        
        if not cat_id:
            return Response({"error": "cat_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return Response({"error": "Cat not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if Mission.objects.filter(cat=cat, is_complete=False).exists():
            return Response({"error": "Cat already has an active mission"}, status=status.HTTP_400_BAD_REQUEST)
        
        mission.cat = cat
        mission.save()
        
        serializer = self.get_serializer(mission)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], url_path='targets/(?P<target_id>[^/.]+)')
    def update_target(self, request, pk=None, target_id=None): # update a specific target within the mission
        mission = self.get_object()
        
        try:
            target = mission.targets.get(id=target_id)
        except Target.DoesNotExist:
            return Response({"error": "Target not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TargetUpdateSerializer(target, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            if all(t.is_complete for t in mission.targets.all()):
                mission.is_complete = True
                mission.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)