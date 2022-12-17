insert into "authorization"(login, password, is_admin) values
	('test', 'test', false);

insert into category(content) values
    ('category_for_test');

insert into "user"(first_name, last_name, auth_id_fk) values
    ('first_name', 'last_name', 1);

insert into poll(description, date_created, date_closed, is_open, user_id_fk, category_id_fk) values
    ('description: bla-bla-bla', '2016-06-22 19:10:25', '2016-06-22 20:10:25', true, 1, 1);

insert into question(text, poll_id_fk) values
    ('question_for_test', 1);

insert into "option"(text, quantity, poll_id_fk) values
    ('option_for_test', 0, 1);

insert into answer(date_answer, user_id_fk, option_id_fk) values
    ('2016-06-22 19:25:34', 1, 1);