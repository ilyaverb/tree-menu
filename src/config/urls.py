from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('menu/', include('tree_menu.menu.urls')),
    path('admin/', admin.site.urls),
]
