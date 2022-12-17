--call insert_data_authorization('test2', 'test2');

call poll_admin.insert_data_user('test', 'test', 1);

call poll_admin.insert_data_category('Test category');

call poll_admin.insert_data_poll_create('Poll test', 'Poll test description', true, 1, 1);

call poll_admin.insert_data_question('Question text', 1);

call poll_admin.insert_data_option('Option text', 1);

call poll_admin.insert_data_answer(1, 1);

call poll_admin.update_quantity_option(1);

call poll_admin.update_login_authorization('new_login', 1);

call poll_admin.update_password_authorization('new_password', 1);

call poll_admin.update_text_question('new_text', 1);

call poll_admin.update_content_category('new_content', 1);

call poll_admin.update_poll_status(true, 1);

call poll_admin.update_poll_date_closed(LOCALTIMESTAMP(0), 1);

call poll_admin.delete_selected_category('1');

call poll_admin.delete_selected_poll('Poll test');

call poll_programmer.insert_100_000_data_category();

call poll_programmer.delete_100_000_data_category();

call poll_programmer.export_category_by_id(200000, 210000, 'C:/Users/User/Desktop/Course_project_DB/Database/data_in_xml_range.xml');

call poll_programmer.import_category_data('C:/Users/User/Desktop/Course_project_DB/Database/data_in_xml_range.xml');
