
-- Section1

select family_name,given_name as name,birth_date,
      if(t.team_name in ('Yugoslavia','Serbia and Montenegro'),'Serbia',t.team_name) as team_name
from players
join squads s on players.player_id = s.player_id
join teams t on s.team_id = t.team_id
where family_name like '%ić'
and t.team_name != 'Croatia'
order by t.team_name,birth_date,family_name,given_name;

-- Section2

select if(team_name='West Germany','Germany',team_name) as team_name,sum(
    case when ts.position = 1 then 4
    when ts.position = 2 then 3
    when ts.position = 3 then 2
    when ts.position = 4 then 1
    else 0
    end
    ) as total_score
from teams
join tournament_standings ts on teams.team_id = ts.team_id
group by if(team_name='West Germany','Germany',team_name)
order by total_score desc ,team_name;

-- Section3

select concat(given_name,' ',family_name) as full_name,m.match_name,t.team_name
,t2.year as tournament_year,(m.match_date - datediff(birth_date,'1970-01-01')) as age
from players
join player_appearances pa on players.player_id = pa.player_id
join matches m on pa.match_id = m.match_id
join teams t on pa.team_id = t.team_id
join tournaments t2 on m.tournament_id = t2.tournament_id

order by age desc
limit 20;

-- Section4

   your fourth query here