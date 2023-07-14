
-- Section1
select p.platform_name as platform_name,avg(region_sales.num_sales) as Average
from region_sales
join game_platform gp on gp.id = region_sales.game_platform_id
join platform p on p.id = gp.platform_id
group by p.platform_name
order by Average DESC;

-- Section2


select game.game_name, p.platform_name as platform_name,gp.release_year,p2.publisher_name, sum(region_sales.num_sales) as global_sales
from region_sales
join game_platform gp on gp.id = region_sales.game_platform_id
join platform p on p.id = gp.platform_id
join game_publisher g on gp.game_publisher_id = g.id
join game  on game.id = g.game_id
join publisher p2 on g.publisher_id = p2.id
group by game.game_name, p.platform_name, gp.release_year, p2.publisher_name
order by global_sales DESC
limit 20;

-- Section3

select distinct g.game_name,COUNT(distinct p.platform_name) as platform_count
from game_platform
join platform p on game_platform.platform_id = p.id
join game_publisher gp on game_platform.game_publisher_id = gp.id
join game g on gp.game_id = g.id
group by g.game_name
having platform_count > 5
order by platform_count desc ;

-- Section4

select platform.platform_name as platform,g3.genre_name as genre,dense_rank() over (
    partition by platform.platform_name
    order by sum(rs.num_sales) desc ) as genre_in_platform_rank,
    sum(rs.num_sales) as genre_sale,
    dense_rank() over (order by sum(rs.num_sales) desc) as total_rank
from platform
join game_platform gp on platform.id = gp.platform_id
join game_publisher g on g.id = gp.game_publisher_id
join game g2 on g2.id = g.game_id
join genre g3 on g3.id = g2.genre_id
join region_sales rs on gp.id = rs.game_platform_id
group by g3.genre_name, platform.platform_name
order by genre_sale desc ,platform,genre ;