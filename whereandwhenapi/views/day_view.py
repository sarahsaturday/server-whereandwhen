from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whereandwhenapi.models import Day


class DayView(ViewSet):
    """Days of the week"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single day
        Returns:
            Response -- JSON serialized day instance
        """
        day = Day.objects.get(pk=pk)
        serializer = DaySerializer(day, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to days resource
        Returns:
            Response -- JSON serialized list of days
        """
        days = Day.objects.all()

        serializer = DaySerializer(
            days, many=True, context={'request': request})
        return Response(serializer.data)
    
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'