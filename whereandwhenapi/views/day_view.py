from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from whereandwhenapi.models import Day


class HomepageDayPermission(permissions.BasePermission):
    """Homepage Day permissions"""

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'search']:
            return True  # Allow all actions for authenticated users
        elif request.user.is_authenticated:
            return True  # Allow retrieve and list for anonymous users
        else:
            return False


class DayView(ViewSet):
    """Days of the week"""

    permission_classes = (HomepageDayPermission, IsAuthenticatedOrReadOnly)

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