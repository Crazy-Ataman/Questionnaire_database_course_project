-- inserts procedures
create or replace procedure poll_user.insert_data_authorization(login varchar(50), password text)
language plpgsql
security definer as $$
    begin
        insert into "authorization" as auth_check_on_duplicate(login, password)
        select *
        from (values (login, password)) v(login, password)
        where not exists(select from "authorization" as b where b.login = v.login)
        on conflict do nothing;
    end;
$$;

create or replace procedure poll_admin.insert_data_authorization(login varchar(50), password text)
language plpgsql
security definer as $$
    begin
        insert into "authorization" as auth_check_on_duplicate(login, password)
        select *
        from (values (login, password)) v(login, password)
        where not exists(select from "authorization" as b where b.login = v.login)
        on conflict do nothing;
    end;
$$;

-- drop procedure if exists insert_data_authorization;
create or replace procedure poll_user.insert_data_user(first_name varchar(50), last_name varchar(50), auth_id_fk int)
language plpgsql
security definer as $$
    begin
        insert into "user"(first_name, last_name, auth_id_fk) values
            (first_name, last_name, auth_id_fk);
    end;
$$;

create or replace procedure poll_admin.insert_data_user(first_name varchar(50), last_name varchar(50), auth_id_fk int)
language plpgsql
security definer as $$
    begin
        insert into "user"(first_name, last_name, auth_id_fk) values
            (first_name, last_name, auth_id_fk);
    end;
$$;

-- drop procedure if exists insert_data_user;


create or replace procedure poll_admin.insert_data_category(content varchar(100))
language plpgsql
security definer as $$
    begin
        insert into category(content) values (content);
    end;
$$;

-- drop procedure if exists insert_data_category;


create or replace procedure poll_admin.insert_data_poll_create(name varchar(100),
                                             description varchar(250),
                                             is_open boolean,
                                             user_id_fk int,
                                             category_id_fk int)
language plpgsql
security definer as $$
    begin
        insert into poll(name, description, is_open, user_id_fk, category_id_fk)
        values (name, description, is_open, user_id_fk, category_id_fk);
    end;
$$;

-- drop procedure if exists insert_data_poll_create;


create or replace procedure poll_admin.insert_data_question(text_p varchar(250), poll_id_p int)
language plpgsql
security definer as $$
    begin
        insert into question(text, poll_id_fk) values (text_p, poll_id_p);
    end;
$$;

-- drop procedure if exists insert_data_question;


create or replace procedure poll_admin.insert_data_option(text_p varchar(250), question_id_p int)
language plpgsql
security definer as $$
    begin
        insert into option(text, question_id_fk) values (text_p, question_id_p);
    end;
$$;

-- drop procedure if exists insert_data_option;

create or replace procedure poll_user.insert_data_answer(user_id_fk int, option_id_fk int)
language plpgsql
security definer as $$
    begin
        insert into answer(user_id_fk, option_id_fk) values (user_id_fk, option_id_fk);
    end;
$$;

create or replace procedure poll_admin.insert_data_answer(user_id_fk int, option_id_fk int)
language plpgsql
security definer as $$
    begin
        insert into answer(user_id_fk, option_id_fk) values (user_id_fk, option_id_fk);
    end;
$$;

-- drop procedure if exists insert_data_answer;


-- try to insert 100_000 categories
create or replace procedure poll_programmer.insert_100_000_data_category()
language plpgsql
security definer as $$
    begin
        for i in 1..100000 loop
            insert into poll_programmer.category(content) values ('content' || i::varchar);
        end loop;
    end;
$$;

-- drop procedure if exists insert_100_000_data_category;
;

-- delete 100_000 rows
create or replace procedure poll_programmer.delete_100_000_data_category()
language plpgsql
security definer as $$
    begin
        for i in 1..100000 loop
            delete from poll_programmer.category where content = 'content' || i::varchar;
        end loop;
    end;
$$;

-- drop procedure if exists delete_100_000_data_category;

-- updates procedures
create or replace procedure poll_admin.update_quantity_option(option_id_p int)
language plpgsql
security definer as $$
    begin
        update "option" set quantity = quantity + 1 where option_id = option_id_p;
    end;
$$;

-- drop procedure if exists update_quantity_option;

create or replace procedure poll_user.update_login_authorization(new_login varchar(50), auth_id_p int)
language plpgsql
security definer as $$
    begin
        update "authorization" set login = new_login where auth_id = auth_id_p;
    end;
$$;

create or replace procedure poll_admin.update_login_authorization(new_login varchar(50), auth_id_p int)
language plpgsql
security definer as $$
    begin
        update "authorization" set login = new_login where auth_id = auth_id_p;
    end;
$$;

-- drop procedure if exists update_login_authorization;

create or replace procedure poll_user.update_password_authorization(new_password text, auth_id_p int)
language plpgsql
security definer as $$
    begin
        update "authorization" set password = new_password where auth_id = auth_id_p;
    end;
$$;

create or replace procedure poll_admin.update_password_authorization(new_password text, auth_id_p int)
language plpgsql
security definer as $$
    begin
        update "authorization" set password = new_password where auth_id = auth_id_p;
    end;
$$;

-- drop procedure if exists update_password_authorization;


create or replace procedure poll_admin.update_text_question(new_text varchar(250), question_id_p int)
language plpgsql
security definer as $$
    begin
        update question set text = new_text where question_id = question_id_p;
    end;
$$;

-- drop procedure if exists update_text_question;


create or replace procedure poll_admin.update_content_category(new_content varchar(250), category_id_p int)
language plpgsql
security definer as $$
    begin
        update category set content = new_content where category_id = category_id_p;
    end;
$$;

-- drop procedure if exists update_content_category;


create or replace procedure poll_admin.update_poll_status(new_status bool, poll_id_p int)
language plpgsql
security definer as $$
    begin
        update poll set is_open = new_status where poll_id = poll_id_p;
    end;
$$;

-- drop procedure if exists update_poll_status;


create or replace procedure poll_admin.update_poll_date_closed(date_closed_p timestamp, poll_id_p int)
language plpgsql
security definer as $$
    begin
        update poll set date_closed = date_closed_p where poll_id = poll_id_p;
    end;
$$;

-- drop procedure if exists update_poll_date_closed;


create or replace procedure poll_admin.delete_selected_category(content_p varchar(100))
language plpgsql
security definer as $$
    begin
        delete from category where content = content_p;
    end;
$$;

-- drop procedure if exists delete_selected_category;


create or replace procedure poll_admin.delete_selected_poll(name_p varchar(100))
language plpgsql
security definer as $$
    begin
        delete from poll where name = name_p;
    end;
$$;

-- drop procedure if exists delete_selected_poll;

alter procedure poll_admin.insert_data_authorization(varchar(50), text) owner to poll_programmer;
alter procedure poll_admin.insert_data_category(varchar(100)) owner to poll_programmer;
alter procedure poll_admin.insert_data_poll_create(name varchar(100), description varchar(250), is_open boolean, user_id_fk int, category_id_fk int) owner to poll_programmer;
alter procedure poll_admin.insert_data_question(text_p varchar(250), poll_id_p int) owner to poll_programmer;
alter procedure poll_admin.insert_data_option(text_p varchar(250), question_id_p int) owner to poll_programmer;
alter procedure poll_admin.insert_data_answer(user_id_fk int, option_id_fk int) owner to poll_programmer;
alter procedure poll_admin.update_quantity_option(option_id_p int) owner to poll_programmer;
alter procedure poll_admin.update_login_authorization(new_login varchar(50), auth_id_p int) owner to poll_programmer;
alter procedure poll_admin.update_password_authorization(new_password text, auth_id_p int) owner to poll_programmer;
alter procedure poll_admin.update_text_question(new_text varchar(250), question_id_p int) owner to poll_programmer;
alter procedure poll_admin.update_content_category(new_content varchar(250), category_id_p int) owner to poll_programmer;
alter procedure poll_admin.update_poll_status(new_status bool, poll_id_p int) owner to poll_programmer;
alter procedure poll_admin.update_poll_date_closed(date_closed_p timestamp, poll_id_p int) owner to poll_programmer;
alter procedure poll_admin.delete_selected_category(content_p varchar(100)) owner to poll_programmer;
alter procedure poll_admin.delete_selected_poll(name_p varchar(100)) owner to poll_programmer;

-- procedure for export data
-- create or replace procedure poll_programmer.export_database_with_schemas()
-- language plpgsql
-- security definer as $$
--     begin
--         copy (
--             select query_to_xml(E'select database_to_xml_and_xmlschema(true, true, \'\')', true, true, '')
--             )
--             to 'E:/Labs/Course_project_DB/Database/database_in_xml.xml';
--     end;
-- $$;

-- drop procedure if exists export_database_with_schemas;


create or replace procedure poll_programmer.export_category_by_id(category_id_p_from int, category_id_p_to int, filepath text)
language plpgsql
security definer as $$
    begin
--         execute format('copy (
--             select query_to_xml(''select * from category where category_id between %s and %s;'', false, false, '''')
--             )
--             to %L;', $1, $2, $3);


        execute format('copy (select xmlelement(name category, xmlforest(category_id, content)) from category where category_id between %s and %s)
            to %L;', category_id_p_from, category_id_p_to, filepath);


    end;
$$;





-- drop procedure if exists export_category_by_id;

-- alter procedure poll_programmer.export_database_with_schemas() owner to poll_programmer;
alter procedure poll_programmer.export_category_by_id(category_id_p_from int, category_id_p_to int, filepath text) owner to poll_programmer;


-- procedure for import data
create or replace procedure poll_programmer.import_category_data(filepath text)
language plpgsql
security definer as $$
    begin
        create table demo(t xml);
        execute format('copy demo from %L', filepath);

        insert into category (category_id, content)
                    select category_id::text::int, content::text
                    from demo
                    cross join unnest(xpath('category/category_id/text()', demo.t)) as a(category_id)
                    cross join unnest(xpath('category/content/text()', demo.t)) as b(content);

        drop table if exists demo;
    end;
$$;

-- drop procedure if exists import_category_data;

alter procedure poll_programmer.import_category_data(filepath text) owner to poll_programmer;



select prosrc from pg_proc where proname='import_category_data';

select * from pg_get_function_arguments();

SELECT
    *
FROM
    information_schema.routines
WHERE
    routine_type = 'FUNCTION'
AND
    routine_schema = 'poll_admin';

SELECT
    routine_schema,
    routine_name
FROM
    information_schema.routines
WHERE
    routine_type = 'PROCEDURE';

