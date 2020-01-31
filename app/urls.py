from django.urls import path
from .views import HomePageView, AboutPageView, MunicipalitiesListView, SeimasPageView, GovPageView, PresidentPageView, MunicipalityPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('apie-mus/', AboutPageView.as_view(), name='about'),
    path('savivaldybes/', MunicipalitiesListView.as_view(), name='municipalities'),
    path('vyriausybe/', GovPageView.as_view(), name='gov'),
    path('seimas/', SeimasPageView.as_view(), name='seimas'),
    path('prezidentura/', PresidentPageView.as_view(), name='president'),
    path('savivaldybes/<str:slug>', MunicipalityPageView.as_view(), name='municipality')
]