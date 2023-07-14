# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from typing import List
from typing import Optional
import json 

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import select,inspect,column

from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer,Numeric,Column,BigInteger
from sqlalchemy import Select, Insert, Update

from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# -

DB_NAME = 'imdb_alchemy'

# +

URL_OBJECT = URL.create(
    "mysql+mysqlconnector",
    username='root',
    password='1234',
    host='localhost',
)
print(URL_OBJECT)
engine = create_engine(URL_OBJECT)
with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
# -

url_object = URL.create(
    "mysql+mysqlconnector",
    username='root',
    password='1234',
    host='localhost',
    database=DB_NAME
)
print(url_object)
engine = create_engine(url_object)

with engine.connect() as conn : 
    results = conn.execute(text('SHOW DATABASES;'))
    for res in results : 
        print(res)


class Base(DeclarativeBase):
    pass


# +
class Movie(Base):
    __tablename__ = "movie"

#    __table_args__ = {'extend_existing': True}

    id:Mapped[str] = mapped_column(String(8),primary_key=True)
    title:Mapped[str] = mapped_column(String(128))
    year:Mapped[int] = mapped_column(Integer)
    runtime:Mapped[int] = mapped_column(Integer)
    parental_guide:Mapped[str] = mapped_column(String(8))
    gross_us_canada:Mapped[int] = mapped_column(BigInteger)

    genres:Mapped["Genre"] = relationship(back_populates="movie")
    casts:Mapped["Cast"] = relationship(back_populates="movie")
    crews:Mapped["Crew"] = relationship(back_populates="movie")

    def __init__(self, id, title, year, runtime, parental_guide, gross_us_canada):
        self.id = id
        self.title = title
        self.year = int(year)
        self.runtime = runtime
        self.parental_guide = parental_guide
        self.gross_us_canada = int(gross_us_canada)


    def __repr__(self) -> str:
        return f"Movie(id= {self.id}, title= {self.title})"



# +
class Person(Base):
    __tablename__ = "person"
#    __table_args__ = {'extend_existing': True}

    id:Mapped[str] = mapped_column(String(8),primary_key=True)
    name:Mapped[str] = mapped_column(String(32))

    casts:Mapped[List["Cast"]] = relationship(back_populates="person")
    crews:Mapped[List["Crew"]] = relationship(back_populates="person")

    def __repr__(self) -> str:
        return f"Movie(id= {self.id}, name= {self.name})"


# -

class Cast(Base):
    __tablename__ = "cast"
#    __table_args__ = {'extend_existing': True}

    id:Mapped[int] = mapped_column(primary_key=True)
    movie_id:Mapped[str] = mapped_column(ForeignKey("movie.id"))
    person_id:Mapped[str] = mapped_column(ForeignKey("person.id"))

    movie:Mapped["Movie"] = relationship(back_populates="casts")
    person:Mapped["Person"] = relationship(back_populates="casts")
    


# +
class Crew(Base):
    __tablename__ = "crew"
#    __table_args__ = {'extend_existing': True}
    
    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    movie_id:Mapped[str] = mapped_column(String(8),ForeignKey("movie.id"))
    person_id:Mapped[str] = mapped_column(String(8),ForeignKey("person.id"))
    role:Mapped[str] = mapped_column(String(8))

    movie:Mapped["Movie"] = relationship(back_populates="crews")
    person:Mapped["Person"] = relationship(back_populates="crews")
    


# +
class Genre(Base):
    __tablename__ = "genre"
#    __table_args__ = {'extend_existing': True}

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    movie_id:Mapped[str] = mapped_column(String(8),ForeignKey("movie.id"))
    genre:Mapped[str] = mapped_column(String(16))

    movie:Mapped["Movie"] = relationship(back_populates="genres")

    
# -

Base.metadata.create_all(engine)

with engine.connect() as conn:
    conn.execute(text('USE imdb_alchemy'))
    result = conn.execute(text("SHOW TABLES"))
    for res in result.all() : 
        print(res)


def to_minutes(runtime:str):
    global result

    if len(runtime) == 6:
        result = int(runtime[0])*60 + int(runtime[3:5])
    elif len(runtime) == 5:
        result = int(runtime[0])*60 + int(runtime[3])
    elif len(runtime) == 3:
        result = int(runtime[0])*60
    elif len(runtime) == 4:
        result = int(runtime[:2])
    else:
        result = int(runtime[0])
    return result


def to_int(string:str):
    global result2
    if string:
        result2 = int(string.replace('$', '').replace(',', '')) 
    else:
       result2 = 0
    return result2


# +
Session = sessionmaker(engine)
session = Session()

with open('imdb_250_movies.json') as f:
    data = json.load(f)

for movie_data in data:
    smovie = Movie(
        id = movie_data['movieid'],
        title = movie_data['title'],
        year = movie_data['year'],
        runtime = to_minutes(movie_data['runtime']),
        parental_guide = movie_data['parental_guide'] if movie_data['parental_guide'] not in ['null', 'blank', 'Not Rated',None,'None'] else 'Unrated',
        gross_us_canada = to_int(movie_data['gross'])
        #int((movie_data['gross'].replace('$', '').replace(',', ''))) if movie_data['gross'] else 0
    )
    session.add(smovie)

    people_ids = movie_data['peopleid']
    people_names = movie_data['director'] + movie_data['writer'] + movie_data['star']   
    people_data = [{'id': id, 'name': name} for id, name in zip(people_ids, people_names)]
    for person in people_data:
        query = select(Person).filter_by(id=person['id'])
        sperson = session.scalars(query).first()
        
        if sperson is None:
            sperson = Person(
                id = person['id'],
                name = person['name']
            )
            session.add(sperson)


        if person['name'] in movie_data['star']:
            scast = Cast(
                movie_id = smovie.id,
                person_id = sperson.id
            )
            session.add(scast)

        if person['name'] in movie_data['director']:
            screw = Crew(
                movie_id = smovie.id,
                person_id = sperson.id,
                role = 'Director'
            )
            session.add(screw)
        if person['name'] in movie_data['writer']:
            screw = Crew(
                movie_id = smovie.id,
                person_id = sperson.id,
                role = 'Writer'
            )
            session.add(screw)
    
    for genre in movie_data['genre']:
        sgenre = Genre(
            genre = genre,
            movie_id = smovie.id
        )
        session.add(sgenre)

session.commit()

# -

x = select(Movie)
for i in session.scalars(x):
    print(i)


