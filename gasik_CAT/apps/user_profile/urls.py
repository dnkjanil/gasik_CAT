from django.urls import path

from gasik_CAT.apps.user_profile.views import user_profile

urlpatterns = [
    path('', user_profile, name='user_profile'),
]