from django.urls import path, re_path
from django.views.generic.base import RedirectView

from .views import Doc, Search


urlpatterns = [
    path('doc/', Doc.as_view(), name='api-v1-doc'),
    path('search', Search.as_view(), name='api-v1-search'),
    path('search/<resource_type>', Search.as_view(), name='api-v1-search'),
    re_path('^/?$', RedirectView.as_view(url='doc/', permanent=False)),
    ]
