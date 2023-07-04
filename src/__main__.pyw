import time
import tkinter as tk
from sqlite3 import IntegrityError
from threading import Thread

from src import db
from src.email_functions import get_emails
from src.functions import *


class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self._center_window()
        self.disable_menu = False

        self.title('Work Assistant')
        self.bind('<Return>', self._create_email)
        
        self.email_frame = tk.Frame(self, borderwidth=2, relief="groove")
        self.options_frame = tk.Frame(self)
        misc_func_frame = tk.Frame(self)

        #email_frame objects:
        docket_label = tk.Label(self.email_frame, text="Docket:")
        self.dkt_entry = tk.Entry(self.email_frame, width=12)
        self.dkt_entry.focus()
        
        self._get_email_templates()
        self.email_var = tk.StringVar()
        self.email_var.set(self.email_templates[0])
    
        self._set_current_email()
        self._create_email_menu()
        
        create_email_btn = tk.Button(self.email_frame,
                                  text='Create Email',
                                  width=10,
                                  command=self._create_email)
        
        add_email_template_btn = tk.Button(self.email_frame,
                                     text="Edit Templates",
                                     command=lambda self=self: AddEmailWindow(self))
        
        other_tasks_btn = tk.Button(misc_func_frame,
                                    text="Other Tasks",
                                    command=lambda self=self: AdminTasksWindow(self))
        
        #***GRIDDING***

        self.email_frame.grid(row=0, column=0, padx=10, pady=10)
        self.options_frame.grid(row=0, column=1)
        misc_func_frame.grid()
        
        docket_label.grid(row=0, column=0, sticky="e")
        self.dkt_entry.grid(row=0, column=1, pady=10, sticky="w")
        create_email_btn.grid(row=2, column=0, padx=10, pady=10)
        add_email_template_btn.grid(row=2, column=1, padx=10, pady=10)

        other_tasks_btn.grid()
    
    def _center_window(self):
        windowWidth = 330
        windowHeight = 185
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        xCoord = int((screenWidth/2) - (windowWidth/2))
        yCoord = int((screenHeight/2) - (windowHeight/2))

        self.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCoord, yCoord))

    def _create_email(self, event=None):
        docket = self.dkt_entry.get()
        template_name = self.email_var.get()
        if len(docket) != 7 or not docket.isnumeric():
            return None

        email_data = db.get_email_by_template_name(template_name)
        
        email = email_factory(docket, email_data, self.email_options)
        self.dkt_entry.delete(0, tk.END)
        self._uncheck_email_options()
        email.create()

    def _create_email_menu(self):
        self.email_var.trace('w', self._on_email_select)
        self.email_menu = tk.OptionMenu(self.email_frame, self.email_var, *self.email_templates)
        if self.disable_menu:
            self.email_menu.configure(state="disabled")
        self._clear_email_options()
        self._set_email_options()
        self.email_menu.grid(row=1, columnspan=2, padx=5, pady=5)

    def _set_email_options(self):
        self.email_options = {}
        try:
            options_raw_text = self.current_email["options"]
        except KeyError:
            return None
        if options_raw_text == "":
            return None
        try:
            options_list = options_raw_text.split(",")
        except AttributeError:
            return None

        for option in options_list:
            option = option.strip()
            var = tk.IntVar()
            chk = tk.Checkbutton(self.options_frame, text=option, variable=var, onvalue=1, offvalue=0)
            chk.grid(stick="w")
            self.email_options[option] = var

    def _clear_email_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.email_options = {}

    def _uncheck_email_options(self):
        for chk_box_var in self.email_options.values():
            chk_box_var.set(0)

    def _get_email_templates(self):
        email_templates = db.get_email_options()
        if len(email_templates) == 0:
            email_templates.append("No Email Templates")
            self.disable_menu = True
        else:
            self.disable_menu = False
        self.email_templates = email_templates

    def _set_current_email(self) -> dict:
        template_name = self.email_var.get()
        current_email = db.get_email_by_template_name(template_name)
        self.current_email = current_email

    def _on_email_select(self, *args):
        self._set_current_email()
        self._clear_email_options()
        self._set_email_options()

    def _update_email_menu(self):
        self.email_menu.destroy()
        self._get_email_templates()
        self._create_email_menu()

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()


class AddEmailWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Template Editor")
        self.template_menu_frame = tk.Frame(self)
        entry_frame = tk.Frame(self)
        text_box_frame = tk.Frame(self)
        button_frame = tk.Frame(self)
        notice_frame = tk.Frame(self)

        template_menu_label = tk.Label(self.template_menu_frame, text="Template:")
        self._create_email_menu()

        template_name_label = tk.Label(entry_frame, text="Name:")
        self.template_name_entry = tk.Entry(entry_frame, width=35)

        subject_label = tk.Label(entry_frame, text="Subject:")
        self.subject_entry = tk.Entry(entry_frame, width=35)

        receiver_label = tk.Label(entry_frame, text="To:")
        self.receiver_entry = tk.Entry(entry_frame, width=50)

        cc_label = tk.Label(entry_frame, text="Cc:")
        self.cc_entry = tk.Entry(entry_frame, width=50)

        func_label = tk.Label(entry_frame, text="Function:")
        self.func_entry = tk.Entry(entry_frame, width=25)

        options_label = tk.Label(entry_frame, text="Options:")
        self.options_entry = tk.Entry(entry_frame, width=30)

        body_label = tk.Label(text_box_frame, text="Body:")
        self.body_text_box = tk.Text(text_box_frame, height=15, width=75)

        save_button = tk.Button(button_frame, text="Save", width=10, command=self._save)
        delete_button = tk.Button(button_frame, text="Delete", width=10, command=self._delete)
        clear_button = tk.Button(button_frame, text="Clear", width=10, command=self._clear)
        self.notice_label = tk.Label(notice_frame, text="")

        self._set_fields(parent.current_email)

        #***GRIDDING***
        self.template_menu_frame.grid()
        template_menu_label.grid(row=0, column=0)

        entry_frame.grid(padx=10, pady=10, sticky="w")
        template_name_label.grid(row=0, column=0, sticky="e")
        self.template_name_entry.grid(row=0, column=1, sticky="w")

        subject_label.grid(row=1, column=0, sticky="e")
        self.subject_entry.grid(row=1, column=1, sticky="w")

        func_label.grid(row=2, column=0, sticky="e")
        self.func_entry.grid(row=2, column=1, sticky="w")

        #entry frame column 2, 3
        receiver_label.grid(row=0, column=2, padx=7, pady=2, sticky="e")
        self.receiver_entry.grid(row=0, column=3)

        cc_label.grid(row=1, column=2, padx=7, pady=2, sticky="e")
        self.cc_entry.grid(row=1, column=3)

        options_label.grid(row=2, column=2, padx=7, pady=2, sticky="e")
        self.options_entry.grid(row=2, column=3, sticky="w")

        text_box_frame.grid(padx=10, pady=10)
        body_label.grid(row=0, column=0, sticky="e")
        self.body_text_box.grid(row=0, column=1, sticky="w")

        button_frame.grid()
        save_button.grid(row=0, column=0, padx=10, pady=5)
        delete_button.grid(row=0, column=1, padx=10, pady=5)
        clear_button.grid(row=0, column=2, padx=10, pady=5)

        notice_frame.grid(pady=5)
        self.notice_label.grid()   

    def _clear(self):
        self._empty_fields()
        if not self.parent.disable_menu:
            self.email_var.set("")

    def _save(self):
        email_data = {
            "template_name": self.template_name_entry.get(),
            "subject": self.subject_entry.get(),
            "body": self.body_text_box.get("1.0", tk.END).strip(),
            "receiver": self.receiver_entry.get(),
            "cc": self.cc_entry.get(),
            "func": self.func_entry.get(),
            "options": self.options_entry.get().strip()
        }
        try:
            db.save_email(email_data)
        except IntegrityError as e:
            self._give_notice_thread(f"Unable to save. Error: {e}")
            return None
        self.parent._get_email_templates()
        self.parent._update_email_menu()
        self._update_email_menu()
        self._give_notice_thread(f"Email template \"{email_data['template_name']}\" successfully saved.")

    def _delete(self):
        template_name = self.template_name_entry.get()
        if template_name == "":
            return None
        db.delete_email(template_name)
        self._empty_fields()
        self.parent._update_email_menu()
        self._update_email_menu()
        self._give_notice_thread(f"Email template {template_name} has been deleted.")

    def _give_notice_thread(self, message):
        Thread(target=self._give_notice, args=(message,)).start()

    def _give_notice(self, message):
        self.notice_label.config(text=message)
        time.sleep(3)
        self.notice_label.config(text="")

    def _set_fields(self, *args):
        self.parent.email_var.set(self.email_var.get())
        email_data = self.parent.current_email
        for key in email_data:
            if email_data[key] is None:
                email_data[key] = ""
        self._empty_fields()
        self.template_name_entry.insert(0, email_data.get("template_name", ""))
        self.subject_entry.insert(0, email_data.get("subject", ""))
        self.body_text_box.insert("1.0", email_data.get("body", ""))
        self.receiver_entry.insert(0, email_data.get("receiver", ""))
        self.cc_entry.insert(0, email_data.get("cc", ""))
        self.func_entry.insert(0, email_data.get("func", ""))
        self.options_entry.insert(0, email_data.get("options", ""))

    def _empty_fields(self):
        self.template_name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text_box.delete("1.0", tk.END)
        self.receiver_entry.delete(0, tk.END)
        self.cc_entry.delete(0, tk.END)
        self.func_entry.delete(0, tk.END)
        self.options_entry.delete(0, tk.END)

    def _create_email_menu(self):
        self.email_var = tk.StringVar()
        self.email_var.set(self.parent.email_var.get())
        self.email_var.trace("w", self._set_fields)
        self.email_menu = tk.OptionMenu(self.template_menu_frame, self.email_var, *self.parent.email_templates)
        if self.parent.disable_menu:
            self.email_menu.configure(state="disabled")
        self.email_menu.grid(row=0, column=1, columnspan=2, padx=5)

    def _update_email_menu(self):
        self.email_menu.destroy()
        self._create_email_menu()

class AdminTasksWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Admin Tasks")

        active_release_report_lbl = tk.Label(self, text="Generate Active Report:")
        update_active_release_report_btn = tk.Button(self,
                                          text="Update",
                                          command=self._update_inmates_pending_release,
                                          width=10)
        reset_active_release_report_btn = tk.Button(self,
                                              text="Reset",
                                              command=self._reset_inmates_pending_release,
                                              width=10)

        find_emails_lbl = tk.Label(self, text="Find PCSO Emails:")
        find_emails_btn = tk.Button(self,
                                    text="Run",
                                    command=get_emails,
                                    width=10)
        
        active_release_report_lbl.grid(row=0, column=0, padx=10, pady=10)
        update_active_release_report_btn.grid(row=0, column=1, padx=10, pady=10)
        reset_active_release_report_btn.grid(row=0, column=2, padx=10, pady=10)
        find_emails_lbl.grid(row=1, column=0, padx=10, pady=10)
        find_emails_btn.grid(row=1, column=1, padx=10, pady=10)


    def _reset_inmates_pending_release(self):
        inmates = get_inmates_from_csv()
        db.reset_inmates_pending_release_table(inmates)
        create_active_release_report(inmates)

    def _update_inmates_pending_release(self):
        inmates = db.get_inmates_pending_release()
        update_inmate_release_times(inmates)
        create_active_release_report(inmates)
        db.update_inmates_pending_release_table(inmates)
        

if __name__ == '__main__':
    window = UserInterface()
    window.mainloop()
