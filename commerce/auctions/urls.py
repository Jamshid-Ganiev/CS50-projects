from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create", views.create_listing, name='create_listing'),
    path("<int:listing_id>", views.listing_details, name='details'),
    path("watchlist/toggle/<int:item_id>/", views.toggle_watchlist, name='toggle_watchlist'),
    path("watchlist/", views.view_watchlist, name='watchlist'),
    path("categories/", views.view_categories, name='categories'),
    path("categories/<int:category_id>", views.view_category, name='category')
]
