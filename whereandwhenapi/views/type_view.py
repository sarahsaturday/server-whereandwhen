from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from whereandwhenapi.models import Type

class HomepageTypePermission(permissions.BasePermission):
    """Homepage Type permissions"""

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'search']:
            return True  # Allow all actions for authenticated users
        elif request.user.is_authenticated:
            return True  # Allow retrieve and list for anonymous users
        else:
            return False
        
class TypeView(ViewSet):
    """Meeting types"""

    permission_classes = (HomepageTypePermission, IsAuthenticatedOrReadOnly)

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