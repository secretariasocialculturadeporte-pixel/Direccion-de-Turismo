from django.urls import path
from .views import (
    AdminPrestadorListView,
    AdminApprovePrestadorView,
)

urlpatterns = [
    path('prestadores/', AdminPrestadorListView.as_view(), name='admin-prestadores-list'),
    path('prestadores/<int:pk>/approve/', AdminApprovePrestadorView.as_view(), name='admin-prestador-approve'),
]