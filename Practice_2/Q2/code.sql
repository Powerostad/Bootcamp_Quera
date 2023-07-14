
-- Section1

SELECT family_name,given_name AS name
FROM players
WHERE family_name LIKE '%pir%'
OR given_name LIKE '%pir%'
ORDER BY family_name ASC;

-- Section2

SELECT shirt_number,COUNT(*) AS count_shirt_number
FROM player_appearances
GROUP BY shirt_number
HAVING count_shirt_number > 1000
ORDER BY count_shirt_number DESC;

-- Section3

SELECT DISTINCT family_name,given_name AS name
FROM players
JOIN award_winners AS a1 ON players.player_id = a1.player_id
JOIN award_winners AS a2 ON players.player_id = a2.player_id
WHERE
a1.award_id = 'A-8'
AND a2.award_id IN ('A-1', 'A-2', 'A-3', 'A-4','A-5','A-6','A-7')
ORDER BY family_name ASC;
