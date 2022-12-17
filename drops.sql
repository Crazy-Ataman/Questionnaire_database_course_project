-- kill all session connected to database
select 
   pg_terminate_backend(pg_stat_activity.pid)
from pg_stat_activity
where
   pg_stat_activity.datname = 'poll'
and pid <> pg_backend_pid();

drop database if exists poll;

drop tablespace if exists poll_tablespace;

drop user if exists poll_user;
drop user if exists poll_admin;

drop schema if exists poll_admin cascade;
drop schema if exists poll_user cascade;