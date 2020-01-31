from django.shortcuts import render
from django.views.generic import View, ListView
from app.models import Region, Municipality

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class AboutPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')

class MunicipalitiesListView(ListView):
    context_object_name = 'municipalities'
    queryset = Municipality.objects.all()
    template_name = 'municipalities.html'

class SeimasPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'seimas.html')

class GovPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'gov.html')

class PresidentPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'president.html')

class MunicipalityPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'municipality.html')