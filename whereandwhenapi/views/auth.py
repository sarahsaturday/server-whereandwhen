from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime
from whereandwhenapi.models import GroupRep

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user'''

    email = request.data['email']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=email, password=password)
    print(authenticated_user)
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        user = GroupRep.objects.get(user_id=authenticated_user)
        data = { 'valid': True, 'token': token.key, 'user': int(user.id) }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)

def register_user(request):
    '''Handles the creation of a new user for authentication'''

    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)
    phone = request.data.get('phone', None)
    is_staff = request.data.get('is_staff', False)
    is_group_rep = request.data.get('is_group_rep', False)
    is_isr = request.data.get('is_isr', False)

    if (
        email is not None
        and first_name is not None
        and last_name is not None
        and password is not None
    ):
        try:
            # Create a new user by invoking the `create_user` helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff
            )

            # If the user is a group representative, create a GroupRep instance
            if is_group_rep:
                GroupRep.objects.create(
                    user=new_user,
                    is_group_rep=True,
                    is_isr=is_isr,
                    phone=phone
                    # Add any additional fields related to GroupRep here
                )

        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)
        # Return the token to the client
        data = { 'token': token.key, 'staff': new_user.is_staff }
        return Response(data)

    return Response(
        {'message': 'Oops, you missed a spot!'},
        status=status.HTTP_400_BAD_REQUEST
    )