from django.urls import path
from gasik_CAT.apps.authenticate.views import user_login, user_logout, admin_login

urlpatterns = [
    path('login', user_login, name='user_login'),
    path('login/admin', admin_login, name='admin_login'),
    path('logout', user_logout, name='user_logout')
]
