#!/usr/bin/env python
# coding: utf-8

# # DATA PREPROCESSING

# In[1]:


#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval


# In[2]:


#reading the dataset required
data_movies = pd.read_csv('tmdb_5000_movies.csv', na_filter=False)
data_credits = pd.read_csv('tmdb_5000_credits.csv')


# In[3]:


#renaming the column present in dataset movies so as to merge
data_movies.rename(columns={'id':'movie_id'},inplace=True)


# In[4]:


#attributes/columns present in both dataset
data_movies.head(1)


# In[5]:


data_credits.head(1)


# In[6]:


#merging both the data set 
data_credits.columns = ['movie_id','tittle','cast','crew']
data_movies = data_movies.merge(data_credits,on='movie_id')


# In[7]:


data_movies.head(2)


# In[8]:


#droping all the unnecessary columns or columns that are not necessary for our recommendation
data_movies = data_movies.drop(columns=['tittle', 'tagline', 'status', 'homepage', 
                                        'keywords','crew','vote_count', 'vote_average',
                                       'tagline', 'spoken_languages', 'runtime',
                                       'popularity', 'production_companies', 'budget',
                                       'production_countries', 'release_date', 'revenue',
                                        'title', 'original_language'])

data_movies.head(2)


# In[9]:


#evaluating the expression
features = ['cast', 'genres']
for feature in features:
    data_movies[feature] = data_movies[feature].apply(literal_eval)


# In[10]:


def get_list(meta_data):
    if isinstance(meta_data, list):
        names = [col['name'] for col in meta_data]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

features = ['cast','genres']
for feature in features:
    data_movies[feature] = data_movies[feature].apply(get_list)


# In[11]:


data_movies.head(2)


# In[12]:


data_movies.isnull().sum()


# In[13]:


data_movies_hindi = pd.read_csv('bollywood_full_1950-2019.csv', na_filter=False)

data_movies_hindi.head(2)


# In[14]:


data_movies_hindi = data_movies_hindi.drop(columns=['title_x', 'tagline', 'poster_path', 
                                        'wiki_link','title_y','is_adult', 'year_of_release',
                                       'tagline', 'imdb_rating', 'runtime',
                                       'imdb_votes', 'story',
                                       'wins_nominations', 'release_date'])

data_movies_hindi.rename(columns = {'actors':'cast', 'imdb_id':'movie_id'}, inplace = True)

data_movies_hindi['genres'] = data_movies_hindi['genres'].str.split('|')

data_movies_hindi['cast'] = data_movies_hindi['cast'].str.split('|')

data_movies_hindi = data_movies_hindi.drop([697])

data_movies_hindi.head()


# In[15]:


def clean_data(actors):
    if isinstance(actors, list):
        return actors[:3]

features = ['cast']
for feature in features:
    data_movies_hindi[feature] = data_movies_hindi[feature].apply(clean_data)

data_movies_hindi.head()


# In[16]:


data_movies_hindi.isnull().sum()


# In[17]:


combine = data_movies.append(data_movies_hindi, ignore_index=True, sort=True)

combine = combine.drop([5160])

#combine['plot'] = combine[['overview', 'summary']].apply(lambda x: ' '.join(x), axis = 1) 

#combine = combine.drop(['summary','overview'],axis=1)

combine  #5160


# In[18]:


combine.to_csv('movie_data_test.csv', index=False)


# In[19]:


pd.set_option('display.max_rows', None)

final_data = pd.read_csv('movie_data_test.csv', na_filter=False)

final_data['plot'] = final_data[['overview', 'summary']].apply(lambda x: ' '.join(x), axis = 1) 

final_data = final_data.drop(['summary','overview'],axis=1)

final_data = final_data[:-1]


# In[20]:


final_data


# In[21]:


final_data.to_csv('all_movie_data.csv', index=False)


# In[22]:


data = pd.read_csv('all_movie_data.csv')
print(data.memory_usage().sum())
data=data.drop([6221,6222,6219,6210,6211,5508,6121,5634,2962,5499])
data


# In[23]:


data.drop(data.index[6465:9130],0,inplace=True)

data[data['original_title'].str.contains('Mission Impossible: Ghost Protocol')]


# In[24]:


data_new = pd.DataFrame({'cast':[['Robert Downey Jr.', 'Chris Evans', 'Chris Hemsworth'],
                              ['Joaquin Phoenix ','Robert De Niro','Zazie Beetz'],
                             ['Robert Downey Jr.', 'Josh Brolin', 'Chris Hemsworth'],
                             ['Chadwick Boseman','Michael B. Jordan', 'Danai Gurira'],
                             ['Chris Hemsworth'", 'Tom Hiddleston'", 'Cate Blanchett'],
                            ['Keanu Reeves', 'Michael Nyqvist', 'Ian McShane'],
                            ['Keanu Reeves', 'Riccardo Scamarcio', 'Ian McShane'],
                            ['Hugh Jackman', 'Patrick Stewart', 'Dafne Keen'],
                            ['Benedict Cumberbatch', 'Chiwetel Ejiofor', 'Tilda Swinton'],
                            ['Manoj Bajpayee', 'Tigmanshu Dhulia', 'Richa Chadda'],
                            ['Nawazuddin Siddiqui', 'Tigmanshu Dhulia', 'Huma Qureshi'],
                            ['Tom Cruise', 'Henry Cavill', 'Rebecca Ferguson']
                            ],
                    
                    'genres':[
                            ['Action', 'Adventure', 'Drama'],
                            ['Crime', 'Drama', 'Thriller'],
                            ['Action', 'Adventure', 'Sci-Fi'],
                            ['Action', 'Adventure', 'Sci-Fi'],
                            ['Action', 'Adventure', 'Comedy'],
                            ['Action', 'Crime', 'Thriller'],
                            ['Action', 'Crime', 'Thriller'],
                            ['Action', 'Drama', 'Sci-Fi'],
                            ['Action', 'Adventure', 'Fantasy'],
                            ['Action', 'Thriller', 'Crime'],
                            ['Action', 'Thriller', 'Crime'],
                            ['Action', 'Adventure', 'Thriller']
                        ],
                   'movie_id':[
                        sum([299534]),
                        sum([475557]),
                        sum([299536]),
                        sum([284054]),
                        sum([284053]),
                        sum([245891]),
                        sum([324552]),
                        sum([263115]),
                        sum([284052]),
                        sum([117691]),
                        sum([126400]),
                        sum([353081])
                        ],
                    
                    'original_title':['Avengers: Endgame', 'Joker',
                                      'Avengers: Infinity War', 'Black Panther', 
                                      'Thor: Ragnarok', 'John Wick', 
                                      'John Wick: Chapter 2','Logan','Doctor Strange',
                                      'Gangs of Wasseypur - Part 1', 'Gangs of Wasseypur - Part 2',
                                      'Mission: Impossible – Fallout'
                                     ],
                      'plot':
['After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos actions and restore balance to the universe.',
'In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.',
'The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.',
'T Challa, heir to the hidden but advanced kingdom of Wakanda,must step forward to lead his people into a new future and must confront a challenger from his country past.',
'Imprisoned on the planet Sakaar, Thor must race against time to return to Asgard and stop Ragnarök, the destruction of his world, at the hands of the powerful and ruthless villain Hela.',
'An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.',
'After returning to the criminal underworld to repay a debt, John Wick discovers that a large bounty has been put on his life.',
'In a future where mutants are nearly extinct, an elderly and weary Logan leads a quiet life. But when Laura, a mutant child pursued by scientists, comes to him for help, he must get her to safety.',
'While on a journey of physical and spiritual healing, a brilliant neurosurgeon is drawn into the world of the mystic arts.',
'Shahid Khan is exiled after impersonating the legendary Sultana Daku in order to rob British trains. Now outcast, Shahid becomes a worker at Ramadhir Singhs colliery, only to spur a revenge battle that passes on to generations. At the turn of the decade, Shahids son, the philandering Sardar Khan vows to get his fathers honor back, becoming the most feared man of Wasseypur.',
'Sardar Khan’s sons are at war with Ramadhir Singh’s men; and the knives clash and the bullets flash; till either drops dead.',
'Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission gone wrong.'
]
                        
})


# In[25]:


data_new


# In[26]:


data = data.append(data_new, ignore_index=True, sort=True)
data


# In[27]:


data[data['original_title'].str.contains('The Shawshank Redemption')]


# In[28]:


data.to_csv('movie_data.csv.zip', index=False)
df = pd.read_csv('movie_data.csv.zip')

df


# In[29]:


df.to_csv('movie_data_compress.csv.zip', index = False)


# # Building a content based recommendation System

# In[30]:


#importing necessary libraries
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[31]:


#Convert the title of all the movies to lowercase letters.
#return the dataset as the function’s result.
def get_data():
    movie_data = pd.read_csv('movie_data.csv.zip')
    movie_data['original_title'] = movie_data['original_title'].str.lower()
    return movie_data


# In[32]:


#it takes the first 3 cast name
import ast
def convert_3(string):
    lst = []
    counter = 0
    for i in ast.literal_eval(string):
        if counter < 3:
            lst.append(i)
        counter+=1
    return lst 


# In[33]:


df['cast'] = df['cast'].apply(convert_3)
df['cast'].head(5)


# In[36]:


#drops the columns not required for feature extraction and then combines the cast and genres column
#return the combine column as the result of this function.
def combine_data(data):
    data_recommend = data.drop(columns=['movie_id', 'original_title','plot'])
    data_recommend['combine'] = data_recommend[['cast','genres']].apply(lambda x:','.join(x.dropna().astype(str)),axis=1)
    data_recommend = data_recommend.drop(columns=[ 'cast','genres'])
    return data_recommend


# In[37]:


#transform_data() takes the value returned by combine_data() and the plot column from get_data() and applies CountVectorizer and TfidfVectorizer respectively and calculates the Cosine values.
def transform_data(data_combine, data_plot):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data_combine['combine'])

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data_plot['plot'])

    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
    
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    
    return cosine_sim


# In[38]:


#Return the Pandas DataFrame with the top 20 movie recommendations.
def recommend_movies(title, data, combine, transform):

    indices = pd.Series(data.index, index = data['original_title'])
    index = indices[title]

    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    
    movie_indices = [i[0] for i in sim_scores]

    movie_id = data['movie_id'].iloc[movie_indices]
    movie_title = data['original_title'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(columns=['Movie_Id','Name','Genres'])

    recommendation_data['Movie_Id'] = movie_id
    recommendation_data['Name'] = movie_title
    recommendation_data['Genres'] = movie_genres

    return recommendation_data


# In[ ]:


#result() takes a movie’s title as input and returns the top 20 recommendations.
def results(movie_name):
    movie_name = movie_name.lower()
    
    find_movie = get_data()
    combine_result = combine_data(find_movie)
    transform_result = transform_data(combine_result,find_movie)
    
    if movie_name not in find_movie['original_title'].unique():
        return 'Movie not in Database'
    
    else:
        recommendations = recommend_movies(movie_name, find_movie, combine_result, transform_result)
        return recommendations.to_dict('records')


# In[ ]:




