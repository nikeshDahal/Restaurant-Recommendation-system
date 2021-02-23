from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import RestaurantForm
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
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
    return render(request,'basic_app/resturantList.html')

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

    return render(request,'basic_app/resturantList.html',{'form': form})

def show(request):
    print('DEBUG')
    #restaurants = Restaurant.objects.all()
    inp = request.GET.get('title')
    from pprint import pprint
    #pprint(vars(restaurants[0]))
    # filtered = pd.DataFrame.from_records(restaurants)
    # print(filtered)
    df = pd.DataFrame(list(Restaurant.objects.all().values('id','city','title','location','index')))
    #print(df.to_string())
    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]


    def get_index_from_title(title):
        return df[df.title == title]["index"].values[0]


    ##################################################


    # Step 1: Read CSV File


    #####


    # df = pd.read_sql_query("select * from restaurant1;", db.connection_obj_db)
    # ##pd.read_sql_table('restaurant - 2', 'postgres:///test')


    # df = fetched_data
    # print df.columns
    # Step 2: Select Features

    features = ['location','city']
    # Step 3: Create a column in DF which combines all selected features
    for feature in features:
        df[feature] = df[feature].fillna('')


    def combine_features(row):
        try:
            return  row['location'] + " " + row['city']
        except:
            print("Error:", row)


    df["combined_features"] = df.apply(combine_features, axis=1)

    # print "Combined Features:", df["combined_features"].head()

    # Step 4: Create count matrix from this new combined column
    cv = CountVectorizer()

    count_matrix = cv.fit_transform(df["combined_features"])

    # Step 5: Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix)
    movie_user_likes = inp

    # Step 6: Get index of this movie from its title
    movie_index = get_index_from_title(movie_user_likes)

    similar_movies = list(enumerate(cosine_sim[int(movie_index)]))

    # Step 7: Get a list of similar movies in descending order of similarity score
    sorted_similar_movies = sorted(
        similar_movies, key=lambda x: x[1], reverse=True)

    # Step 8: Print titles of first 50 movies
    i = 0
    # a list to hold recommended restros
    restaurants_list = []
    for element in sorted_similar_movies:
        print(get_title_from_index(element[0]))
        
        restaurants_list.append(get_title_from_index(element[0]))
        #restaurants = get_title_from_index(element[0])

        i = i + 1
        if i > 5:
            break
    # print("THis is ", restaurants)
    print("This is my recommendation", restaurants_list)
    # restaurant_list is passed as context named 'restaurants'
    return render(request,"basic_app/resturantList.html",{'restaurants':restaurants_list})

    #return HttpResponse('jpt')
