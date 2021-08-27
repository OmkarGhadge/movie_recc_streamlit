# MOVIE RECOMMENDER SYSTEM
This recommender uses CONTENT based filtering from the TMDb 5000 movie datset.

![image](https://user-images.githubusercontent.com/64735478/131145585-fda63f21-143e-4f89-a670-226c23d65c57.png)


### Dataset
TMDB 5000 Movie Dataset downloaded from [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
### Dependencies
* Python >=3
* pandas
* numpy
* jupyter notebook
* tmdbv3api
* Streamlit

### Streamlit App
- Contains filtering by genres, top rated, most popular and recommends movies with plot and poster.
- ```app.py``` contains the code for this streamlit application.
- Used the TMDb API to extract information about the movie along with the movie poster.

### Heroku deployment
- Deployed at https://movie-recc-st-app.herokuapp.com/ on Heroku.
