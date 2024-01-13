from django.urls import path
from movie.views import index, pagination, movieDetails, genres, addMoviesToWatch, addMoviesWatched, Rate

urlpatterns = [
    path('', index, name='index'),
    path('search/<query>/page/<page_number>', pagination, name='pagination'),
    path('<imdb_id>', movieDetails, name='movie-details'),
    path('<imdb_id>/addmoviestowatch', addMoviesToWatch, name='add-movies-to-watch'),
    path('<imdb_id>/addmovieswatched', addMoviesWatched, name='add-movies-watched'),
    path('<imdb_id>/rate', Rate, name='rate-movie'),
    path('genre/<slug:genre_slug>', genres, name='genres')
]