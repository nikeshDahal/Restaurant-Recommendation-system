from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import RestaurantForm
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from scipy import sparse
import pandas as pd
import numpy as np
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = RestaurantForm()

    return render(request,'basic_app/index.html',{'form': form})

   

    

   
def about(request):
    return render(request,'basic_app/about.html')

def contact(request): 
    return render(request,'basic_app/contact.html')

def resturantList(request): 
    return render(request,'basic_app/sresturantList.html')

def hawa(request): 
    return render(request,'basic_app/hawa.html')

def login(request): 
    return render(request,'basic_app/login.html')

def Menu(request): 
    return render(request,'basic_app/Menu.html')

def signup(request): 
    return render(request,'basic_app/signup.html')

def singleblog(request): 
    return render(request,'basic_app/singleblog.html')


def rest(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = RestaurantForm()

    return render(request,'basic_app/index.html',{'form': form})

def show(request):
    inp = [request.GET.get('title')]
    inp1 = request.GET.get('location')
    inp2 = request.GET.get('index')
    inp.append(inp1)
    inp.append(inp2)
    print(inp)


    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('restaurant.csv')
    ratings = pd.merge(movies, ratings).drop(['city'], axis=1)
    (ratings.shape)
    (ratings.head())
    userRatings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')
    userRatings.head()
    ("Before: ", userRatings.shape)
    userRatings = userRatings.dropna(thresh=10, axis=0).fillna(0, axis=0)
    # userRatings.fillna(0, inplace=True)
    ("After: ", userRatings.shape)

    corrMatrix = userRatings.corr(method='pearson')
    (corrMatrix.head(100))

    def get_similar(movie_name,location,rating):
        similar_ratings = corrMatrix[movie_name]*(rating-2.5)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        #print(type(similar_ratings))
        return similar_ratings

    romantic_lover = inp
    similar_movies = pd.DataFrame()
    for movie,location,rating in romantic_lover:
        similar_movies = similar_movies.append(get_similar(movie,location,rating),ignore_index = True)

    (similar_movies.head(10))
    (similar_movies.sum().sort_values(ascending=False).head(10))
        
        
    action_lover = inp
    similar_movies = pd.DataFrame()
    for movie,location,rating in action_lover:
        similar_movies = similar_movies.append(get_similar(movie,location,rating),ignore_index = True)
    
    similar_movies.head(5)
    ####################################################
    restaurants_list = [(similar_movies.sum().sort_values(ascending=False).head(10))]

  #to show o/p in frontend .

    return render(request,"basic_app/index.html",{'restaurants':restaurants_list})

    #return HttpResponse('jpt')
