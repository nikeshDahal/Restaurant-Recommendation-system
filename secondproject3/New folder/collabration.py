import pandas as pd
from scipy import sparse

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

romantic_lover = [("Cafe Cofee Day","Kumaripati",0)]
similar_movies = pd.DataFrame()
for movie,location,rating in romantic_lover:
    similar_movies = similar_movies.append(get_similar(movie,location,rating),ignore_index = True)

(similar_movies.head(10))


(similar_movies.sum().sort_values(ascending=False).head(10))

action_lover = [("Chicken Station","Jhamsikhel",4)]
similar_movies = pd.DataFrame()
for movie,location,rating in action_lover:
    similar_movies = similar_movies.append(get_similar(movie,location,rating),ignore_index = True)

similar_movies.head(5)
print(similar_movies.sum().sort_values(ascending=False).head(10))



