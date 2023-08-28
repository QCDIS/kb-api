from django.urls import re_path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(r'^v1/', include('api.v1.urls'), name='v1'),
    re_path('^/?$', RedirectView.as_view(url='v1/', permanent=False)),
    ]
