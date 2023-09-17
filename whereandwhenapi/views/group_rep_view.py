from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whereandwhenapi.models import GroupRep


class GroupRepView(ViewSet):
    """Group Reps"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single group rep
        Returns:
            Response -- JSON serialized group rep instance
        """
        group_rep = GroupRep.objects.get(pk=pk)
        serializer = GroupRepSerializer(group_rep, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to group reps resource
        Returns:
            Response -- JSON serialized list of group_reps
        """
        group_reps = GroupRep.objects.all()

        serializer = GroupRepSerializer(
            group_reps, many=True, context={'request': request})
        return Response(serializer.data)
    
class GroupRepSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRep
        fields = '__all__'