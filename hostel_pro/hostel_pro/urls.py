"""
URL configuration for hostel_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# hoste_pro/hostel_pro/urls.py
# hostel_pro/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from malnad_app import views as mal_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mal_views.landing, name='landing'),         # combined landing page
    path('any-logout/', mal_views.any_logout, name='any_logout'),
    path('app/', include('malnad_app.urls')),            # all app pages under /app/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
