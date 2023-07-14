import streamlit as st
from sqlalchemy import URL,create_engine,text,inspect
from sqlalchemy.orm import Session
from datetime import time,datetime
import pandas as pd
import matplotlib.pyplot as plt

#url_object = URL.create(
#    "mysql+mysqlconnector",
#    username='root',
#    password='1234',
#    host='localhost',
#    database='imdb_alchemy'
#)
engine = create_engine("mysql+mysqlconnector://root:1234@localhost/imdb_alchemy")

    
    
#conn = st.experimental_connection('mysql',type='sql')

#df = conn.query('SELECT * from movie;', ttl=600)

st.set_page_config(
    page_title='Streamlit IMDB',
    page_icon= ':snake:'
)
st.title("Filtering Tables")

st.header('Year Filter')

start_year, end_year = st.slider(
    "**Year Filter**",
    1900,2023,(1900,2023))


with engine.connect() as conn:
    df_year = conn.execute(text(f"SELECT * from movie where year >= {start_year} and year <= {end_year}"))

st.dataframe(df_year)

st.header('Runtime Filter')

start_runtime,end_runtime = st.slider(
    "**Runtime Filter**",
    0,300,(0,300))


with engine.connect() as conn:
    df_runtime = conn.execute(text(f"SELECT * from movie where runtime >= {start_runtime} and runtime <= {end_runtime}"))

st.dataframe(df_runtime)

st.header('Actors Filter')

with engine.connect() as conn:
    data = conn.execute(text(f"select distinct p.name from cast join person p on p.id = cast.person_id"))

actors = st.multiselect(
    label='choose your favorite casts!',
    options=[name[0] for name in data],
)

with engine.connect() as conn:
    if not actors:
        df_actors = conn.execute(text(f"select title from movie"))
    else:
        actor_names = ', '.join([f"'{actor}'" for actor in actors]) if len(actors) > 1 else ''.join([f"'{actor}'" for actor in actors])
        df_actors = conn.execute(text(f"select distinct title from cast join movie m on m.id = cast.movie_id join person p on p.id = cast.person_id where p.name in ({actor_names})"))

st.dataframe(df_actors)


st.header('Genre Filter')

with engine.connect() as conn:
    data_genre = conn.execute(text(f"select distinct genre from genre"))

genres = st.multiselect(
    label='choose your genre!',
    options=[name[0] for name in data_genre],
    max_selections=1
)

with engine.connect() as conn:
    if not genres:
        df_genre = conn.execute(text(f"select title from movie"))
    else:
        genre = ''.join([f"'{i}'" for i  in genres])
        df_genre = conn.execute(text(f"SELECT title FROM movie m JOIN genre g ON g.movie_id = m.id WHERE g.genre = {genre} GROUP BY m.id HAVING COUNT(*) = 1;"))

st.dataframe(df_genre)


st.title("Interactive Charts")

st.header('Sales Bar Chart')

with engine.connect() as conn:
    sale_chart = conn.execute(text('select title,gross_us_canada from movie order by gross_us_canada desc limit 10'))
    df_sale = pd.DataFrame(sale_chart.fetchall(),columns=sale_chart.keys())

st.bar_chart(df_sale.set_index("title"))


st.header('5 Most Frequent Actors')
with engine.connect() as conn:
    query_top5 = """
SELECT person.name, COUNT(*) as appearances
FROM person
JOIN cast ON person.id = cast.person_id
WHERE cast.movie_id IN (SELECT id FROM movie)
GROUP BY person.name
ORDER BY appearances DESC
LIMIT 5
"""
    top5_chart = conn.execute(text(query_top5))
    df_top5 = pd.DataFrame(top5_chart.fetchall(),columns=top5_chart.keys())
st.bar_chart(df_top5.set_index("name"))


st.header('Pie Charts')
with engine.connect() as conn:
    query_genre = """
select genre,count(*) as count
from genre
join movie m on m.id = genre.movie_id
group by genre;
"""
    query_age_rating = """
SELECT parental_guide, COUNT(*) as count
FROM movie
GROUP BY parental_guide
"""
    genre_chart = conn.execute(text(query_genre))
    df_count_genre = pd.DataFrame(genre_chart.fetchall(),columns=genre_chart.keys())

    age_chart = conn.execute(text(query_age_rating))
    df_age_rating = pd.DataFrame(age_chart.fetchall(),columns=age_chart.keys())

fig,ax = plt.subplots(1,2)
ax[0].pie(df_count_genre['count'],labels=df_count_genre['genre'], autopct="%1.1f%%")
ax[0].set_title('Genre Distribution')

ax[1].pie(df_age_rating['count'],labels=df_age_rating['parental_guide'], autopct="%1.1f%%")
ax[1].set_title('Age Distribution')

st.pyplot(fig)


st.header('Age Rating Per Genre')
with engine.connect() as conn:
    query_age_genre = """
SELECT genre.genre, movie.parental_guide, COUNT(*) as count
FROM genre
JOIN movie on genre.movie_id = movie.id
GROUP BY genre.genre, movie.parental_guide
"""
    age_genre_chart = conn.execute(text(query_age_genre))
    df_age_genre = pd.DataFrame(age_genre_chart.fetchall(),columns=age_genre_chart.keys())
st.bar_chart(df_age_genre.pivot(index='genre',columns='parental_guide',values='count'))

st.title("Static Charts")

st.header('Most Sells Per Genre')
with engine.connect() as conn:
    data_sells_genre = conn.execute(text(f"select distinct genre from genre"))

age_sell_genres = st.multiselect(
    label='Select Genre',
    options=[name[0] for name in data_sells_genre],
    max_selections=1,
    key='2'
)

with engine.connect() as conn:
    if not age_sell_genres:
        sell_genres_chart = conn.execute(text(f"select title,gross_us_canada from movie"))
        df_sell_genre = pd.DataFrame(sell_genres_chart.fetchall(),columns=sell_genres_chart.keys())
    else:
        sell_genre = ''.join([f"'{i2}'" for i2  in age_sell_genres])
        sell_genres_chart = conn.execute(text(f"SELECT title,gross_us_canada FROM movie m JOIN genre g ON g.movie_id = m.id WHERE g.genre = ({sell_genre}) order by gross_us_canada desc;"))
        df_sell_genre = pd.DataFrame(sell_genres_chart.fetchall(),columns=sell_genres_chart.keys())
st.bar_chart(df_sell_genre.set_index("title"))
