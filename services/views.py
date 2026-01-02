from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Service


# ------------------------------------
# Service List (Catalog)
# ------------------------------------
class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        """
        Return only active services.
        You can later add filters (origin/destination) here.
        """
        return Service.objects.filter(is_active=True)


# ------------------------------------
# Service Detail Page
# ------------------------------------
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'


# ------------------------------------
# Optional: Simple function-based view
# (If you prefer FBVs instead of CBVs)
# ------------------------------------
def service_list_view(request):
    services = Service.objects.filter(is_active=True)
    return render(
        request,
        'services/service_list.html',
        {'services': services}
    )


def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    return render(
        request,
        'services/service_detail.html',
        {'service': service}
    )
