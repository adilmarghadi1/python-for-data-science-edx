## ######################################################################### ##
## Analysis of IMDB Movie Dataset
## For EdX Course
## Python for Data Science (Week 6 Mini Project)
## ######################################################################### ##

## ========================================================================= ## 
## import libraries
## ========================================================================= ##

import requests
import io
import zipfile
import os
import urllib.parse
import re   ## for regular expressions
from itertools import chain  ## for chain, similar to R's unlist
import collections   ## for Counters (used in frequency tables, for example)
import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt


## ========================================================================= ##
## download and extract zip
## ========================================================================= ##

## define url and filename, as well as target path:
url_base = 'http://files.grouplens.org/datasets/movielens/'
filename = 'ml-20m.zip'
url = urllib.parse.urljoin(url_base, filename)
path_dat = './data'

# ## download (commented out in order not to repeat it every time):
# r = requests.get(url, allow_redirects=True)
# open(filename, 'wb').write(r.content)
#
# ## check download:
# os.getcwd()
# os.listdir()
# 
# ## unzip:
# zip_ref = zipfile.ZipFile(filename, 'r')
# zip_ref.extractall(path_dat)
# zip_ref.close()

## ========================================================================= ##
## Load data files
## ========================================================================= ##

dat_movies = pd.read_csv(
    os.path.join(path_dat, 'ml-20m/movies.csv'), 
    sep = ',')

dat_movies.head(2)
dat_movies.info()

#dat_movies.dtype                    ## 'DataFrame' object has no attribute 'dtype'
dat_movies['movieId'].dtype
dat_movies['title'].dtype   

type(dat_movies)                     ## also for DataFrame: pandas.core.frame.DataFrame
type(dat_movies['movieId'])          ## pandas.core.series.Series
type(dat_movies['movieId'].values)   ## numpy.ndarray
type(dat_movies['movieId'][1])       ## numpy.int64

dir(dat_movies)                      ## list all methods?

## find strings in this list:
# dir(dat_movies).str.contains('unstack')  ... str.-methods only work on pandas df, not lists
list(filter(lambda x:'values' in x, dir(dat_movies)))  ## filter returns an iterable, hence need 'list'
list(filter(lambda x: re.search(r'unstack', x), dir(dat_movies)))

cond = df['A'].str.contains('a')

dat_movies.__dict__                  ## lengthy, equivalent to vars(<>)
vars(dat_movies)                     ## lengthy, equivalent to <>.__dict__

dat_movies.describe()                ## similar to R's summary()

dat_ratings = pd.read_csv(
    os.path.join(path_dat, 'ml-20m/ratings.csv'), 
    sep = ',')

dat_ratings.head(2)
dat_ratings.info()

dat_tags = pd.read_csv(
    os.path.join(path_dat, 'ml-20m/tags.csv'), 
    sep = ',')

dat_tags.head(2)
dat_tags.info()

## Note:
## For some reason, string columns are of type "object".
## https://stackoverflow.com/questions/33957720/how-to-convert-column-with-dtype-as-object-to-string-in-pandas-dataframe
## since strings data types have variable length, 
## it is by default stored as object dtype. If you want to store them as 
## string type, you can do something like this.
## df['column'] = df['column'].astype('|S80') #where the max length is set at 80 bytes,
## or alternatively
## df['column'] = df['column'].astype('|S') # which will by default set the length to the max len it encounters
##  the pandas dataframe stores the pointers to the strings and hence it is of type 'object'.

#dat_movies.head(2)['title'].astype('str')

## ========================================================================= ##
## data prep
## ========================================================================= ##

## possible research questions:
## * what is the relationship of movie complexity 
##   (as measured by number of genres) and average rating? u-shaped?
## * what is the relationship of genres and average rating? 
##   have different genres different ratings, on average?


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## aggregate ratings data
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

## aggregate ratings data:
## https://stackoverflow.com/questions/38935541/dplyr-summarize-equivalent-in-pandas
dat_ratings_agg = dat_ratings \
    .groupby('movieId') \
    .agg({'rating': ['size', 'min', 'max', 'mean', 'std'], 
         'timestamp': ['min', 'max', 'mean', 'std']})
#dat_ratings_agg.head(2)

## rename columns:
dat_ratings_agg.columns = ['_'.join(col) \
                           for col in dat_ratings_agg.columns]
#dat_ratings_agg.head(2)

## add correct timestamp column (after aggregation, 
## as they cannot be aggregated like numerical values):
dat_tags['parsed_time'] = pd.to_datetime(
    dat_tags['timestamp'], unit='s')
dat_ratings['parsed_time'] = pd.to_datetime(
    dat_ratings['timestamp'], unit='s')
dat_ratings_agg['parsed_time_min'] = pd.to_datetime(
    dat_ratings_agg['timestamp_min'], unit='s')
dat_ratings_agg['parsed_time_max'] = pd.to_datetime(
    dat_ratings_agg['timestamp_max'], unit='s')
dat_ratings_agg['parsed_time_mean'] = pd.to_datetime(
    dat_ratings_agg['timestamp_mean'], unit='s')
dat_ratings_agg.head(2)

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## merge data files into one wide file
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

## merge data files into one wide file for analysis by movie:
dat_raw = pd.merge(
    left = dat_movies,
    right = dat_ratings_agg,
    how = 'left',
    on = 'movieId')

dat_raw.head(2)


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## add measurement for movie complexity
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

## add measurement for movie complexity:
dat_raw['complexity'] = dat_raw['genres'] \
    .str.split('|') \
    .apply(lambda x: len(x))


## exclude movies that have no genres listed:
## '(no genres listed)' --> None
#dat_raw['complexity'] = None if (dat_raw['genres'] == '(no genres listed)') else dat_raw['complexity']
dat_raw['complexity'] = np.where(dat_raw['genres'] == '(no genres listed)', 
                                 None,
                                dat_raw['complexity'])

## inspect correctness:
dat_raw.groupby(['genres', 'complexity']).agg({'genres': 'size'})
dat_raw.groupby(['genres', 'complexity']).agg({'genres': 'size'}).sort_values(by = 'genres')
## Note:
## 'None' values are just omitted by groupby?

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## add isGenre attributes for most common genres
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

## get list of different genres:
tmp = dat_raw['genres'] \
    .str.split('|')

## similar to unlist, I suppose:
#from itertools import chain
list(chain.from_iterable(tmp))

genres_nonunique = list(chain.from_iterable(tmp))
len(genres_nonunique)

## make frequency table:
# import collections
counter = collections.Counter(genres_nonunique)
print(counter)
print(counter.values())
print(counter.keys())
print(counter.most_common(3))

## make frequency table:
# {x:genres_nonunique.count(x) for x in genres_nonunique}
## (horribly slow, but works)

## create indicator column for each genre:
for i in counter.keys():
    #print('creating indicator for key', i, ':')
    this_ind_name = 'is_' + re.sub('[-\(\) ]', '', i).lower()
    #print(this_ind_name)
    dat_raw[this_ind_name] = dat_raw['genres'].str.contains(i)

dat_raw.info()


## ========================================================================= ##
## Data exploration
## ========================================================================= ##

# dat_raw.info()

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## univariate data checks
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

## mean ratings:

## check mean ratings (histogram):
ggplot(dat_raw, aes(x = 'rating_mean')) + \
  geom_histogram(bins = 40, color = 'blue', fill = 'blue')

## same plot (histogram) using matplotlib, simple variant:
## (doesn't work with missing values in the data)
## (preliminary) conclusion: does not work with jupyterlab, only with 
## ipython notebooks. No idea why. 
## [[?]] how to get matplotlib plots working, without showing all intermediate steps?

# %matplotlib inline
# %matplotlib ipympl
# %matplotlib widget
plt.hist(dat_raw['rating_mean'].dropna().values, 40, density = False, facecolor = 'blue')
plt.grid(True)
plt.show()

## same plot (histogram) using matplotlib, complex variant:
# fig, ax = plt.subplots()
# plt.hist(dat_raw['rating_mean'], 10, normed=False, facecolor='green')

## complexity:

ggplot(dat_raw, aes(x = 'complexity')) + \
  geom_bar(color = 'blue', fill = 'blue')


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## multivariate checks
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

## plot complexity vs. average rating, using ggplot/plotnine:
ggplot(dat_raw, aes(y = 'rating_mean', x = 'complexity')) + \
  geom_jitter(alpha = 0.2)

## similar plot using matplotlib:
## [[todo]]


# ## plot complexity vs. average rating and genre, using ggplot/plotnine:
# ggplot(dat_raw, aes(y = 'rating_mean', x = 'complexity', color = )) + \
#   geom_jitter(alpha = 0.2)
# 
# ## similar plot using matplotlib:
# ## [[todo]]


## ========================================================================= ##
## Analysis
## ========================================================================= ##

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## correlation
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

dat_nona = dat_raw.dropna()

## np.corrcoef(dat_nona['rating_mean'], dat_nona['complexity'])
## AttributeError: 'float' object has no attribute 'shape'
## The error is reproducible if the array is of dtype=object

np.corrcoef(dat_nona['rating_mean'], dat_nona['complexity'].astype(float))


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## regression
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##




