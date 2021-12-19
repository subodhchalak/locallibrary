"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import defaultdict
from django.contrib import admin
from django.urls import path
from django.urls import include

from django.views.generic import RedirectView

from django.conf.urls import handler404, handler500

from django.conf.urls.static import static
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest

import catalogApp


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('catalog/', include('catalogApp.urls')),
    
]

urlpatterns += [
    path('', RedirectView.as_view(url='catalog', permanent=True))        # redirecting to new url
]


# enable the serving of static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
   path('accounts/', include('django.contrib.auth.urls')), 
]




handler404 = catalogApp.views.error_404
handler500 = catalogApp.views.error_500




# def page_not_found_handler(request: WSGIRequest, exception=None):
#     if request.path.startswith("/catalog/"):
#         return redirect("catalog:error", error_code=404)
#     elif request.path.startswith("/accounts/"):
#         return redirect("accounts:error", error_code=404)
#     return defaults.page_not_found(request, exception)


# def server_error_handler(request: WSGIRequest):
#     if request.path.startswith("/catalog/"):
#         return redirect("blog:error", error_code=500)
#     elif request.path.startswith("/demo/"):
#         return redirect("demo:error", error_code=500)
#     return defaults.server_error(request)


# handler404 = page_not_found_handler
# handler500 = server_error_handler