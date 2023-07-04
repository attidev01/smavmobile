from django.urls import path
from .views import hook_handle

urlpatterns = [
    path('', hook_handle, name='hook')
]
