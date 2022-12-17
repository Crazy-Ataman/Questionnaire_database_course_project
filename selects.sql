-- Check postgreSQL
select *
from pg_stat_activity
where datname = 'poll';

select *
from pg_tablespace;

select *
from pg_database;

-- Check tables
select *
from answer;

select *
from "authorization";

select *
from category;

select *
from "option";

select *
from poll;

select *
from question;

select *
from "user";