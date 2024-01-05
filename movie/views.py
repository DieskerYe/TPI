from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.text import slugify
from movie.models import Movie, Genre, Rating
from actor.models import Actor
import requests


# Create your views here.
def index(request):
    query = request.GET.get('q')

    if query:
        url = 'http://www.omdbapi.com/?apikey=ff4e1a0f&s=' + query
        response = requests.get(url)
        movie_data = response.json()

        context = {
            'query': query,
            'movie_data': movie_data,
            'page_number': 1
        }

        template = loader.get_template('search_results.html')

        return HttpResponse(template.render(context, request))
    return render(request, 'index.html')


def pagination(request, query, page_number):
    url = 'http://www.omdbapi.com/?apikey=ff4e1a0f&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1

    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number
    }

    template = loader.get_template('search_results.html')

    return HttpResponse(template.render(context, request))

def movieDetails(request, imdb_id):
    if Movie.objects.filter(imdb_id=imdb_id).exists():
        movie_data = Movie.objects.get(imdbid=imdb_id)
        db = True
    else:
        url = 'http://www.omdbapi.com/?apikey=ff4e1a0f&s=' + imdb_id
        response = requests.get(url)
        movie_data = response.json()

        #inject to our database bellow:

        rating_objs = []
        genre_objs = []
        actor_objs = []

        #For the actors
        actor_list = [i.strip() for i in movie_data['Actors'].split(',')]

        for actor in actor_list:
            a, created = Actor.objects.get_or_create(name=actor)
            actor_objs.append(a)

        #For the Genre or categories
        genre_list = list(movie_data['Genre'].replace(" ", "").split(','))

        for genre in genre_list:
            genre_slug = slugify(genre)
            g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
            genre_objs.append(g)

        #For the rate
        for rate in movie_data['Ratings']:
            r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
            rating_objs.append(r)

        if movie_data['Type'] == 'movie':
            m, created = Movie.objects.get_or_create(
                title=movie_data['Title'],
                year=movie_data['Year'],
                rated=movie_data['Rated'],
                released=movie_data['Released'],
                runtime=movie_data['Runtime'],
                director=movie_data['Director'],
                writer=movie_data['Writer'],
                plot=movie_data['Plot'],
                language=movie_data['Language'],
                country=movie_data['Country'],
                awards=movie_data['Awards'],
                poster_url=movie_data['Poster'],
                metascore=movie_data['Metascore'],
                imdb_rating=movie_data['imdbRating'],
                imdb_votes=movie_data['imdbVotes'],
                imdb_id=movie_data['imdbID'],
                type=movie_data['Type'],
                dvd=movie_data['DVD'],
                box_office=movie_data['BoxOffice'],
                production=movie_data['Production'],
                website=movie_data['Website'],
            )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(rating_objs)
        else:
            m, created = Movie.objects.get_or_create(
                title=movie_data['Title'],
                year=movie_data['Year'],
                rated=movie_data['Rated'],
                released=movie_data['Released'],
                runtime=movie_data['Runtime'],
                director=movie_data['Director'],
                writer=movie_data['Writer'],
                plot=movie_data['Plot'],
                language=movie_data['Language'],
                country=movie_data['Country'],
                awards=movie_data['Awards'],
                poster_url=movie_data['Poster'],
                metascore=movie_data['Metascore'],
                imdb_rating=movie_data['imdbRating'],
                imdb_votes=movie_data['imdbVotes'],
                imdb_id=movie_data['imdbID'],
                type=movie_data['Type'],
                totalSeasons=movie_data['totalSeasons'],
            )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(rating_objs)

        for actor in actor_objs:
            actor.movies.add(m)
            actor.save()

        m.save()
        db = False

    context = {
        'movie_data': movie_data,
        'db': db
    }

    template = loader.get_template('movie_details.html')

    return HttpResponse(template.render(context, request))
