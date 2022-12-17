import psycopg2
import bcrypt
from config import config
from tkinter import Tk
from tkinter import PhotoImage
from tkinter import Toplevel
from tkinter import SOLID
from tkinter import StringVar
from tkinter import NW
from tkinter import Variable
from tkinter import Scrollbar
from tkinter import VERTICAL
from tkinter import RIGHT
from tkinter import ttk
from tkinter import Y
from tkinter import Listbox
from tkinter import SINGLE
import tkinter.messagebox
from tkinter.messagebox import showerror, showwarning, showinfo
from datetime import datetime, timezone
import matplotlib.pyplot as plt


auth_id_global = -1

def connect():
    """ Connect to the PostgreSQL database server """
    global conn
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')

def character_limit_50(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:50])

def character_limit_100(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:100])

def character_limit_250(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:250])

class Register_user():

    def __init__(self, root):
        self.root = root
        self.window_for_registration = Toplevel(self.root)

        self.window_for_registration.title("Registration")
        self.window_for_registration.geometry("450x600")
        self.window_for_registration.resizable(False, False)

        self.label_registration = ttk.Label(self.window_for_registration, text="Registration", font=("Arial", 14))
        self.label_registration.pack()

        self.frame_for_sign_up= ttk.Frame(self.window_for_registration, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.first_name = StringVar()
        self.label_first_name_reg = ttk.Label(self.frame_for_sign_up, text="First name", font=("Arial", 14))
        self.label_first_name_reg.pack()
        self.entry_first_name_reg = ttk.Entry(self.frame_for_sign_up, textvariable=self.first_name)
        self.entry_first_name_reg.pack(padx=8, pady= 8)

        self.last_name = StringVar()
        self.label_last_name_reg = ttk.Label(self.frame_for_sign_up, text="Last name", font=("Arial", 14))
        self.label_last_name_reg.pack()
        self.entry_last_name_reg = ttk.Entry(self.frame_for_sign_up, textvariable=self.last_name)
        self.entry_last_name_reg.pack(padx=8, pady= 8)
        

        self.login_reg = StringVar()
        self.password_reg = StringVar()
        self.password_reg_repeat = StringVar()

        self.label_login_reg = ttk.Label(self.frame_for_sign_up, text="Login", font=("Arial", 14))
        self.label_login_reg.pack()
        self.entry_login_reg = ttk.Entry(self.frame_for_sign_up, textvariable=self.login_reg)
        self.entry_login_reg.pack(padx=8, pady= 8)

        self.label_password_reg = ttk.Label(self.frame_for_sign_up, text="Password", font=("Arial", 14))
        self.label_password_reg.pack()
        self.entry_password_reg = ttk.Entry(self.frame_for_sign_up, textvariable=self.password_reg, show="*")
        self.entry_password_reg.pack(padx=8, pady= 8)

        self.label_password_reg_repeat = ttk.Label(self.frame_for_sign_up, text="Repeat password", font=("Arial", 14))
        self.label_password_reg_repeat.pack()
        self.entry_password_reg_repeat = ttk.Entry(self.frame_for_sign_up, textvariable=self.password_reg_repeat, show="*")
        self.entry_password_reg_repeat.pack(padx=8, pady= 8)

        def check_entries_reg(*args):
            if self.first_name.get()=="" or self.last_name.get()=="" or self.login_reg.get()=="" or self.password_reg.get()=="" or self.password_reg_repeat.get()=="" or self.password_reg.get()!=self.password_reg_repeat.get():
                self.button_register['state'] = 'disabled'
            else: 
                self.button_register['state'] = 'normal'

        self.first_name.trace("w", lambda *args: character_limit_50(self.first_name))
        self.first_name.trace_add("write", check_entries_reg)
        self.last_name.trace("w", lambda *args: character_limit_50(self.last_name))
        self.last_name.trace_add("write", check_entries_reg)

        self.login_reg.trace_add("write", check_entries_reg)
        self.login_reg.trace("w", lambda *args: character_limit_50(self.login_reg))
        self.password_reg.trace_add("write", check_entries_reg)
        self.password_reg_repeat.trace_add("write", check_entries_reg)

        def func_back_to_sign_in(window_for_registration):
            self.window_for_registration.grab_release()
            self.window_for_registration.destroy()

        def func_register(window_for_registration, login_reg, password_reg, first_name, last_name):
            try:
                bytes = password_reg.get().encode('utf-8')
                hashed_password = bcrypt.hashpw(bytes, bcrypt.gensalt())

                cur = conn.cursor()
                cur.execute('call poll_admin.insert_data_authorization(%s, %s)', (login_reg.get(), hashed_password.decode("utf-8")))

                cur.callproc('poll_admin.find_auth_id', ['auth_id_cur', login_reg.get()])
                auth_id_cur = conn.cursor('auth_id_cur')
                auth_id = auth_id_cur.fetchone()
                auth_id_cur.close()

                cur.execute('call poll_admin.insert_data_user(%s, %s, %s)', (first_name.get(), last_name.get(), int(auth_id[0])))
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                showerror(title="Error", message="Login already in use!")
                conn.rollback()
                return False

            func_back_to_sign_in(self.window_for_registration)


        self.button_register = ttk.Button(self.frame_for_sign_up, text="Register", state=["disabled"])
        self.button_register["command"] = lambda: func_register(self.window_for_registration, self.login_reg, self.password_reg, self.first_name, self.last_name)
        self.button_register.pack()

        self.button_back = ttk.Button(self.frame_for_sign_up, text="Back")
        self.button_back["command"] = lambda: func_back_to_sign_in(self.window_for_registration)
        self.button_back.pack()

        self.frame_for_sign_up.pack()
        self.window_for_registration.grab_set()


def check_user_status():
    try:
        cur = conn.cursor()
        
        cur.callproc('poll_admin.get_auth_info', ['get_auth_info_cur', auth_id_global])
        get_auth_info_cur = conn.cursor('get_auth_info_cur')
        auth_info = get_auth_info_cur.fetchone()
        get_auth_info_cur.close()
        cur.close()

        user_status = auth_info[3]
        if user_status:
            return True
        else:
            return False
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        showerror(title="Error", message="Wrong password or login!")
        return False
    
class Authorization_user():

    def check_login_and_password(self, *args):
        if self.login.get()=="" or self.password.get()=="":
            self.button_sign_in['state'] = 'disabled'
        else: 
            self.button_sign_in['state'] = 'normal'

    def __init__(self, root):
        self.root = root
        self.window_for_authorization = Toplevel(self.root)

        self.window_for_authorization.title("Authorization")
        self.window_for_authorization.geometry("400x450")
        self.window_for_authorization.resizable(False, False)

        self.label_authorization = ttk.Label(self.window_for_authorization, text="Authorization", font=("Arial", 14))
        self.label_authorization.pack()

        self.frame_for_sign_in= ttk.Frame(self.window_for_authorization, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.login = StringVar()
        self.password = StringVar()

        self.label_login = ttk.Label(self.frame_for_sign_in, text="Login", font=("Arial", 14))
        self.label_login.pack()
        self.entry_login = ttk.Entry(self.frame_for_sign_in, textvariable=self.login)
        self.entry_login.pack(padx=8, pady= 8)

        self.label_password = ttk.Label(self.frame_for_sign_in, text="Password", font=("Arial", 14))
        self.label_password.pack()
        self.entry_password = ttk.Entry(self.frame_for_sign_in, textvariable=self.password, show="*")
        self.entry_password.pack(padx=8, pady= 8)

        self.login.trace_add("write", self.check_login_and_password)
        self.login.trace("w", lambda *args: character_limit_50(self.login))
        self.password.trace_add("write", self.check_login_and_password)

        def check_authorization(login, password):
            bytes = password.get().encode('utf-8')

            try:
                cur = conn.cursor()
                cur.callproc('poll_admin.find_auth_id', ['auth_id_cur', login.get()])
                auth_id_cur = conn.cursor('auth_id_cur')
                auth_id = auth_id_cur.fetchone()
                auth_id_cur.close()
                
                cur.callproc('poll_admin.get_auth_info', ['get_auth_info_cur', int(auth_id[0])])
                get_auth_info_cur = conn.cursor('get_auth_info_cur')
                auth_info = get_auth_info_cur.fetchone()
                get_auth_info_cur.close()
                cur.close()

                password_from_db = auth_info[2].encode('utf-8')
                global auth_id_global
                auth_id_global = int(auth_id[0])

            except (Exception, psycopg2.DatabaseError) as error:
                showerror(title="Error", message="Wrong password or login!")
                return False
            
            if bcrypt.checkpw(bytes, password_from_db):
                root.deiconify()

                button_about_user = ttk.Button(text="About user", command=lambda: About_user(root))
                button_about_user.pack()


                if check_user_status():

                    button_сreate_poll = ttk.Button(text="Create poll", command=lambda: Create_poll(root))
                    button_сreate_poll.pack()

                    button_сreate_category = ttk.Button(text="Create category", command=lambda: Create_category(root))
                    button_сreate_category.pack()

                    button_сreate_question = ttk.Button(text="Create question", command=lambda: Create_question(root))
                    button_сreate_question.pack()

                    button_сreate_question = ttk.Button(text="Create option", command=lambda: Create_option(root))
                    button_сreate_question.pack()

                    button_poll_status = ttk.Button(text="Poll status", command=lambda: Poll_status(root))
                    button_poll_status.pack()

                    button_delete_category = ttk.Button(text="Delete category", command=lambda: Delete_category(root))
                    button_delete_category.pack()

                    button_delete_poll = ttk.Button(text="Delete poll", command=lambda: Delete_poll(root))
                    button_delete_poll.pack()

                    button_poll_result = ttk.Button(text="Poll result", command=lambda: Poll_result(root))
                    button_poll_result.pack()
                else:
                    poll_id_local = -1

                    def selected(event):
                        try:
                            cur = conn.cursor()

                            cur.callproc('poll_admin.find_poll_id', ['find_poll_id_cur', combobox_polls.get()])
                            find_poll_id_cur = conn.cursor('find_poll_id_cur')
                            poll_id = find_poll_id_cur.fetchone()
                            poll_id = int(poll_id[0])
                            poll_id_local = poll_id
                            find_poll_id_cur.close()

                            cur.close()

                        except (Exception, psycopg2.DatabaseError) as error:
                            conn.rollback()
                            print(error)
                            return False

                        Start_polling(root, poll_id_local)

                    label_choose_a_poll = ttk.Label(text="Select a poll to vote", font=("Arial", 14))
                    label_choose_a_poll.pack() 

                    combobox_polls = ttk.Combobox(values=get_polls_name(), state="readonly")
                    combobox_polls.pack()
                    combobox_polls.bind("<<ComboboxSelected>>", selected)

                    # button_start_polling = ttk.Button(text="Let's poll!", command=lambda: Start_polling(root, poll_id_local), state=["disabled"])
                    # button_start_polling.pack()
                    




                    

                self.window_for_authorization.grab_release()
                self.window_for_authorization.destroy()
            else:
                showerror(title="Error", message="Wrong password or login!")

        self.button_sign_up = ttk.Button(self.frame_for_sign_in, text="Sign up", command=lambda: Register_user(root))
        self.button_sign_up.pack()
        self.button_sign_in = ttk.Button(self.frame_for_sign_in, text="Sign in", command=lambda: check_authorization(self.login, self.password), state=["disabled"])
        self.button_sign_in.pack()

        self.frame_for_sign_in.pack()

        self.window_for_authorization.grab_set()

class About_user():

    def check_login(self, *args):
        if self.new_login.get()=="":
            self.button_change_login['state'] = 'disabled'
        else: 
            self.button_change_login['state'] = 'normal'

    def check_password(self, *args):
        if self.new_password.get()=="":
            self.button_change_password['state'] = 'disabled'
        else: 
            self.button_change_password['state'] = 'normal'


    def __init__(self, root):
        self.root = root
        self.window_about_user = Toplevel(self.root)

        self.window_about_user.title("User information")
        self.window_about_user.geometry("400x450")
        self.window_about_user.resizable(False, False)

        self.label_user_info = ttk.Label(self.window_about_user, text="User information", font=("Arial", 14))
        self.label_user_info.pack()

        self.frame_user_info = ttk.Frame(self.window_about_user, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.login = ""
        self.is_admin = ""
        self.first_name = ""
        self.last_name = ""

        try:
            cur = conn.cursor()
            cur.callproc('poll_admin.get_auth_info', ['get_auth_info_cur', auth_id_global])
            get_auth_info_cur = conn.cursor('get_auth_info_cur')
            auth_info = get_auth_info_cur.fetchone()
            get_auth_info_cur.close()

            self.login = auth_info[1]
            self.is_admin = auth_info[3]

            cur.callproc('poll_admin.get_user_info', ['get_user_info_cur', auth_id_global])
            get_user_info_cur = conn.cursor('get_user_info_cur')
            user_info = get_user_info_cur.fetchone()
            get_user_info_cur.close()

            self.first_name = user_info[1]
            self.last_name = user_info[2]

            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        self.label_user_login = ttk.Label(self.frame_user_info, text=f"Login: %s" % self.login, font=("Arial", 14))
        self.label_user_login.pack()

        self.label_user_first_name = ttk.Label(self.frame_user_info, text=f"First name: %s" % self.first_name, font=("Arial", 14))
        self.label_user_first_name.pack()

        self.label_user_last_name = ttk.Label(self.frame_user_info, text=f"Last name: %s" % self.last_name, font=("Arial", 14))
        self.label_user_last_name.pack()

        self.label_user_is_admin = ttk.Label(self.frame_user_info, text=f"Admin: %s" % str(self.is_admin), font=("Arial", 14))
        self.label_user_is_admin.pack()

        self.new_login = StringVar()
        self.entry_change_login = ttk.Entry(self.frame_user_info, textvariable=self.new_login)
        self.entry_change_login.pack(padx=8, pady= 8)

        self.new_login.trace_add("write", self.check_login)
        self.new_login.trace("w", lambda *args: character_limit_50(self.new_login))

        def change_login(new_login):
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.login_in_used', ['login_in_used_cur', new_login.get()])
                login_in_used_cur = conn.cursor('login_in_used_cur')
                login_from_db = login_in_used_cur.fetchone()
                login_in_used_cur.close()

                
                if login_from_db:
                    if login_from_db[0] == new_login.get():
                        showerror(title="Error", message="Login is being used by another user!")
                        return False
                    

                cur.execute('call poll_admin.update_login_authorization(%s, %s)', (new_login.get(), auth_id_global))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return False;

            showinfo(title="Success", message="Login has been updated.")

        self.button_change_login = ttk.Button(self.frame_user_info, text="Change login", command=lambda: change_login(self.new_login), state=["disabled"])
        self.button_change_login.pack()

        self.new_password = StringVar()
        self.entry_change_password = ttk.Entry(self.frame_user_info, textvariable=self.new_password)
        self.entry_change_password.pack(padx=8, pady= 8)

        self.new_password.trace_add("write", self.check_password)

        def change_password(new_password):
            try:
                cur = conn.cursor()

                bytes = new_password.get().encode('utf-8')
                hashed_password = bcrypt.hashpw(bytes, bcrypt.gensalt())

                cur.execute('call poll_admin.update_password_authorization(%s, %s)', (hashed_password.decode("utf-8"), auth_id_global))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                conn.rollback()
                return False

            showinfo(title="Success", message="Password has been updated.")

        self.button_change_password = ttk.Button(self.frame_user_info, text="Change password", command=lambda: change_password(self.new_password), state=["disabled"])
        self.button_change_password.pack()

        self.frame_user_info.pack()

        self.window_about_user.grab_set()


class Create_poll():
    def __init__(self, root):
        self.root = root
        self.window_create_poll = Toplevel(self.root)

        self.window_create_poll.title("Create poll")
        self.window_create_poll.geometry("400x570")
        self.window_create_poll.resizable(False, False)

        self.label_create_poll = ttk.Label(self.window_create_poll, text="Create poll", font=("Arial", 14))
        self.label_create_poll.pack()

        self.frame_create_poll = ttk.Frame(self.window_create_poll, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.poll_name = StringVar()
        self.poll_description = StringVar()

        self.label_poll_name = ttk.Label(self.frame_create_poll, text="Poll name", font=("Arial", 14))
        self.label_poll_name.pack()
        self.entry_poll_name = ttk.Entry(self.frame_create_poll, textvariable=self.poll_name)
        self.entry_poll_name.pack(padx=8, pady= 8)

        self.label_poll_description = ttk.Label(self.frame_create_poll, text="Description", font=("Arial", 14))
        self.label_poll_description.pack()
        self.entry_poll_description = ttk.Entry(self.frame_create_poll, textvariable=self.poll_description)
        self.entry_poll_description.pack(padx=8, pady= 8)

        def check_entry_text(event, *args):
            if self.poll_name.get()=="" or self.poll_description.get()=="":
                self.button_create_poll['state'] = 'disabled'
            else:
                self.button_create_poll['state'] = 'normal'      

        self.poll_name.trace("w", lambda *args: character_limit_100(self.poll_name))
        self.poll_name.trace_add("write", check_entry_text)
        self.poll_description.trace("w", lambda *args: character_limit_250(self.poll_description))
        self.poll_description.trace_add("write", check_entry_text)

        self.poll_is_open = StringVar(value=True)

        self.label_poll_is_true = ttk.Label(self.frame_create_poll, text="Is poll open?", font=("Arial", 14))
        self.label_poll_is_true.pack()

        self.button_poll_is_true = ttk.Radiobutton(self.frame_create_poll, text="True", value=True, variable=self.poll_is_open)
        self.button_poll_is_true.pack(padx=6, pady=6, anchor=NW)
        self.button_poll_is_false = ttk.Radiobutton(self.frame_create_poll, text="False", value=False, variable=self.poll_is_open)
        self.button_poll_is_false.pack(padx=6, pady=6, anchor=NW)

        self.label_poll_category = ttk.Label(self.frame_create_poll, text="Poll category", font=("Arial", 14))
        self.label_poll_category.pack()
        # self.combobox_categories = ttk.Combobox(self.frame_create_poll, values=get_categories_name(), state="readonly")
        # self.combobox_categories.pack(padx=6, pady=6, anchor=NW)
        # self.combobox_categories.bind("<<ComboboxSelected>>", check_entry_text)

        self.current_page = 1

        self.categories = get_categories_name_pagination(self.current_page, 1000)
        self.categories_var = Variable(value=self.categories)

        self.scrollbar = Scrollbar(self.frame_create_poll, orient = VERTICAL)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        self.listbox_categories = Listbox(self.frame_create_poll, listvariable=self.categories_var, selectmode=SINGLE)
        self.listbox_categories.pack(padx=6, pady=6, anchor=NW)

        self.listbox_categories.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command = self.listbox_categories.yview)

        def next_page():
            self.current_page += 1

            self.backup_categories = self.categories

            self.categories = get_categories_name_pagination(self.current_page, 1000)

            if not self.categories:
                self.current_page -= 1
                self.categories = self.backup_categories
                showwarning(title="Warning", message="Next page is empty. Click previous page, please.")
                return False

            self.categories_var = Variable(value=self.categories)
            self.listbox_categories['listvariable'] = self.categories_var

            if self.current_page == 1:
                self.button_previous_page['state'] = 'disabled'
            else:
                self.button_previous_page['state'] = 'normal'


        self.button_next_page = ttk.Button(self.frame_create_poll, text="Next page", command=lambda: next_page())
        self.button_next_page.pack()

        def previous_page():

            self.current_page -= 1
            self.categories = get_categories_name_pagination(self.current_page, 1000)
            self.categories_var = Variable(value=self.categories)
            self.listbox_categories['listvariable'] = self.categories_var

            if self.current_page == 1:
                self.button_previous_page['state'] = 'disabled'
                return False
            else:
                self.button_previous_page['state'] = 'normal'

        self.button_previous_page = ttk.Button(self.frame_create_poll, text="Previous page", command=lambda: previous_page(), state=["disabled"])
        self.button_previous_page.pack()

        def func_create_poll(name, description, is_open):
            selection = self.listbox_categories.curselection()

            if not selection:
                showerror(title="Error", message="Selection in categories is empty! Select something!")
                return False

            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_category_id', ['find_category_id_cur', self.categories[int(selection[0])]])
                find_category_id_cur = conn.cursor('find_category_id_cur')
                category_id = find_category_id_cur.fetchone()
                find_category_id_cur.close()

                cur.callproc('poll_admin.find_user_id', ['find_user_id_cur', auth_id_global])
                find_user_id_cur = conn.cursor('find_user_id_cur')
                user_id = find_user_id_cur.fetchone()
                find_user_id_cur.close()

                cur.execute('call poll_admin.insert_data_poll_create(%s, %s, %s, %s, %s)', (name.get(), description.get(), is_open.get(), int(user_id[0]), int(category_id[0])))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                showerror(title="Error", message="The poll with this name is already exist!")
                conn.rollback()
                print(error)
                return False;

            showinfo(title="Success", message="Poll has been added.")

        def func_back_to_admin_panel(window_create_poll):
            self.window_create_poll.grab_release()
            self.window_create_poll.destroy()

        self.button_create_poll = ttk.Button(self.frame_create_poll, text="Create poll", command=lambda: func_create_poll(self.poll_name, self.poll_description, self.poll_is_open), state=["disabled"])
        self.button_create_poll.pack()

        self.button_back_to_admin_panel = ttk.Button(self.frame_create_poll, text="Back", command=lambda: func_back_to_admin_panel(self.window_create_poll))
        self.button_back_to_admin_panel.pack()

        self.frame_create_poll.pack()

        self.window_create_poll.grab_set()


class Create_category():
    def __init__(self, root):
        self.root = root
        self.window_create_category = Toplevel(self.root)

        self.window_create_category.title("Create poll")
        self.window_create_category.geometry("400x450")
        self.window_create_category.resizable(False, False)

        self.label_create_category = ttk.Label(self.window_create_category, text="Create category", font=("Arial", 14))
        self.label_create_category.pack()

        self.frame_create_category = ttk.Frame(self.window_create_category, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.category_content = StringVar()

        self.label_category_content = ttk.Label(self.frame_create_category, text="Category name", font=("Arial", 14))
        self.label_category_content.pack()
        self.entry_category_content = ttk.Entry(self.frame_create_category, textvariable=self.category_content)
        self.entry_category_content.pack(padx=8, pady= 8)

        def check_entry_text(*args):
            if self.category_content.get()=="":
                self.button_create_category['state'] = 'disabled'
            else:
                self.button_create_category['state'] = 'normal'

        self.category_content.trace("w", lambda *args: character_limit_100(self.category_content))
        self.category_content.trace_add("write", check_entry_text)

        def func_create_category(content):
            try:
                cur = conn.cursor()

                cur.execute('call poll_admin.insert_data_category(%s)', (content.get(), ))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False;

            showinfo(title="Success", message="Category has been added.")


        def func_back_to_admin_panel(window_create_category):
            self.window_create_category.grab_release()
            self.window_create_category.destroy()

        self.button_create_category = ttk.Button(self.frame_create_category, text="Create category", command=lambda: func_create_category(self.category_content), state=["disabled"])
        self.button_create_category.pack()

        self.button_back_to_admin_panel = ttk.Button(self.frame_create_category, text="Back", command=lambda: func_back_to_admin_panel(self.window_create_category))
        self.button_back_to_admin_panel.pack()

        self.frame_create_category.pack()

        self.window_create_category.grab_set()

class Create_question():

    def __init__(self, root):
        self.root = root
        self.window_create_question = Toplevel(self.root)

        self.window_create_question.title("Create question")
        self.window_create_question.geometry("400x450")
        self.window_create_question.resizable(False, False)

        self.label_create_question = ttk.Label(self.window_create_question, text="Create question", font=("Arial", 14))
        self.label_create_question.pack()

        self.frame_create_question = ttk.Frame(self.window_create_question, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.question_text = StringVar()

        self.label_question_text = ttk.Label(self.frame_create_question, text="Question text", font=("Arial", 14))
        self.label_question_text.pack()
        self.entry_question_text = ttk.Entry(self.frame_create_question, textvariable=self.question_text)
        self.entry_question_text.pack(padx=8, pady= 8)

        def check_entry_text(event, *args):
            if self.question_text.get()=="" or self.combobox_polls.get()=="":
                self.button_create_question['state'] = 'disabled'
            else:
                self.button_create_question['state'] = 'normal'

        self.question_text.trace("w", lambda *args: character_limit_250(self.question_text))
        self.question_text.trace_add("write", check_entry_text)

        self.combobox_polls = ttk.Combobox(self.frame_create_question, values=get_polls_name(), state="readonly")
        self.combobox_polls.pack(padx=6, pady=6, anchor=NW)
        self.combobox_polls.bind("<<ComboboxSelected>>", check_entry_text)

        def func_create_question(text, poll_name):
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_poll_id', ['find_poll_id_cur', poll_name.get()])
                find_poll_id_cur = conn.cursor('find_poll_id_cur')
                poll_id = find_poll_id_cur.fetchone()
                find_poll_id_cur.close()

                cur.callproc('poll_admin.poll_already_have_question', ['poll_already_have_question_cur', int(poll_id[0])])
                poll_already_have_question_cur = conn.cursor('poll_already_have_question_cur')
                have_a_question = poll_already_have_question_cur.fetchone()
                poll_already_have_question_cur.close()

                if have_a_question:
                    conn.rollback()
                    cur.close()
                    showerror(title="Error", message="One poll - one question!")
                    return False
                else:
                    cur.execute('call poll_admin.insert_data_question(%s, %s)', (text.get(), int(poll_id[0])))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.errors.UniqueViolation) as error:
                conn.rollback()
                print(error)
                showerror(title="Error", message="One poll - one question!")
                return False
            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                showerror(title="Error", message=error)
                return False;

            showinfo(title="Success", message="Question has been added.")


        def func_back_to_admin_panel(window_create_question):
            self.window_create_question.grab_release()
            self.window_create_question.destroy()

        self.button_create_question = ttk.Button(self.frame_create_question, text="Create question", command=lambda: func_create_question(self.question_text, self.combobox_polls), state=["disabled"])
        self.button_create_question.pack()

        self.button_back_to_admin_panel = ttk.Button(self.frame_create_question, text="Back", command=lambda: func_back_to_admin_panel(self.window_create_question))
        self.button_back_to_admin_panel.pack()

        self.frame_create_question.pack()

        self.window_create_question.grab_set()

class Create_option():
    def __init__(self, root):
        self.root = root
        self.window_create_option = Toplevel(self.root)

        self.window_create_option.title("Create option")
        self.window_create_option.geometry("400x450")
        self.window_create_option.resizable(False, False)

        self.label_create_option = ttk.Label(self.window_create_option, text="Create option", font=("Arial", 14))
        self.label_create_option.pack()

        self.frame_create_option = ttk.Frame(self.window_create_option, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.option_text = StringVar()

        self.label_option_text = ttk.Label(self.frame_create_option, text="Option text", font=("Arial", 14))
        self.label_option_text.pack()
        self.entry_option_text = ttk.Entry(self.frame_create_option, textvariable=self.option_text)
        self.entry_option_text.pack(padx=8, pady= 8)

        def check_entry_text(event, *args):
            if self.option_text.get()=="" or self.combobox_questions.get()=="":
                self.button_create_option['state'] = 'disabled'
            else:
                self.button_create_option['state'] = 'normal'

        self.option_text.trace("w", lambda *args: character_limit_250(self.option_text))
        self.option_text.trace_add("write", check_entry_text)

        self.combobox_questions = ttk.Combobox(self.frame_create_option, values=get_questions_text(), state="readonly")
        self.combobox_questions.pack(padx=6, pady=6, anchor=NW)
        self.combobox_questions.bind("<<ComboboxSelected>>", check_entry_text)

        def func_create_option(text, question_text):
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_question_id', ['find_question_id_cur', question_text.get()])
                find_question_id_cur = conn.cursor('find_question_id_cur')
                question_id = find_question_id_cur.fetchone()
                find_question_id_cur.close()

                cur.execute('call poll_admin.insert_data_option(%s, %s)', (text.get(), int(question_id[0])))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                showerror(title="Error", message="The option with this name is already exist!")
                conn.rollback()
                print(error)
                return False;

            showinfo(title="Success", message="Option has been added.")


        def func_back_to_admin_panel(window_create_option):
            self.window_create_option.grab_release()
            self.window_create_option.destroy()

        self.button_create_option = ttk.Button(self.frame_create_option, text="Create option", command=lambda: func_create_option(self.option_text, self.combobox_questions), state=["disabled"])
        self.button_create_option.pack()

        self.button_back_to_admin_panel = ttk.Button(self.frame_create_option, text="Back", command=lambda: func_back_to_admin_panel(self.window_create_option))
        self.button_back_to_admin_panel.pack()

        self.frame_create_option.pack()

        self.window_create_option.grab_set()


class Poll_status():
    def __init__(self, root):
        self.root = root
        self.window_poll_status = Toplevel(self.root)

        self.window_poll_status.title("Poll status")
        self.window_poll_status.geometry("400x450")
        self.window_poll_status.resizable(False, False)

        self.frame_poll_status = ttk.Frame(self.window_poll_status, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.label_select_poll = ttk.Label(self.frame_poll_status, text="Select poll", font=("Arial", 14))
        self.label_select_poll.pack()

        self.poll_id = -1
        self.poll_status = StringVar()

        def selected(event):
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_poll_id', ['find_poll_id_cur', self.combobox_polls.get()])
                find_poll_id_cur = conn.cursor('find_poll_id_cur')
                poll_id = find_poll_id_cur.fetchone()
                poll_id = int(poll_id[0])
                self.poll_id = poll_id
                find_poll_id_cur.close()

                cur.callproc('poll_admin.get_poll_status', ['get_poll_status_cur', poll_id])
                get_poll_status_cur = conn.cursor('get_poll_status_cur')
                poll_status_local = get_poll_status_cur.fetchone()
                get_poll_status_cur.close()

                poll_status_local = poll_status_local[0]
                poll_status = StringVar(value=poll_status_local)
                self.poll_status = poll_status

                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False

            self.label_poll_status.pack()
            self.button_poll_is_true.pack(padx=6, pady=6, anchor=NW)
            self.button_poll_is_false.pack(padx=6, pady=6, anchor=NW)
            self.button_poll_is_true.configure(variable=poll_status)
            self.button_poll_is_false.configure(variable=poll_status)
            self.button_change_poll_status['state'] = 'normal'

        def func_change_poll_stsatus(new_poll_status, poll_id_p):
            try:
                cur = conn.cursor()

                cur.execute('call poll_admin.update_poll_status(%s, %s)', (new_poll_status, poll_id_p))

                # '0' = false (in this case)
                if new_poll_status == '0':
                    cur.execute('call poll_admin.update_poll_date_closed(%s, %s)', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), poll_id_p))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False;

            showinfo(title="Success", message="Poll status has been changed.")

        self.combobox_polls = ttk.Combobox(self.frame_poll_status, values=get_polls_name(), state="readonly")
        self.combobox_polls.pack(padx=6, pady=6, anchor=NW)
        self.combobox_polls.bind("<<ComboboxSelected>>", selected)

        self.label_poll_status = ttk.Label(self.frame_poll_status, text="Poll status", font=("Arial", 14))

        self.button_poll_is_true = ttk.Radiobutton(self.frame_poll_status, text="True", value=True, variable=self.poll_status)
        
        self.button_poll_is_false = ttk.Radiobutton(self.frame_poll_status, text="False", value=False, variable=self.poll_status)

        def func_back_to_admin_panel(window_poll_status):
            self.window_poll_status.grab_release()
            self.window_poll_status.destroy()

        self.button_change_poll_status = ttk.Button(self.frame_poll_status, text="Change the poll status", command=lambda: func_change_poll_stsatus(self.poll_status.get(), self.poll_id), state=["disabled"])
        self.button_change_poll_status.pack()

        self.button_back_to_admin_panel = ttk.Button(self.frame_poll_status, text="Back", command=lambda: func_back_to_admin_panel(self.window_poll_status))
        self.button_back_to_admin_panel.pack()

        self.frame_poll_status.pack()

        self.window_poll_status.grab_set()

class Start_polling():
    def __init__(self, root, poll_id):
        self.root = root
        self.window_start_polling = Toplevel(self.root)

        self.window_start_polling.title("Let's poll!")
        self.window_start_polling.geometry("400x450")
        self.window_start_polling.resizable(False, False)

        self.frame_start_polling = ttk.Frame(self.window_start_polling, borderwidth=1, relief=SOLID, padding=[8, 10])

        question_text = ''
        options_texts_tuples_in_list = []

        user_voted = False
        poll_status = True

        def func_back_to_admin_panel(window_start_polling):
            self.window_start_polling.grab_release()
            self.window_start_polling.destroy()

        # get questions
        try:
            cur = conn.cursor()

            cur.callproc('poll_admin.get_question_texts_by_poll_id', ['get_question_texts_by_poll_id_cur', poll_id])
            get_question_texts_by_poll_id_cur = conn.cursor('get_question_texts_by_poll_id_cur')
            questions_texts_tuples_in_list = get_question_texts_by_poll_id_cur.fetchone()
            get_question_texts_by_poll_id_cur.close()

            if not questions_texts_tuples_in_list:
                showerror(title="Error", message="Poll is wrong. Сontact administrator.")
                conn.rollback()
                cur.close()
                func_back_to_admin_panel(self.window_start_polling)
                return None
            else:
                question_text = questions_texts_tuples_in_list[0]

            cur.callproc('poll_admin.find_question_id', ['find_question_id_cur', question_text])
            find_question_id_cur = conn.cursor('find_question_id_cur')
            questions_id_tuples_in_list = find_question_id_cur.fetchone()
            find_question_id_cur.close()

            question_id = questions_id_tuples_in_list[0]

            cur.callproc('poll_admin.get_option_texts_by_question_id', ['get_option_texts_by_question_id_cur', question_id])
            get_option_texts_by_question_id_cur = conn.cursor('get_option_texts_by_question_id_cur')
            options_texts_tuples_in_list += get_option_texts_by_question_id_cur.fetchall()
            get_option_texts_by_question_id_cur.close()

            # User voted?

            cur.callproc('poll_admin.find_user_id', ['find_user_id_cur', auth_id_global])
            find_user_id_cur = conn.cursor('find_user_id_cur')
            user_id = find_user_id_cur.fetchone()
            find_user_id_cur.close()

            cur.callproc('poll_admin.find_option_id_by_question_id', ['find_option_id_by_question_id_cur', question_id])
            find_option_id_by_question_id_cur = conn.cursor('find_option_id_by_question_id_cur')
            option_ids_list_of_tuples = find_option_id_by_question_id_cur.fetchall()
            find_option_id_by_question_id_cur.close()

            option_ids_list = [item for t in option_ids_list_of_tuples for item in t]

            cur.callproc('poll_admin.get_option_id_from_answer_by_user_id', ['get_option_id_from_answer_by_user_id_cur', user_id])
            get_option_id_from_answer_by_user_id_cur = conn.cursor('get_option_id_from_answer_by_user_id_cur')
            user_option_answer_list_of_tuples = get_option_id_from_answer_by_user_id_cur.fetchall()
            get_option_id_from_answer_by_user_id_cur.close()

            user_option_answer_list = [item for t in user_option_answer_list_of_tuples for item in t]

            # get poll status
            cur.callproc('poll_admin.get_poll_status', ['get_poll_status_cur', poll_id])
            get_poll_status_cur = conn.cursor('get_poll_status_cur')
            poll_status_tuples_in_list = get_poll_status_cur.fetchone()
            get_poll_status_cur.close()

            poll_status = poll_status_tuples_in_list[0]

            if not user_option_answer_list:
                user_voted = False
            else:
                flag_find = False
                for item in option_ids_list:
                    if flag_find:
                        break
                    for option_item in user_option_answer_list:
                        if option_item == item:
                            user_voted = True
                            flag_find = True
                            break

            conn.commit()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            print(error)  


        def create_answer():
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_user_id', ['find_user_id_cur', auth_id_global])
                find_user_id_cur = conn.cursor('find_user_id_cur')
                user_id = find_user_id_cur.fetchone()
                find_user_id_cur.close()

                cur.callproc('poll_admin.find_option_id', ['find_option_id_cur', answer.get()])
                find_option_id_cur = conn.cursor('find_option_id_cur')
                option_id = find_option_id_cur.fetchone()
                find_option_id_cur.close()

                cur.execute('call poll_admin.insert_data_answer(%s, %s)', (user_id, option_id))

                cur.execute('call poll_admin.update_quantity_option(%s)', (option_id, ))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)

            showinfo(title="Success", message="You have successfully voted!")
            func_back_to_admin_panel(self.window_start_polling)

        def poll_result():
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_question_id_by_poll_id', ['find_question_id_by_poll_id_cur', poll_id])
                find_question_id_by_poll_id_cur = conn.cursor('find_question_id_by_poll_id_cur')
                question_id = find_question_id_by_poll_id_cur.fetchone()
                find_question_id_by_poll_id_cur.close()

                cur.callproc('poll_admin.get_text_and_quantity_by_question_id', ['get_text_and_quantity_by_question_id_cur', int(question_id[0])])
                get_text_and_quantity_by_question_id_cur = conn.cursor('get_text_and_quantity_by_question_id_cur')
                option_text_and_quantity_list_of_tuples = get_text_and_quantity_by_question_id_cur.fetchall()
                get_text_and_quantity_by_question_id_cur.close()

                text=[]
                quantity=[]
                for item in option_text_and_quantity_list_of_tuples:
                    text.append(item[0])
                    quantity.append(item[1])
                
                # If everything is zero in quantity
                if not any(quantity):
                    showerror(title="Error", message="No one has voted yet! Сontact administrator.")
                    cur.close()
                    return False

                plt.title('Poll result')
                plt.pie(quantity,labels=text,autopct='%1.1f%%',shadow=True,startangle=140)
                plt.axis('equal')
                plt.show()

                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False

        if poll_status:
            if user_voted:
                self.label_wait_for_results = ttk.Label(self.frame_start_polling, text="Wait for the results", font=("Arial", 14))
                self.label_wait_for_results.pack()

                self.label_user_voted_part = ttk.Label(self.frame_start_polling, text="You have already voted! Please, wait for the poll to end to see the results.", font=("Arial", 14), wraplength=300, justify="center")
                self.label_user_voted_part.pack()
            else:
                self.label_poll = ttk.Label(self.frame_start_polling, text="Question", font=("Arial", 14))
                self.label_poll.pack()

                self.label_question_text = ttk.Label(self.frame_start_polling, text=question_text, font=("Arial", 14))
                self.label_question_text.pack()

                answer = StringVar()

                for option in options_texts_tuples_in_list:
                    self.rdbutton_poll_option = ttk.Radiobutton(self.frame_start_polling, text=option[0], value=option[0], variable=answer)
                    self.rdbutton_poll_option.pack()

                def check_option_selection(event, *args):
                    if answer.get()=="":
                        self.button_vote['state'] = 'disabled'
                    else:
                        self.button_vote['state'] = 'normal'

                answer.trace_add("write", check_option_selection)

                self.button_vote = ttk.Button(self.frame_start_polling, text="Vote", command=lambda: create_answer(), state=["disabled"])
                self.button_vote.pack()
        else:
            self.label_poll_is_over = ttk.Label(self.frame_start_polling, text="Poll is over", font=("Arial", 14))
            self.label_poll_is_over.pack()

            self.button_poll_result = ttk.Button(self.frame_start_polling, text="Result", command=lambda: poll_result())
            self.button_poll_result.pack()

        self.button_back_to_admin_panel = ttk.Button(self.frame_start_polling, text="Back", command=lambda: func_back_to_admin_panel(self.window_start_polling))
        self.button_back_to_admin_panel.pack()

        self.frame_start_polling.pack()

        self.window_start_polling.grab_set()

class Delete_category():
    def __init__(self, root):
        self.root = root
        self.window_delete_category = Toplevel(self.root)

        self.window_delete_category.title("Deleting category")
        self.window_delete_category.geometry("400x450")
        self.window_delete_category.resizable(False, False)

        self.frame_delete_category = ttk.Frame(self.window_delete_category, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.label_delete_category = ttk.Label(self.frame_delete_category, text="Deleting category", font=("Arial", 14))
        self.label_delete_category.pack()

        self.current_page = 1

        self.categories = get_categories_name_pagination(self.current_page, 1000)
        self.categories_var = Variable(value=self.categories)

        self.scrollbar = Scrollbar(self.frame_delete_category, orient = VERTICAL)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        self.listbox_categories = Listbox(self.frame_delete_category, listvariable=self.categories_var, selectmode=SINGLE)
        self.listbox_categories.pack(padx=6, pady=6, anchor=NW)

        self.listbox_categories.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command = self.listbox_categories.yview)

        def delete():
            selection = self.listbox_categories.curselection()

            if not selection:
                showerror(title="Error", message="Selection is empty! Select something!")
                return False

            try:
                cur = conn.cursor()

                print(self.categories[int(selection[0])])

                cur.execute('call poll_admin.delete_selected_category(%s)', (self.categories[int(selection[0])], ))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.errors.IntegrityError) as error:
                conn.rollback()
                print(error)
                showerror(title="Error", message="The category is used for polls.")
                return False

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False

            showwarning(title="Warning", message="Category has been deleted.")

            self.listbox_categories.delete(selection[0])
            del self.categories[int(selection[0])]


        self.button_delete_category = ttk.Button(self.frame_delete_category, text="Delete selected category", command=lambda: delete())
        self.button_delete_category.pack()

        def next_page():
            self.current_page += 1

            self.backup_categories = self.categories

            self.categories = get_categories_name_pagination(self.current_page, 1000)

            if not self.categories:
                self.current_page -= 1
                self.categories = self.backup_categories
                showwarning(title="Warning", message="Next page is empty. Click previous page, please.")
                return False

            self.categories_var = Variable(value=self.categories)
            self.listbox_categories['listvariable'] = self.categories_var

            if self.current_page == 1:
                self.button_previous_page['state'] = 'disabled'
            else:
                self.button_previous_page['state'] = 'normal'


        self.button_next_page = ttk.Button(self.frame_delete_category, text="Next page", command=lambda: next_page())
        self.button_next_page.pack()

        def previous_page():

            self.current_page -= 1
            self.categories = get_categories_name_pagination(self.current_page, 1000)
            self.categories_var = Variable(value=self.categories)
            self.listbox_categories['listvariable'] = self.categories_var

            if self.current_page == 1:
                self.button_previous_page['state'] = 'disabled'
                return False
            else:
                self.button_previous_page['state'] = 'normal'

        self.button_previous_page = ttk.Button(self.frame_delete_category, text="Previous page", command=lambda: previous_page(), state=["disabled"])
        self.button_previous_page.pack()

        def func_back_to_admin_panel(window_delete_category):
            self.window_delete_category.grab_release()
            self.window_delete_category.destroy()

        self.button_back_to_admin_panel = ttk.Button(self.frame_delete_category, text="Back", command=lambda: func_back_to_admin_panel(self.window_delete_category))
        self.button_back_to_admin_panel.pack()

        self.frame_delete_category.pack()

        self.window_delete_category.grab_set()

class Delete_poll():
    def __init__(self, root):
        self.root = root
        self.window_delete_poll = Toplevel(self.root)

        self.window_delete_poll.title("Deleting poll")
        self.window_delete_poll.geometry("400x450")
        self.window_delete_poll.resizable(False, False)

        self.frame_delete_poll = ttk.Frame(self.window_delete_poll, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.label_delete_poll = ttk.Label(self.frame_delete_poll, text="Deleting poll", font=("Arial", 14))
        self.label_delete_poll.pack()


        polls = get_polls_name()
        polls_var = Variable(value=polls)

        self.scrollbar = Scrollbar(self.frame_delete_poll, orient = VERTICAL)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        self.listbox_polls = Listbox(self.frame_delete_poll, listvariable=polls_var, selectmode=SINGLE)
        self.listbox_polls.pack(padx=6, pady=6, anchor=NW)

        self.listbox_polls.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command = self.listbox_polls.yview)

        def delete():
            selection = self.listbox_polls.curselection()

            if not selection:
                showerror(title="Error", message="Selection is empty! Select something!")
                return False

            try:
                cur = conn.cursor()

                cur.execute('call poll_admin.delete_selected_poll(%s)', (polls[int(selection[0])], ))

                conn.commit()
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False

            showwarning(title="Warning", message="Poll has been deleted. All related information with the poll has been deleted.")

            self.listbox_polls.delete(selection[0])
            del polls[int(selection[0])]


        self.button_delete_poll = ttk.Button(self.frame_delete_poll, text="Delete selected poll", command=lambda: delete())
        self.button_delete_poll.pack()

        def func_back_to_admin_panel(window_delete_category):
            self.window_delete_poll.grab_release()
            self.window_delete_poll.destroy()

        self.button_back_to_admin_panel = ttk.Button(self.frame_delete_poll, text="Back", command=lambda: func_back_to_admin_panel(self.window_delete_poll))
        self.button_back_to_admin_panel.pack()

        self.frame_delete_poll.pack()

        self.window_delete_poll.grab_set()


class Poll_result():
    def __init__(self, root):
        self.root = root
        self.window_poll_result = Toplevel(self.root)

        self.window_poll_result.title("Poll result")
        self.window_poll_result.geometry("400x450")
        self.window_poll_result.resizable(False, False)

        self.frame_poll_result = ttk.Frame(self.window_poll_result, borderwidth=1, relief=SOLID, padding=[8, 10])

        self.label_poll_result = ttk.Label(self.frame_poll_result, text="poll result", font=("Arial", 14))
        self.label_poll_result.pack()

        def selected(event):
            try:
                cur = conn.cursor()

                cur.callproc('poll_admin.find_poll_id', ['find_poll_id_cur', self.combobox_polls.get()])
                find_poll_id_cur = conn.cursor('find_poll_id_cur')
                poll_id = find_poll_id_cur.fetchone()
                find_poll_id_cur.close()

                cur.callproc('poll_admin.find_question_id_by_poll_id', ['find_question_id_by_poll_id_cur', int(poll_id[0])])
                find_question_id_by_poll_id_cur = conn.cursor('find_question_id_by_poll_id_cur')
                question_id = find_question_id_by_poll_id_cur.fetchone()
                find_question_id_by_poll_id_cur.close()

                cur.callproc('poll_admin.get_text_and_quantity_by_question_id', ['get_text_and_quantity_by_question_id_cur', int(question_id[0])])
                get_text_and_quantity_by_question_id_cur = conn.cursor('get_text_and_quantity_by_question_id_cur')
                option_text_and_quantity_list_of_tuples = get_text_and_quantity_by_question_id_cur.fetchall()
                get_text_and_quantity_by_question_id_cur.close()

                text=[]
                quantity=[]
                for item in option_text_and_quantity_list_of_tuples:
                    text.append(item[0])
                    quantity.append(item[1])
                
                # If everything is zero in quantity
                if not any(quantity):
                    showerror(title="Error", message="No one has voted yet! Nothing to show!")
                    cur.close()
                    return False

                plt.title('Poll result')
                plt.pie(quantity,labels=text,autopct='%1.1f%%',shadow=True,startangle=140)
                plt.axis('equal')
                plt.show()

                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                conn.rollback()
                print(error)
                return False

        self.combobox_polls = ttk.Combobox(self.frame_poll_result, values=get_polls_name(), state="readonly")
        self.combobox_polls.pack(padx=6, pady=6, anchor=NW)
        self.combobox_polls.bind("<<ComboboxSelected>>", selected)

        def func_back_to_admin_panel(window_poll_result):
            self.window_poll_result.grab_release()
            self.window_poll_result.destroy()

        self.button_back_to_admin_panel = ttk.Button(self.frame_poll_result, text="Back", command=lambda: func_back_to_admin_panel(self.window_poll_result))
        self.button_back_to_admin_panel.pack()

        self.frame_poll_result.pack()

        self.window_poll_result.grab_set()

def get_questions_text():
    try:
        cur = conn.cursor()
        
        cur.callproc('poll_admin.get_questions_text', ['get_questions_text_cur'])
        get_questions_text_cur = conn.cursor('get_questions_text_cur')
        questions_text_tuples_in_list = get_questions_text_cur.fetchall()
        get_questions_text_cur.close()
        cur.close()

        questions_text_list = [item for t in questions_text_tuples_in_list for item in t]
        return questions_text_list

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        showerror(title="Error", message="Wrong!")


def get_categories_name():
    try:
        cur = conn.cursor()
        
        cur.callproc('poll_admin.get_categories_content', ['get_categories_content_cur'])
        get_categories_content_cur = conn.cursor('get_categories_content_cur')
        categories_name_tuples_in_list = get_categories_content_cur.fetchall()
        get_categories_content_cur.close()
        cur.close()

        categories_name_list = [item for t in categories_name_tuples_in_list for item in t]
        return categories_name_list

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        showerror(title="Error", message="Wrong!")


def get_categories_name_pagination(page, limit):
        try:
            cur = conn.cursor()
            
            cur.callproc('poll_admin.get_categories_content_pagination', ['get_categories_content_pagination_cur', page if page > 0 else 1, limit if limit > 0 else 1000])
            get_categories_content_pagination_cur = conn.cursor('get_categories_content_pagination_cur')
            categories_name_tuples_in_list = get_categories_content_pagination_cur.fetchall()
            get_categories_content_pagination_cur.close()
            cur.close()

            categories_name_list = [item for t in categories_name_tuples_in_list for item in t]
            return categories_name_list

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            showerror(title="Error", message="Wrong!")


def get_polls_name():
    try:
        cur = conn.cursor()
        
        cur.callproc('poll_admin.get_polls_name', ['get_polls_name_cur'])
        get_polls_name_cur = conn.cursor('get_polls_name_cur')
        polls_name_tuples_in_list = get_polls_name_cur.fetchall()
        get_polls_name_cur.close()
        cur.close()

        polls_name_list = [item for t in polls_name_tuples_in_list for item in t]
        return polls_name_list

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        showerror(title="Error", message="Wrong!")




connect()
root = Tk()
root.withdraw()
root.title("Poll")
icon = PhotoImage(file = "poll.png")
# first parameter - use default icon for all app windows
root.iconphoto(True, icon)
# Width x Height (window size)
root.geometry("400x450")
# resize width, height
root.resizable(False, False)


Authorization_user(root)
root.mainloop()


