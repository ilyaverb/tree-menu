from django.urls import re_path

from tree_menu.menu.views import MenuView

urlpatterns = [
    re_path(r'^$', MenuView.as_view(), name='index'),
    re_path(r'^(.*)/$', MenuView.as_view(), name='index'),
]
