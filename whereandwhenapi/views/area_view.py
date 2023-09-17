from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whereandwhenapi.models import Area


class AreaView(ViewSet):
    """Areas"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single area
        Returns:
            Response -- JSON serialized area instance
        """
        area = Area.objects.get(pk=pk)
        serializer = AreaSerializer(area, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to areas resource
        Returns:
            Response -- JSON serialized list of areas
        """
        areas = Area.objects.all()

        serializer = AreaSerializer(
            areas, many=True, context={'request': request})
        return Response(serializer.data)
    
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'