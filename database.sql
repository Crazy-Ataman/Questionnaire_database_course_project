create user poll_programmer with password 'poll_programmer';
alter user poll_programmer createrole noinherit replication;
grant all privileges on database poll to poll_programmer;
alter user poll_programmer with superuser;
 
create tablespace poll_tablespace owner poll_programmer
location 'C:\Users\User\Desktop\Course_project_DB\Database\Tablespaces';

create database poll
    with owner = poll_programmer
    encoding = 'UTF8'
    lc_collate = 'Russian_Russia.1251'
    lc_ctype = 'Russian_Russia.1251'
    tablespace = poll_tablespace
-- 	-1 = no limits
    connection limit = -1 
    template = template0;

alter database poll owner to poll_programmer;
grant all privileges on database poll to poll_programmer;

create user poll_admin with password 'poll_admin';
create user poll_user with password 'poll_user';

revoke create on schema public from public;
revoke all privileges on database poll from poll_user;
revoke all privileges on database poll from poll_admin;

alter user poll_user set search_path = poll_user;
alter user poll_admin set search_path = poll_admin;

create schema if not exists poll_programmer;
create schema if not exists poll_admin;
create schema if not exists poll_user;

revoke all privileges on schema poll_user from poll_user;
revoke all privileges on schema poll_admin from poll_admin;

grant usage on schema poll_user to poll_user;
grant usage on schema poll_admin to poll_admin;

grant execute on all routines in schema poll_admin to poll_admin;
grant execute on all routines in schema poll_user to poll_user;