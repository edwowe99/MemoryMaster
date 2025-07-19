from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),             # ✅ admin once
    path('api/', include('memorise.urls')),      # ✅ app API
]