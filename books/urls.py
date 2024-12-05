from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('add_book/', views.add_book, name='add_book'),
    path('recommend/<int:book_id>/', views.recommend, name='recommend'),
    path('recommended/', views.recommended_books, name='recommended_books'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
