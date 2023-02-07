from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<str:TITLE>', views.get_title, name='get_title'),
    path('search', views.search_results, name='search_results'),
    path('new_page', views.create_entry, name='create_entry'),
    path('edit_entry/<str:title>', views.edit_entry, name='edit_entry'),
    path('random_entry/', views.random, name='random')
]
