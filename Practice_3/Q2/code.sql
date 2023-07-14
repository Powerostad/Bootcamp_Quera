-- Section1
select p_title as p_title,c_title as c_title
from (select p.title as p_title,c.title as c_title, count(*) as count
from submissions
join problems p on submissions.problem_id = p.id
join contests c on c.id = p.contest_id
group by p.title,c.title
order by count desc,p.title,c.title) as sub;
-- Section2
select c2.title as title, count(distinct u.id)  as amount
    from users as u
    join submissions s on u.id = s.user_id
    join problems p on p.id = s.problem_id
    join contests c2 on c2.id = p.contest_id
    group by c2.id,c2.title
    order by amount desc,c2.title ;
-- Section3
select  name,(
    select sum(score1) from (
        select max(score) as score1
        from submissions
        join problems p on p.id = submissions.problem_id
        join contests c2 on c2.id = p.contest_id
        where submissions.user_id = u.id  and c2.title = 'mahale'
        group by p.contest_id,submissions.problem_id
                           ) as score ) as score
from users u
having score is not null
order by score desc,name ;
-- Section4
select name,(
    select coalesce(sum(score1),0) from (
        select max(score) as score1
        from submissions
        join problems p on p.id = submissions.problem_id
        where u.id = submissions.user_id
        group by p.contest_id,submissions.problem_id
                           ) as sub
    ) as score
from users as u
order by score desc ,name;
-- Section5
update contests
set title = 'Mosabeghe Mahale'
where title = 'mahale';

-- Section6
delete from contests as c
where not exists(
    select 1 from submissions
             join problems p on p.id = submissions.problem_id
             where p.contest_id = c.id
);