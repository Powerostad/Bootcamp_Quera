
-- Section1

SELECT title FROM movie
WHERE movie_id NOT IN (SELECT movie_id FROM movie_genres);

-- Section2

SELECT movie.title AS Title ,p.person_name AS "Director/Leading actor"
FROM movie
JOIN movie_cast AS mcast ON movie.movie_id = mcast.movie_id
JOIN person AS p ON p.person_id = mcast.person_id
JOIN movie_crew AS mcrew ON p.person_id = mcrew.person_id AND movie.movie_id = mcrew.movie_id
WHERE mcast.cast_order = 0 AND mcrew.job = 'Director'
ORDER BY movie.title;

-- Section3

SELECT p.person_name AS Name,count(*) AS count_of_movies
FROM movie_cast
JOIN person AS p ON p.person_id = movie_cast.person_id
WHERE movie_cast.cast_order = 0
GROUP BY p.person_name
HAVING count_of_movies
ORDER BY count_of_movies DESC,p.person_name ASC;

-- Section4

SELECT g.genre_name AS genre,AVG(m.vote_average) AS avg_rating,MAX(m.vote_average) AS max_rating,
       MIN(m.vote_average) AS min_rating
FROM movie_genres
JOIN movie m on movie_genres.movie_id = m.movie_id
JOIN genre g on movie_genres.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY avg_rating DESC;

-- Section5

SELECT p1.person_name AS "person #1",p2.person_name AS "person #2",count(*) AS movies_played_together
FROM movie_cast as mc1
JOIN movie_cast mc2 on mc1.movie_id = mc2.movie_id AND mc1.person_id < mc2.person_id
JOIN person p1 on mc1.person_id = p1.person_id
JOIN person p2 on mc2.person_id = p2.person_id
GROUP BY p1.person_name, p2.person_name
HAVING count(*) > 1
ORDER BY movies_played_together DESC ,`person #1`, `person #2`
LIMIT 10;
