from rest_framework import serializers
from .models import SpyCat
import requests
from django.conf import settings

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_breed(self, value):
        # validate breed thacatapi
        try:
            response = requests.get(settings.CAT_API_URL, timeout=5)
            response.raise_for_status()
            breeds = response.json()
            breed_names = [breed['name'].lower() for breed in breeds]
            
            if value.lower() not in breed_names:
                raise serializers.ValidationError(
                    f"Breed '{value}' is not valid. Please check TheCatAPI for valid breeds."
                )
            return value
        except requests.RequestException as e:
            raise serializers.ValidationError(f"Error validating breed: {str(e)}")
        
class SpyCatUpdateSerializer(serializers.ModelSerializer):
    # only salary can be updated
    class Meta:
        model = SpyCat
        fields = ['salary']