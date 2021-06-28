import streamlit as st
import pandas as pd
import numpy as np
import time


from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = '3d665c8e4b06f0fd2de441c414da3d3a'
tmdb.language = 'en'
tmdb.debug = True
from tmdbv3api import Movie
movie = Movie() 


data = pd.read_csv('tmdb_5000_movies.csv')
cred = pd.read_csv('tmdb_5000_credits.csv')
cred.columns = ['id','title','cast','crew']
data = data.merge(cred,on='id')

data = data.reset_index()

C = 6.092171559442011
m = 1838.4000000000015
indices = pd.Series(data.index, index = data['title_y'])


def wt_rate(x, m=m,C=C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

def disp_movie(id):
    m = movie.details(id)
    c1,c2 = st.beta_columns([3,1])
    with c1:
        st.write('**{}**'.format(m.title))
        st.write(m.overview)
    x = m.poster_path
    with c2:
        st.image('https://image.tmdb.org/t/p/w185/'+x)
    return 0



def disp(title):
        search = movie.search(title)
        try:
            id = search[0].id
            disp_movie(id)
        except:
            st.write("not found")

def get_title(title):
    tit = movie.search(title)
    id_ = tit[0].id
    mo= movie.details(id_)
    return mo.title

@st.cache(allow_output_mutation=True)
def load_cs2():
    cs2 = pd.read_csv('cs22.csv')
    cs = cs2.to_numpy()
    cs_new = np.delete(cs,0,axis=1)
    return cs_new


def get_recc(title,cosine_sim):
    try:
        title = get_title(title)
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]
        
        movies = data.iloc[movie_indices][['title_y', 'vote_count', 'vote_average']]
        vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
        C = vote_averages.mean()
        m = vote_counts.quantile(0.60)
        qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & 
                        (movies['vote_average'].notnull())]
        qualified['vote_count'] = qualified['vote_count'].astype('int')
        qualified['vote_average'] = qualified['vote_average'].astype('int')
        qualified['wr'] = qualified.apply(wt_rate, axis=1)
        qualified = qualified.sort_values('wr', ascending=False).head(20)
        return qualified['title_y']
    except:
        st.write("No such movie in our directory")


genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
       'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign', 'History',
       'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
       'TV Movie', 'Thriller', 'War', 'Western']

def main():
    
    st.markdown('<style>body{color: white ; text-align: center;}</style>',unsafe_allow_html=True)
    st.title("MOVIE RECOMMENDOR")
    
        
    #st.title("MOVIE RECOMMENDER APP")
    menu = ['HOME','MOST POPULAR','TOP RATED','RECOMMEND','GENRE CHARTS']
    choice = st.sidebar.selectbox("""MENU:""",menu)
        
    if choice == 'HOME':
        st.subheader("HOME")
        st.write("")
        st.header("Content Based Recommendor System")
        st.subheader("The system recommends movies on the basis of the movie you enter.")
        st.write("")
   
                    
    elif choice == 'MOST POPULAR':
        st.subheader("MOST POPULAR MOVIES:")
        popular = pd.read_csv('popular.csv')

        n = st.number_input("No of movies: ",min_value=3,max_value=20,value=8)
        bt = st.button("SHOW MOVIES",key='55')
        if bt:
            for i in popular.head(n)['title_y']:
                disp(i)


    elif choice == 'TOP RATED':
        st.subheader("TOP RATED MOVIES:")
        t = pd.read_csv('top_csv.csv').head(20)
        topp = t['title_y']
        n = st.number_input("No of movies: ",min_value=3,max_value=20,value=8)
        btt = st.button("SHOW MOVIES",key='555')
        if btt:
            for i in topp.head(n):
                disp(i)

    elif choice =='GENRE CHARTS':
        gen = st.selectbox("Select the genre: ",genre_list)
        if st.button("Show chart",key="5"):
            ge = pd.read_csv('genre_csv.csv').head(10)
            d = ge[gen]
            for i in d.head(8):
                disp(i)
                    
    elif choice == 'RECOMMEND':
        title = st.text_input('TYPE ANY MOVIE: ')
        if st.button("Show movie",key="6"):
            if title is not None:
                st.write("Your selected movie is:")
                disp(title)
            st.subheader("Similar movies are:")
            try:
                movies = get_recc(get_title(title),load_cs2())
                for i in movies:
                    disp(i)
            except:
                pass


if __name__=='__main__':
    main()