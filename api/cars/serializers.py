from api.cars.models import Car
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

    def validate_name(self, value):
        if Car.objects.filter(name=value).exists():
            raise serializers.ValidationError("This name is already taken.")
        return value
