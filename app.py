from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests


#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get("https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31")
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', class_ = "lister-list")
movie_table = table.find_all('div', class_ = "lister-item-content")


temp = [] #initiating a list


# Extracting Movie's Title
for i in movie_table:
	titles = i.find('a').string #to convert result into string object
	
# Extract Genre
	x = (i.find('span', {'class' : "genre"}).string).split(',') #split string into list
	General_genres = x[-1].strip()  #slice genre last list to describe the movie in general genre
	Specific_genres = x[0].strip()  #slice genre first list to describe the movie in specific genre
	
# Extracting Movie's PG Rating
	pg_rate = i.find('span',  class_ = "certificate")
	if pg_rate != None:
		pg_rate = pg_rate.string
	
	
# Extracting Movie's Rating
	ratings = float(i.find('strong').string) #to convert from string into float
	
	
# Extracting Movie's Votes
	votes = i.find('span', {'name':'nv'}).string.replace(',', '') #to remove (,) in the number of votes
	
# Extracting Movie's Metascore
	metascore = i.find('span', {'class':'metascore favorable'})
	if metascore != None:                           #To return each output with conditional statemenent with desired format
		metascore = metascore.string.strip() 
		
	temp.append((titles, General_genres, Specific_genres, pg_rate, ratings, votes, metascore))

#change into dataframe

movie_df = pd.DataFrame(temp, columns = ['Title', 'General_genres', 'Specific_genres', 'pg_rate', 'Imdb_Ratings', 'Votes', 'Metascore'])

#insert data wrangling here
category = []
for i in movie_df['Metascore']:
	if i == None:
		category.append('TV-Show/Series')
	else:
		category.append('Movie')

# Create Category Column
movie_df['Category'] = category

movie_df[['Metascore']] = movie_df[['Metascore']].fillna(0)
movie_df[['Votes', 'Metascore']] = movie_df[['Votes', 'Metascore']].astype('int')
movie_df[['General_genres', 'Specific_genres', 'Category']] = movie_df[['General_genres', 'Specific_genres', 'Category']]. astype('category')
movie_df['pg_rate'] = movie_df['pg_rate'].fillna(method = 'ffill')

movie = movie_df[movie_df['Category'] == 'Movie']
movieMetascore = movie[['Title', 'General_genres', 'Specific_genres', 'Metascore']]

#end of data wranggling 

@app.route("/")
def index(): 
	

	#be careful with the " and ' 
	card_data = f'{movieMetascore["Metascore"].mean().round(2)}'
	# generate plot∏

	ax = movieMetascore.plot.box(figsize = (20,9)) 
	
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
	app.run(debug=True)