from rest_framework import serializers
from .models import Mission, Target
from cats.serializers import SpyCatSerializer


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_complete']
        read_only_fields = ['id']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=True)
    cat = SpyCatSerializer(read_only=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'targets', 'is_complete', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MissionCreateSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, write_only=True)

    class Meta:
        model = Mission
        fields = ['targets']

    def validate_targets(self, value):
        if len(value) < 1 or len(value) > 3:
            raise serializers.ValidationError("Mission must have between 1 and 3 targets")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['notes', 'is_complete']

    def validate(self, data):
        target = self.instance
        
        # Check if trying to update notes
        if 'notes' in data and data['notes'] != target.notes:
            if target.is_complete:
                raise serializers.ValidationError("Cannot update notes: target is already complete")
            if target.mission.is_complete:
                raise serializers.ValidationError("Cannot update notes: mission is already complete")
        
        return data