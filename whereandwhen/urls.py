from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from whereandwhenapi.views import register_user, login_user, MeetingView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'meetings', MeetingView, 'meeting')

urlpatterns = [
path('', MeetingView.as_view({'get': 'list'}), name='meeting-list'),
path('register', register_user),
path('login', login_user),
path('admin/', admin.site.urls),
]
