from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whereandwhenapi.models import Type


class TypeView(ViewSet):
    """Meeting types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single day
        Returns:
            Response -- JSON serialized type instance
        """
        day = Type.objects.get(pk=pk)
        serializer = TypeSerializer(day, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to types resource
        Returns:
            Response -- JSON serialized list of types
        """
        types = Type.objects.all()

        serializer = TypeSerializer(
            types, many=True, context={'request': request})
        return Response(serializer.data)
    
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'