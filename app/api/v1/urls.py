from django.urls import path

from .views import Doc, Search


urlpatterns = [
    path('doc/', Doc.as_view(), name='api-v1-doc'),
    path('search', Search.as_view(), name='api-v1-search'),
    path('search/<resource_type>', Search.as_view(), name='api-v1-search'),
    ]
