from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create", views.create_listing, name='create_listing'),
    path("<int:auction_id>", views.listing_details, name='details'),
    path("watchlist/toggle/<int:item_id>/", views.toggle_watchlist, name='toggle_watchlist'),
    path("watchlist/", views.view_watchlist, name='watchlist'),
    path("categories/", views.view_categories, name='categories'),
    path("categories/<int:category_id>", views.view_category, name='category'),
    path('create_comment/<int:auction_id>', views.create_comment, name='create_comment'),
    path('delete_comment/<int:auction_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:auction_id>/<int:comment_id>', views.edit_comment, name='edit_comment'),
]
