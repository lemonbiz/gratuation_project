from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Movie
# Create your views here.


class viewMovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'view_movie.html'
    paginate_by = 14


# class viewMovieContent()