from webscrapping import executeWebScrapping
import pandas as pd

def execute():
    data = executeWebScrapping(1, 2)

    movieDF = pd.DataFrame(data, columns = ['Title', 'General_genres', 'Specific_genres', 'pg_rate', 'Imdb_Ratings',
                            'Votes', 'Metascore'], index = range(1, len(data)+1))

    category = []
    for i in movieDF['Metascore']:
        if i == None:
            category.append('TV-Show/Series')
        else:
            category.append('Movie')

    # Create Category Column
    movieDF['Category'] = category
    movieDF[['Votes','Metascore']] = movieDF[['Votes','Metascore']].fillna(0)
    movieDF[['Votes', 'Metascore']] = movieDF[['Votes', 'Metascore']].astype('int')
    movieDF[['General_genres', 'Specific_genres', 'Category']] = movieDF[['General_genres', 'Specific_genres', 'Category']]. astype('category')
    movieDF['pg_rate'] = movieDF['pg_rate'].fillna(method = 'ffill')

    movies = movieDF[movieDF['Category'] == 'Movie']
    tvSeries = movieDF[movieDF['Category'] != 'Movie']


    #Calculate TOP 10 based on Keyword from all entries data
    def getTop10(data, key):
        return data.sort_values(key, ascending = False).head(10)


    #Subset data based on Keyword
    def subsetByColumn(data, column, key):
        return data[data[column] == (key)]


    

    #Design dictionaries for calculation subsetting and sorting
    top10Movies = {}
    top10TvSeries = {}
    top10MovieRating = {}
    top10TvSeriesRating ={}
    top10MovieMetascore = {}

    listGenre = movieDF['General_genres'].unique()

    for genre in listGenre:
        #Calculate highest Votes per Genre
        top10Movies[genre] = getTop10(subsetByColumn(movies, 'Specific_genres', genre), 'Votes')
        top10TvSeries[genre] = getTop10(subsetByColumn(tvSeries, 'General_genres', genre), 'Votes')
        
        #Calculate highest IMDB Rating per Genre
        top10MovieRating[genre] = getTop10(subsetByColumn(movies, 'Specific_genres', genre), 'Imdb_Ratings')
        top10TvSeriesRating[genre] = getTop10(subsetByColumn(tvSeries, 'General_genres', genre), 'Imdb_Ratings')
        
        #Calculate highest Metascore per Genre
        top10MovieMetascore[genre] = getTop10(subsetByColumn(movies, 'Specific_genres', genre), 'Metascore')
    
    return top10Movies


    