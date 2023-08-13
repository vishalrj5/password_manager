"""password_management URL Configuration

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
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Password Management API",
      default_version='v1',
      description="Initial Django Project",
      contact=openapi.Contact(email="vishal@aventusinformatics.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    
    
    
    
    path('admin/', admin.site.urls),
    path('users/',include('apps.users.urls')),
    path('auth/',include('apps.authentication.urls')),
    path('passwords/',include('apps.passwords.urls')),
    path('', include('apps.home.urls')),
    
    
    
    
    
    re_path(r'^api/', include([
        
        path('auth/',include('apps.authentication.api.urls')),   
        
        path('passwords/',include('apps.passwords.api.urls')), 
    
        re_path(r'^docs/', include([

            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path("redoc", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        ])),    
    ])),    
     
        
    
]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
