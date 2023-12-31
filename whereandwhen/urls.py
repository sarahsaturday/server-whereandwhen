from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from whereandwhenapi.views import register_user, login_user, MeetingView, DayView, TypeView, GroupRepView, AreaView, DistrictView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'meetings', MeetingView, 'meeting')
router.register(r'days', DayView, 'day')
router.register(r'types', TypeView, 'type')
router.register(r'groupreps', GroupRepView, 'grouprep')
router.register(r'areas', AreaView, 'area')
router.register(r'districts', DistrictView, 'district')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'search/', MeetingView.as_view({'get': 'search'}), name='meeting-search'),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]
