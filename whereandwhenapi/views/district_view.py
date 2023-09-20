from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from whereandwhenapi.models import District

class HomepageDistrictPermission(permissions.BasePermission):
    """Homepage District permissions"""

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'search']:
            return True  # Allow all actions for authenticated users
        elif request.user.is_authenticated:
            return True  # Allow retrieve and list for anonymous users
        else:
            return False

class DistrictView(ViewSet):
    """Districts"""

    permission_classes = (HomepageDistrictPermission, IsAuthenticatedOrReadOnly)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single district
        Returns:
            Response -- JSON serialized district instance
        """
        district = District.objects.get(pk=pk)
        serializer = DistrictSerializer(district, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to districts resource
        Returns:
            Response -- JSON serialized list of districts
        """
        districts = District.objects.all()

        serializer = DistrictSerializer(
            districts, many=True, context={'request': request})
        return Response(serializer.data)
    
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'