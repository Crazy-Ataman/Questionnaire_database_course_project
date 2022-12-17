-- start a transaction
begin;
select poll_admin.select_authorizations('authorizations_cur');
fetch all in "authorizations_cur";
commit;

-- start a transaction
begin;
select poll_admin.select_users('users_cur');
fetch all in "users_cur";
commit;

-- start a transaction
begin;
select poll_admin.select_polls('polls_cur');
fetch all in "polls_cur";
commit;

-- start a transaction
begin;
select poll_admin.select_questions('questions_cur');
fetch all in "questions_cur";
commit;

-- start a transaction
begin;
select poll_admin.select_options('options_cur');
fetch all in "options_cur";
commit;

-- start a transaction
begin;
select poll_admin.select_answers('answers_cur');
fetch all in "answers_cur";
commit;

-- start a transaction
begin;
select poll_admin.select_categories('categories_cur');
fetch all in "categories_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_auth_id('find_auth_id_cur', 'test');
fetch all in "find_auth_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_auth_info('get_auth_info_cur', '1');
fetch all in "get_auth_info_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_user_info('get_user_info_cur', '1');
fetch all in "get_user_info_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_polls_name('get_polls_name_cur');
fetch all in "get_polls_name_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_categories_content('get_categories_content_cur');
fetch all in "get_categories_content_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_categories_content_pagination('get_categories_content_pagination_cur', 1, 1000);
fetch all in "get_categories_content_pagination_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_questions_text('get_questions_text_cur');
fetch all in "get_questions_text_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_category_id('find_category_id_cur', 'category2');
fetch all in "find_category_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_user_id('find_user_id_cur', 1);
fetch all in "find_user_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_poll_id('find_poll_id_cur', 'Poll test');
fetch all in "find_poll_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_question_id('find_question_id_cur', 'Question text2');
fetch all in "find_question_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_poll_status('get_poll_status_cur', 1);
fetch all in "get_poll_status_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_option_text('get_option_text_cur', 2);
fetch all in "get_option_text_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_question_texts_by_poll_id('get_question_texts_by_poll_id_cur', 1);
fetch all in "get_question_texts_by_poll_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_option_texts_by_question_id('get_option_texts_by_question_id_cur', 2);
fetch all in "get_option_texts_by_question_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_option_id('find_option_id_cur', '1ghdggdg');
fetch all in "find_option_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_question_id_by_poll_id('find_question_id_by_poll_id_cur', 1);
fetch all in "find_question_id_by_poll_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_text_and_quantity_by_question_id('get_text_and_quantity_by_question_id_cur', 1);
fetch all in "get_text_and_quantity_by_question_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.find_option_id_by_question_id('find_option_id_by_question_id_cur', 1);
fetch all in "find_option_id_by_question_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_option_id_from_answer_by_user_id('get_option_id_from_answer_by_user_id_cur', 1);
fetch all in "get_option_id_from_answer_by_user_id_cur";
commit;

-- start a transaction
begin;
select poll_admin.get_poll_status('get_poll_status_cur', 1);
fetch all in "get_poll_status_cur";
commit;