from django.urls import path

from .views import HelloView

urlpatterns = [
    path('', HelloView.as_view(), name='index'),
]