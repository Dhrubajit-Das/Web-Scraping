from bs4 import BeautifulSoup
import requests 
import pandas as pd

url = "https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2417962742&pf_rd_r=0M85G1V8JHW928EHBETF&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3"

movies_df = pd.DataFrame()

data = requests.get(url)
data = data.text
soup = BeautifulSoup(data, 'html.parser')

m_list = []
movies_class = soup.find_all('td', class_='titleColumn')
for movie in movies_class:
    movie_name = movie.find('a').get_text()
    m_list.append(movie_name)
    

y_list = []
for yr in movies_class:
    myear = yr.find('span').get_text()
    y_list.append(myear)
    
r_list = []
rating = soup.find_all('td', class_='ratingColumn imdbRating')
for rate in rating:
    rate_n = rate.find('strong').get_text()
    rate_n = float(rate_n)
    r_list.append(rate_n)
    

movies_df['name'] = m_list
movies_df['year'] = y_list
movies_df['rating'] = r_list

links = []
movies_class = soup.find_all('td', class_='titleColumn')

for movie in movies_class:
    link_name = movie.find('a').get('href')
    links.append(link_name)
   
directors = []
writers = []
actors = []
genre = []
country = []
language = []
count = 0
for i in links:
    movies_links = "https://www.imdb.com/" + i
    resp = requests.get(movies_links)
    resp = resp.text
    msoup = BeautifulSoup(resp, 'html.parser')    
    
    #country, language
    p = msoup.find('div', attrs={'id': 'titleDetails'})
    
    bar = p.find('div', attrs={'class': 'txt-block'})
    
    country_list = bar.find_next_siblings('div')[0]
    country.append(country_list.text)
    
    language_list = bar.find_next_siblings('div')[1]
    language.append(language_list.text)
    
    
    #genre
    g = msoup.find('div', attrs={'class': 'see-more inline canwrap'})
    genre_list = g.find_next_siblings('div')[1]
    
    genre.append(genre_list.text)
   
    
    #directors, writers and actors...
    x = msoup.find('div', attrs={'class': 'credit_summary_item'})
    directors.append(x.text)
    
    writers_name = x.find_next_siblings('div')[0]
    writers.append(writers_name.text)
        
    actors_names = x.find_next_siblings('div')[1]
    actors.append(actors_names.text)
    count += 1
    print(count)
    
movies_df['Directors'] = directors   
movies_df['Writers'] = writers
movies_df['Actors'] = actors
movies_df['Genre'] = genre
movies_df['Country'] = country
movies_df['Language'] = language
    
    




