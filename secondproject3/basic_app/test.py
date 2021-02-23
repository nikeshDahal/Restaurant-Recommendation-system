import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
import db


###### helper functions. Use them when needed #######


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


##################################################


# Step 1: Read CSV File


#####


df = pd.read_sql_query("select * from basic_app_restaurant;", db.connection_obj_db)
print(df.to_string())
##pd.read_sql_table('restaurant - 2', 'postgres:///test')


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
movie_user_likes = 'Syanko'

# Step 6: Get index of this movie from its title
movie_index = get_index_from_title(movie_user_likes)


similar_movies = list(enumerate(cosine_sim[int(movie_index)]))

# Step 7: Get a list of similar movies in descending order of similarity score
sorted_similar_movies = sorted(
    similar_movies, key=lambda x: x[1], reverse=True)

# Step 8: Print titles of first 50 movies
i = 0
for element in sorted_similar_movies:
    print(get_title_from_index(element[0]))
    i = i + 1
    if i > 5:
        break