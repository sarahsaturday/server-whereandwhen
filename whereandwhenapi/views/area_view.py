from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from whereandwhenapi.models import Area

class HomepageAreaPermission(permissions.BasePermission):
    """Homepage Area permissions"""

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'search']:
            return True  # Allow all actions for authenticated users
        elif request.user.is_authenticated:
            return True  # Allow retrieve and list for anonymous users
        else:
            return False

class AreaView(ViewSet):
    """Areas"""

    permission_classes = (HomepageAreaPermission, IsAuthenticatedOrReadOnly)

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