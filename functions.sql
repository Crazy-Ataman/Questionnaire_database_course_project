-- selects functions
create or replace function poll_admin.select_authorizations(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "authorization";
        return ref;
    end;
$$;

-- drop function if exists select_authorizations;


create or replace function poll_admin.select_users(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "user";
        return ref;
    end;
$$;

-- drop function if exists select_users;


create or replace function poll_admin.select_polls(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from poll;
        return ref;
    end;
$$;

-- drop function if exists select_polls;


create or replace function poll_admin.select_questions(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from question;
        return ref;
    end;
$$;

-- drop function if exists select_questions;


create or replace function poll_admin.select_options(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "option";
        return ref;
    end;
$$;

-- drop function if exists select_options;


create or replace function poll_admin.select_answers(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from answer;
        return ref;
    end;
$$;

-- drop function if exists select_answers;


create or replace function poll_admin.select_categories(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from category;
        return ref;
    end;
$$;

-- drop function if exists select_categories;


create or replace function poll_admin.find_auth_id(ref refcursor, login_p varchar(50))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select auth_id from "authorization" where login = login_p;
        return ref;
    end;
$$;

-- drop function if exists find_auth_id;


create or replace function poll_user.get_auth_info(ref refcursor, auth_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "authorization" where auth_id = auth_id_p;
        return ref;
    end;
$$;

create or replace function poll_admin.get_auth_info(ref refcursor, auth_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "authorization" where auth_id = auth_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_auth_info;

create or replace function poll_user.get_user_info(ref refcursor, auth_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "user" where auth_id_fk = auth_id_p;
        return ref;
    end;
$$;


create or replace function poll_admin.get_user_info(ref refcursor, auth_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select * from "user" where auth_id_fk = auth_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_user_info;

create or replace function poll_user.get_polls_name(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select name from poll;
        return ref;
    end;
$$;

create or replace function poll_admin.get_polls_name(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select name from poll;
        return ref;
    end;
$$;

-- drop function if exists get_polls_name;


create or replace function poll_admin.get_categories_content(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select content from category;
        return ref;
    end;
$$;


-- drop function if exists get_categories_content;

create or replace function poll_admin.get_categories_content_pagination(ref refcursor, page int, limit_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select content from category order by category_id limit limit_p offset (page-1)*limit_p;
        return ref;
    end;
$$;

-- drop function if exists get_categories_content_pagination;

create or replace function poll_user.get_questions_text(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text from question;
        return ref;
    end;
$$;

create or replace function poll_admin.get_questions_text(ref refcursor)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text from question;
        return ref;
    end;
$$;

-- drop function if exists get_questions_text;


create or replace function poll_admin.find_category_id(ref refcursor, content_p varchar(50))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select category_id from category where content = content_p;
        return ref;
    end;
$$;

-- drop function if exists find_category_id;


create or replace function poll_admin.find_user_id(ref refcursor, auth_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select user_id from "user" where auth_id_fk = auth_id_p;
        return ref;
    end;
$$;

-- drop function if exists find_user_id;

create or replace function poll_user.find_poll_id(ref refcursor, poll_name varchar(100))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select poll_id from poll where name = poll_name;
        return ref;
    end;
$$;

create or replace function poll_admin.find_poll_id(ref refcursor, poll_name varchar(100))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select poll_id from poll where name = poll_name;
        return ref;
    end;
$$;

-- drop function if exists find_poll_id;

create or replace function poll_user.find_question_id(ref refcursor, question_text varchar(250))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select question_id from question where text = question_text;
        return ref;
    end;
$$;

create or replace function poll_admin.find_question_id(ref refcursor, question_text varchar(250))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select question_id from question where text = question_text;
        return ref;
    end;
$$;

-- drop function if exists find_question_id;

create or replace function poll_user.get_poll_status(ref refcursor, poll_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select is_open from poll where poll_id = poll_id_p;
        return ref;
    end;
$$;

create or replace function poll_admin.get_poll_status(ref refcursor, poll_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select is_open from poll where poll_id = poll_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_poll_status;

create or replace function poll_user.get_option_text(ref refcursor, question_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text from "option" where question_id_fk = question_id_p;
        return ref;
    end;
$$;

create or replace function poll_admin.get_option_text(ref refcursor, question_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text from "option" where question_id_fk = question_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_option_text;


create or replace function poll_admin.get_question_texts_by_poll_id(ref refcursor, poll_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text from question where poll_id_fk = poll_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_question_text_by_poll_id;


create or replace function poll_admin.get_option_texts_by_question_id(ref refcursor, question_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text, question_id_fk from "option" where question_id_fk = question_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_option_texts_by_question_id;


create or replace function poll_admin.find_option_id(ref refcursor, option_text varchar(250))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select option_id from "option" where text = option_text;
        return ref;
    end;
$$;

-- drop function if exists find_option_id;


create or replace function poll_admin.find_question_id_by_poll_id(ref refcursor, poll_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select question_id from question where poll_id_fk = poll_id_p;
        return ref;
    end;
$$;

-- drop function if exists find_question_id_by_poll_id;


create or replace function poll_admin.get_text_and_quantity_by_question_id(ref refcursor, question_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select text, quantity from "option" where question_id_fk = question_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_text_and_quantity_by_question_id;


create or replace function poll_admin.find_option_id_by_question_id(ref refcursor, question_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select option_id from "option" where question_id_fk = question_id_p;
        return ref;
    end;
$$;

-- drop function if exists find_option_id;


create or replace function poll_admin.get_option_id_from_answer_by_user_id(ref refcursor, user_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select option_id_fk from answer where user_id_fk = user_id_p;
        return ref;
    end;
$$;

-- drop function if exists get_option_id_from_answer_by_user_id;

create or replace function poll_admin.poll_already_have_question(ref refcursor, poll_id_p int)
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select question_id from question where poll_id_fk = poll_id_p;
        return ref;
    end;
$$;

-- drop function if exists poll_already_have_question;

create or replace function poll_admin.login_in_used(ref refcursor, login_p varchar(50))
returns refcursor
language plpgsql
security definer as $$
    begin
        open ref for select login from "authorization" where login = login_p;
        return ref;
    end;
$$;

-- drop function if exists login_in_used;

alter function poll_admin.login_in_used(ref refcursor, login_p varchar(50)) owner to poll_programmer;
alter function poll_admin.select_authorizations(refcursor) owner to poll_programmer;
alter function poll_admin.select_categories(refcursor) owner to poll_programmer;
alter function poll_admin.select_polls(refcursor) owner to poll_programmer;
alter function poll_admin.select_questions(refcursor) owner to poll_programmer;
alter function poll_admin.select_options(refcursor) owner to poll_programmer;
alter function poll_admin.select_users(refcursor) owner to poll_programmer;
alter function poll_admin.select_answers(refcursor) owner to poll_programmer;
alter function poll_admin.find_auth_id(ref refcursor, login_p varchar(50)) owner to poll_programmer;
alter function poll_admin.find_user_id(ref refcursor, auth_id_p int) owner to poll_programmer;
alter function poll_admin.find_poll_id(ref refcursor, poll_name varchar(100)) owner to poll_programmer;
alter function poll_admin.find_question_id(ref refcursor, question_text varchar(250)) owner to poll_programmer;
alter function poll_admin.get_poll_status(ref refcursor, poll_id_p int) owner to poll_programmer;
alter function poll_admin.get_option_text(ref refcursor, question_id_p int) owner to poll_programmer;
alter function poll_admin.get_question_texts_by_poll_id(ref refcursor, poll_id_p int) owner to poll_programmer;
alter function poll_admin.get_option_texts_by_question_id(ref refcursor, question_id_p int) owner to poll_programmer;
alter function poll_admin.find_option_id(ref refcursor, option_text varchar(250)) owner to poll_programmer;
alter function poll_admin.find_question_id_by_poll_id(ref refcursor, poll_id_p int) owner to poll_programmer;
alter function poll_admin.get_text_and_quantity_by_question_id(ref refcursor, question_id_p int) owner to poll_programmer;
alter function poll_admin.find_option_id_by_question_id(ref refcursor, question_id_p int) owner to poll_programmer;
alter function poll_admin.poll_already_have_question(ref refcursor, poll_id_p int) owner to poll_programmer;
alter function poll_admin.get_option_id_from_answer_by_user_id(ref refcursor, user_id_p int) owner to poll_programmer;
alter function poll_user.find_poll_id(ref refcursor, poll_name varchar(100)) owner to poll_programmer;
alter function poll_user.find_question_id(ref refcursor, question_text varchar(250)) owner to poll_programmer;
alter function poll_user.get_poll_status(ref refcursor, poll_id_p int) owner to poll_programmer;
alter function poll_user.get_option_text(ref refcursor, question_id_p int) owner to poll_programmer;
