from django.urls import path
from .views import *

urlpatterns = [
    path('upload-file/', upload_inventory, name='upload_inventory'),
    path('merge/', merge_inventory, name='merge_inventory'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
]
