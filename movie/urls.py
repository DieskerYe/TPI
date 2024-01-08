from django.urls import path
from movie.views import index, pagination, movieDetails, genres

urlpatterns = [
    path('', index, name='index'),
    path('search/<query>/page/<page_number>', pagination, name='pagination'),
    path('<imdb_id>', movieDetails, name='movie-details'),
    path('genre/<slug:genre_slug>', genres, name='genres')
]