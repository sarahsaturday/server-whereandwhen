from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from datetime import time
from django.db.models import F, OuterRef, Subquery
from django.db.models import Prefetch
from whereandwhenapi.models import Meeting, MeetingDay, GroupRep, GroupRepMeeting, Day


class HomepagePermission(permissions.BasePermission):
    """Homepage permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True  # Allow all actions for authenticated users
        elif view.action in ['retrieve', 'list', 'search']:
            return True  # Allow retrieve and list for anonymous users
        else:
            return False

class MeetingView(ViewSet):
    """Where and When Meetings"""

    permission_classes = (HomepagePermission,)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meeting
        Returns:
            Response -- JSON serialized meeting instance
        """
        meeting = Meeting.objects.get(pk=pk)
        serializer = MeetingSerializer(meeting, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to meetings resource
        Returns:
            Response -- JSON serialized list of meetings
        """
        # Subquery to get the latest day for each meeting
        latest_day_subquery = MeetingDay.objects.filter(
            meeting=OuterRef('pk')).order_by('-day').values('day')[:1]

        # Annotate the Meeting queryset with the latest day
        meetings = Meeting.objects.annotate(
            latest_day=Subquery(latest_day_subquery))

        # Order by the latest_day and then start_time
        meetings = meetings.order_by('latest_day', 'start_time')

        serializer = MeetingSerializer(
            meetings, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized meeting instance
        """

        # Extract the list of day IDs and group rep IDs from the request data
        day_ids = request.data.get("days", [])
        group_rep_ids = request.data.get("group_reps", [])

        # Remove 'days' and 'group_reps' from the request data
        request_data = request.data.copy()
        request_data.pop("days", None)
        request_data.pop("group_reps", None)

        new_meeting = Meeting()
        new_meeting.wso_id = request.data["wso_id"]
        new_meeting.district_id = request.data["district"]
        new_meeting.area_id = request.data["area"]
        new_meeting.meeting_name = request.data["meeting_name"]
        new_meeting.start_time = request.data["start_time"]
        new_meeting.street_address = request.data["street_address"]
        new_meeting.city = request.data["city"]
        new_meeting.zip = request.data["zip"]
        new_meeting.location_details = request.data["location_details"]
        new_meeting.type_id = request.data["type"]
        new_meeting.zoom_login = request.data.get("zoom_login")
        new_meeting.zoom_pass = request.data.get("zoom_pass")
        new_meeting.email = request.data.get("email")
        new_meeting.phone = request.data.get("phone")
        new_meeting.save()

        # Add the days and group reps to the new meeting instance
        new_meeting.days.set(day_ids)

        user = request.user 
        GroupRepMeeting.objects.create(
            group_rep=user,
            meeting=new_meeting,
            is_home_group=False  # Default to False
        )
        for group_rep_data in group_rep_ids:
            group_rep_id = group_rep_data["id"]
            # Default to False if not provided
            is_home_group = group_rep_data.get("is_home_group", False)
            GroupRepMeeting.objects.create(
                group_rep_id=group_rep_id,
                meeting=new_meeting,
                is_home_group=is_home_group
            )

        serializer = MeetingSerializer(
            new_meeting, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a meeting"""
        meeting = Meeting.objects.get(pk=pk)
        request_data = request.data

        meeting.wso_id = request.data["wso_id"]
        meeting.district_id = request.data["district"]
        meeting.area_id = request.data["area"]
        meeting.meeting_name = request.data["meeting_name"]
        meeting.start_time = request.data["start_time"]
        meeting.street_address = request.data["street_address"]
        meeting.city = request.data["city"]
        meeting.zip = request.data["zip"]
        meeting.location_details = request.data["location_details"]
        meeting.type_id = request.data["type"]
        meeting.zoom_login = request.data.get("zoom_login")
        meeting.zoom_pass = request.data.get("zoom_pass")
        meeting.email = request.data.get("email")
        meeting.phone = request.data.get("phone")

        # Update associated days
        if "days" in request_data:
            meeting.days.clear()  # Remove existing associations
            days = Day.objects.filter(pk__in=request_data["days"])
            meeting.days.add(*days)

        # Update associated group reps
        if "group_reps" in request_data:
            # Remove existing GroupRepMeeting associations for this meeting
            GroupRepMeeting.objects.filter(meeting=meeting).delete()

            # Add the new group rep associations with is_home_group information
            group_reps_data = request_data["group_reps"]
            for group_rep_data in group_reps_data:
                group_rep_id = group_rep_data["id"]
                # Default to False if not provided
                is_home_group = group_rep_data.get("is_home_group", False)
                GroupRepMeeting.objects.create(
                    group_rep_id=group_rep_id,
                    meeting=meeting,
                    is_home_group=is_home_group
                )

        meeting.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a meeting"""
        meeting = Meeting.objects.get(pk=pk)
        meeting.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy_meeting_day(self, request, pk=None, meeting_day_id=None):
    #     """
    #     Custom action to delete a MeetingDay record associated with a Meeting.
    #     """
    #     # Ensure that the MeetingDay record exists and is associated with the specified Meeting
    #     meeting_day = get_object_or_404(MeetingDay, pk=meeting_day_id, meeting__pk=pk)

    #     # Now you can safely delete the MeetingDay record
    #     meeting_day.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def search(self, request):
        """Handle GET requests to search meetings based on parameters"""
        # Create an instance of the MeetingSearchSerializer with request.GET data
        serializer = MeetingSearchSerializer(data=request.GET)

        # Validate the serializer
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated search parameters from the serializer
        validated_data = serializer.validated_data
        day = validated_data.get('day')
        meeting_name = validated_data.get('meeting_name')
        meeting_type = validated_data.get('type')
        zip_code = validated_data.get('zip')
        city = validated_data.get('city')
        start_time = validated_data.get('start_time')

        # Use the search parameters to filter meetings
        queryset = Meeting.objects.all()

        if day:
            queryset = queryset.filter(meetingday__day__day=day)

        # if start_time:
        #     try:
        #         # Parse the time string into a Time object
        #         parsed_time = time.fromisoformat(start_time)
        #         queryset = queryset.filter(start_time=parsed_time)
        #     except ValueError:
        #         pass

        if meeting_name:
            queryset = queryset.filter(meeting_name__icontains=meeting_name)

        if meeting_type:
            queryset = queryset.filter(type=meeting_type)

        if zip_code:
            queryset = queryset.filter(zip=zip_code)

        if city:
            queryset = queryset.filter(city__icontains=city)

        if start_time:
            queryset = queryset.filter(start_time=start_time)

        # Serialize the filtered meetings and return the response
        serializer = MeetingSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class MeetingSerializer(serializers.ModelSerializer):
    """JSON serializer for meetings"""

    class Meta:
        model = Meeting
        fields = (
            'id',
            'wso_id',
            'district',
            'area',
            'meeting_name',
            'start_time',
            'street_address',
            'city',
            'zip',
            'location_details',
            'type',
            'zoom_login',
            'zoom_pass',
            'email',
            'phone',
            'last_updated',
            'days',
            'group_reps'
        )


class MeetingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingDay
        fields = '__all__'


class GroupRepSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRep
        fields = '__all__'


class MeetingSearchSerializer(serializers.Serializer):
    day = serializers.CharField(required=False)
    meeting_name = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    zip = serializers.IntegerField(required=False)
    city = serializers.CharField(required=False)
    start_time = serializers.TimeField(required=False)
