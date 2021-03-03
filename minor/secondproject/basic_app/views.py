from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .models import userreg
from .forms import RestaurantForm
from django.contrib import messages
from .forms import  loginForm
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

    return render(request, 'basic_app/index.html', {'form': form})

def userregistration(request, saverecord=None):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('pwd'):
            saverecord=userreg()
            saverecord.username = request.POST.get('username')
            saverecord.pwd = request.POST.get('pwd')
            saverecord.save()
            messages.success(request,"New user registered sucessfully")
            return render(request,'basic_app/signup.html')
    else:
            return render(request,'basic_app/signup.html')





def about(request):
    return render(request, 'basic_app/about.html')


def contact(request):
    return render(request, 'basic_app/contact.html')


def resturantList(request):
    return render(request, 'basic_app/resturantList.html')


def hawa(request):
    return render(request, 'basic_app/hawa.html')


def login(request):

    return render(request, 'basic_app/login.html')


def Menu(request):
    return render(request, 'basic_app/Menu.html')


def signup(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = loginForm()

    return render(request, 'basic_app/signup.html', {'form': form})


def singleblog(request):
    return render(request, 'basic_app/singleblog.html')


# def rest(request):
#     if request.method == 'POST':
#         form = RestaurantForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/')
#             except:
#                 pass
#     else:
#         form = RestaurantForm()
#
#     return render(request, 'basic_app/resturantList.html', {'form': form})

global is_res_present


def show(request):
    print('DEBUG')
    # restaurants = Restaurant.objects.all()
    inp = request.GET.get('title').lower()
    inp2 = request.GET.get('location').lower()
    from pprint import pprint
    # pprint(vars(restaurants[0]))
    # filtered = pd.DataFrame.from_records(restaurants)
    # print(filtered)
    df = pd.DataFrame(list(Restaurant.objects.all().values('id', 'city', 'title', 'location', 'index')))

    try:
        is_res_present=df[df.title == inp]["index"].values[0]
    except:
        is_res_present=''


    if is_res_present!='':
        # print(df.to_string())
        def get_title_from_index(index):
            # print("Printing from get_titl e_from_index")
            # print(df[df.index == index]["title"].values[0])
            return df[df.index == index]["title"].values[0]

        def get_index_from_title(title,location):
            a = df[df.title == title]["index"]
            b= df[df.location == location]["index"]
            cap=0
            for af in a :
                for bf in b:
                    if (af == bf):
                        cap=af
            return cap

        def get_location_from_index(index):
                # print("Printing from get_titl e_from_index")
                # print(df[df.index == index]["title"].values[0])
            return df[df.index == index]["location"].values[0]


                # return 2

            # else:
            #     print(df.head, "shape is")

                # return 1

        ##################################################

        # Step 1: Read CSV File

        #####

        # df = pd.read_sql_query("select * from restaurant1;", db.connection_obj_db)
        # ##pd.read_sql_table('restaurant - 2', 'postgres:///test')

        # df = fetched_data
        # print df.columns
        # Step 2: Select Features

        features = ['location', 'city']
        # Step 3: Create a column in DF which combines all selected features
        for feature in features:
            df[feature] = df[feature].fillna('')

        def combine_features(row):
            try:
                return row['location'] + " " + row['city']
            except:
                print("Error:", row)

        df["combined_features"] = df.apply(combine_features, axis=1)

        # print "Combined Features:", df["combined_features"].head()

        # Step 4: Create count matrix from this new combined column
        cv = CountVectorizer()

        count_matrix = cv.fit_transform(df["combined_features"])

        # Step 5: Compute the Cosine Similarity based on the count_matrix
        cosine_sim = cosine_similarity(count_matrix)
        restaurants_user_types = inp
        location_user_types = inp2
        # movie_user_likes

        # Step 6: Get index of this movie from its title
        restaurants_index = get_index_from_title(restaurants_user_types,location_user_types)
        # print("Printing movie index")
        # print(movie_index)

        similar_restaurants = list(enumerate(cosine_sim[int(restaurants_index)]))
        # print("Printing Similar Movies")
        # print(similar_movies)

        # Step 7: Get a list of similar movies in descending order of similarity score
        sorted_similar_restaurants = sorted(
            similar_restaurants, key=lambda x: x[1], reverse=True)

        # print("Printing Sorted_Similar movies")
        # print(sorted_similar_movies)
        # Step 8: Print titles of first 50 movies
        i = 0
        # a list to hold recommended restros
        restaurants_list = []
        restaurants_loc = []

        for element in sorted_similar_restaurants:
            # print(get_title_from_index(element[0]))
            res_val = get_title_from_index(element[0]).title()
            res_loc = get_location_from_index(element[0]).title()
            # print(res_val)
            restaurants_list.append(res_val)
            restaurants_loc.append(res_loc)

            i = i + 1
            if i > 6:
                break
          # print("THis is ", restaurants_list)
        #  print("This is my recommendation", restaurants_list)
        # restaurant_list is passed as context named 'restaurants'
        if len(restaurants_list) > 0:
            return render(request, "basic_app/resturantList.html", {'restaurants': [restaurants_list],'restaurants1':[restaurants_loc]})


        else:
            return render(request, "basic_app/nodata.html", )

        # return render(request, "basic_app/nodata.html",)

    else:
         #return render(request, "basic_app/index.html", )
         return render(request, "basic_app/nodata.html", )
