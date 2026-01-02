from django.urls import path
from .views import ServiceListView, ServiceDetailView

app_name = 'services'

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
]
