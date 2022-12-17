create table if not exists poll_programmer.category (
    category_id serial primary key,
    content varchar(100) unique not null
) tablespace poll_tablespace;

create table if not exists poll_programmer."authorization" (
    auth_id serial primary key,
    login varchar(50) unique not null,
	password text not null,
	is_admin boolean default false
) tablespace poll_tablespace;

create table if not exists poll_programmer."user" (
    user_id serial primary key,
    first_name varchar(50) not null,
	last_name varchar(50) not null,
	auth_id_fk int references "authorization" (auth_id) unique
) tablespace poll_tablespace;

-- CURRENT_TIMESTAMP(0) - 0 is passed to get rid of the fractional digits
create table if not exists poll_programmer.poll (
    poll_id serial primary key,
    name varchar(100) unique not null,
    description varchar(250),
	date_created timestamp not null default CURRENT_TIMESTAMP(0),
	date_closed timestamp,
	is_open boolean,
	user_id_fk int references "user" (user_id),
	category_id_fk int references category (category_id) unique
) tablespace poll_tablespace;

create table if not exists poll_programmer.question (
    question_id serial primary key,
    text varchar(250) unique not null,
	poll_id_fk int references poll (poll_id) unique
) tablespace poll_tablespace;

create table if not exists poll_programmer."option" (
    option_id serial primary key,
    text varchar(250) unique not null,
	quantity int default 0,
	question_id_fk int references question (question_id),
	constraint quantity_non_negative check (quantity >= 0)
) tablespace poll_tablespace;

create table if not exists poll_programmer.answer (
    answer_id serial primary key,
    date_answer timestamp not null default CURRENT_TIMESTAMP(0),
	user_id_fk int references "user" (user_id),
	option_id_fk int references "option" (option_id)
) tablespace poll_tablespace;

alter table poll_programmer.category owner to poll_programmer;

alter table poll_programmer."authorization" owner to poll_programmer;

alter table poll_programmer."user" owner to poll_programmer;

alter table poll_programmer.poll owner to poll_programmer;

alter table poll_programmer.question owner to poll_programmer;

alter table poll_programmer."option" owner to poll_programmer;

alter table poll_programmer.answer owner to poll_programmer;

-- add cascade delete

-- unnecessary
-- alter table poll
-- drop constraint "poll_category_id_fk_fkey",
-- add constraint "poll_category_id_fk_fkey"
--   foreign key ("category_id_fk")
--   references category(category_id)
--   on delete cascade;

alter table poll_programmer.question
drop constraint "question_poll_id_fk_fkey",
add constraint "question_poll_id_fk_fkey"
  foreign key ("poll_id_fk")
  references poll(poll_id)
  on delete cascade;

alter table poll_programmer."option"
drop constraint "option_question_id_fk_fkey",
add constraint "option_question_id_fk_fkey"
  foreign key ("question_id_fk")
  references question(question_id)
  on delete cascade;

alter table poll_programmer.answer
drop constraint "answer_option_id_fk_fkey",
add constraint "answer_option_id_fk_fkey"
  foreign key ("option_id_fk")
  references "option"(option_id)
  on delete cascade;

alter table answer enable row level security;
alter table "option" enable row level security;
alter table poll enable row level security;
alter table question enable row level security;
alter table "user" enable row level security;
alter table "authorization" enable row level security;
alter table "category" enable row level security;

create policy select_all_in_authorization
    on "authorization" for select
    using (true);

create policy select_all_in_user
    on "user" for select
    using (true);

create policy select_all_in_category
    on "category" for select
    using (true);

create policy select_all_in_poll
    on poll for select
    using (true);

create policy select_all_in_question
    on question for select
    using (true);

create policy select_all_in_option
    on "option" for select
    using (true);

create policy select_all_in_answer
    on answer for select
    using (true);

create policy insert_category
    on "category" for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy insert_option
    on "option" for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy insert_poll
    on poll for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy insert_question
    on question for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy insert_user
    on "user" for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy insert_authorization
    on "authorization" for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy insert_answer
    on answer for insert
    with check (current_user = 'poll_programmer' or current_user = 'poll_admin');

grant insert on "category" to poll_admin;
grant insert on "option" to poll_admin;
grant insert on poll to poll_admin;
grant insert on question to poll_admin;
grant insert on "user" to poll_admin;
grant insert on "authorization" to poll_admin;
grant insert on answer to poll_admin;

create policy update_category
    on "category" for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy update_option
    on "option" for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy update_poll
    on poll for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy update_question
    on question for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy update_user
    on "user" for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy update_authorization
    on "authorization" for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy update_answer
    on answer for update
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

grant update on "category" to poll_admin;
grant update on "option" to poll_admin;
grant update on poll to poll_admin;
grant update on question to poll_admin;
grant update on "user" to poll_admin;
grant update on "authorization" to poll_admin;
grant update on answer to poll_admin;

create policy delete_category
    on "category" for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy delete_option
    on "option" for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy delete_poll
    on poll for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy delete_question
    on question for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy delete_user
    on "user" for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy delete_authorization
    on "authorization" for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

create policy delete_answer
    on answer for delete
    using (current_user = 'poll_programmer' or current_user = 'poll_admin');

grant delete on "category" to poll_admin;
grant delete on "option" to poll_admin;
grant delete on poll to poll_admin;
grant delete on question to poll_admin;
grant delete on "user" to poll_admin;
grant delete on "authorization" to poll_admin;
grant delete on answer to poll_admin;

-- drop function if exists poll_programmer.alert_is_admin_change() cascade;

create function poll_programmer.alert_is_admin_change()
    returns trigger
    language plpgsql

    as $$
    declare
        msg text := 'Column is_admin in table authorization has been changed.';
    begin

        create table demo(str text);
        insert into demo values(msg);

        copy demo to 'C:/Users/User/Desktop/Course_project_DB/Database/alert.txt';

--         if current_user = 'poll_admin' then
--             raise notice 'You are now poll_admin';
--         else
--             raise notice 'You are now poll_programmer';
--         end if;
        drop table if exists demo;

        return old;
    end;
    $$;


create trigger update_is_admin
    after update on "authorization" for each row
    execute procedure poll_programmer.alert_is_admin_change();


-- drop policy if exists select_all_in_authorization on "authorization";
-- drop policy if exists select_all_in_user on "user";
-- drop policy if exists select_all_in_category on "category";
-- drop policy if exists select_all_in_poll on poll;
-- drop policy if exists select_all_in_question on question;
-- drop policy if exists select_all_in_option on "option";
-- drop policy if exists select_all_in_answer on answer;


-- change column type to text
alter table poll_programmer."authorization"
    alter column password type text;

-- reset counters for tables
-- alter sequence authorization_auth_id_seq restart with 2;
--
-- alter sequence user_user_id_seq restart with 2;
--
-- alter sequence category_category_id_seq restart with 2;
--
-- alter sequence question_question_id_seq restart with 1;
--
-- alter sequence option_option_id_seq restart with 1;