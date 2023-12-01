from django.urls import path
from films import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("films/", views.FilmList.as_view(), name="film-list")
]


htmx_urlpatterns = [
    path("check_username/", views.check_username, name="check-username"),
    path("add_film/", views.addFilm, name="add-film"),
    path("delete_film/<int:pk>", views.deleteFilm, name="delete-film"),
    path("search_film/", views.searchFilm, name="search-film"),
    path("clear/", views.clear, name="clear"),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('film-list-partial', views.films_partial, name='film-list-partial'),

]

urlpatterns += htmx_urlpatterns