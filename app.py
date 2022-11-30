# customtkinter from: https://github.com/TomSchimansky/CustomTkinter
# makes tkinter look modern
import customtkinter as tk
import os
import shutil
import pickle


# Sets Customtkinter's global attributes
def set_tkinter_global():
    tk.set_appearance_mode("System")  # Modes: system (default), light, dark
    tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# Creates a popup box with a message and a button that closes it
# Customtkinter does not provide the messagebox normally found in tkinter
def message_box(msg: str, ctx: tk.CTk):
    window = tk.CTkToplevel(ctx)
    window.geometry("320x200")
    window.title("Error")

    label = tk.CTkLabel(window, text=msg)
    label.pack(side="top", fill="both", expand=True, padx=40, pady=20)

    button = tk.CTkButton(window, text="OK", command=window.destroy)
    button.pack(side="bottom", padx=40, pady=20)


class App:
    def rename_button_callback(self):
        # Switch
        self.rename_check = not self.rename_check

    def update_button_callback(self):
        # Make sure that all the appropriate settings have been set
        if not self._check_all_for_update():
            return

        # Get all paths to each class
        paths = []
        for year in self.years.get().split(','):
            path = self.year_path.get() + "\\" + year
            for folder in os.listdir(path):
                paths.append(path + "\\" + folder)

        # Copy the includes into each class directory
        for path in paths:
            for include in self.include.get().split(','):
                shutil.copyfile(self.temp_scr.get() + "\\" + include, path + "\\" + include)

    def add_button_callback(self):
        # Make sure that all the appropriate settings have been set
        if not self._check_add_update():
            return

        # Make class dir if it doesn't exist
        path = self.year_path.get() + "\\" + self.year_names.get() + "\\" + self.classes.get()
        if not os.path.exists(path):
            os.makedirs(path)

        # Copy Includes
        for include in self.include.get().split(','):
            shutil.copyfile(self.temp_scr.get() + "\\" + include, path + "\\" + include)

        # Copy template / Rename template
        shutil.copyfile(self.temp_scr.get() + "\\" + self.template.get(), path + "\\" + self.template.get())
        if self.rename_check:
            os.rename(path + "\\" + self.template.get(), path + "\\" + self.classes.get() + ".tex")

    # Make sure that the template source path exists
    def _check_templ_src(self):
        value = self.temp_scr.get()
        if not os.path.exists(value):
            return False
        else:
            return True

    def _tmpl_src_fail(self):
        message_box("Template Source path is invalid", self.context)

    # Make sure that the include files exist
    def _check_includes(self):
        value = self.include.get()
        files = value.split(',')
        for file in files:
            if not os.path.isfile(self.temp_scr.get() + "\\" + file):
                return False

        return True

    def _includes_fail(self):
        message_box("One or more include files do not exist", self.context)

    # Make sure that the path to the year exists
    def _check_year_path(self):
        value = self.year_path.get()
        if not os.path.exists(value):
            return False
        else:
            return True

    def _year_path_fail(self):
        message_box("Year Path is invalid", self.context)

    # Check that each year folder exists
    def _check_years(self):
        value = self.years.get()
        files = value.split(',')
        for file in files:
            if not os.path.isdir(self.year_path.get() + "\\" + file):
                return False

        return True

    def _years_fail(self):
        message_box("One or more years do not exist", self.context)

    # Check that the set year exists
    def _check_year(self):
        value = self.year_names.get()
        if value in self.years.get().split(','):
            return True
        return False

    def _year_fail(self):
        message_box("Year doesn't exist", self.context)

    # Check that the template file exists
    def _check_template(self):
        value = self.template.get()
        if not os.path.isfile(self.temp_scr.get() + "\\" + value):
            return False
        return True

    def _template_fail(self):
        message_box("Could not find template file", self.context)

    # Check for all settings relevant to the Update Includes button
    def _check_all_for_update(self) -> bool:
        if not self._check_includes():
            self._includes_fail()
            return False
        elif not self._check_template():
            self._template_fail()
            return False
        elif not self._check_years():
            self._years_fail()
            return False
        elif not self._check_year_path():
            self._year_path_fail()
            return False
        elif not self._check_templ_src():
            self._tmpl_src_fail()
            return False

        return True

    # Check for all settings relevant to the Add Class button
    def _check_add_update(self) -> bool:
        if not self._check_year_path():
            self._year_path_fail()
            return False
        elif not self._check_year():
            self._year_fail()
            return False
        elif not self._check_includes():
            self._includes_fail()
            return False
        elif not self._check_template():
            self._template_fail()
            return False
        elif not self._check_year_path():
            self._year_path_fail()
            return False
        elif not self._check_templ_src():
            self._tmpl_src_fail()
            return False

        return True

    # -------------------------------- Save/Load -------------------------------- #
    # Modified from: https://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python

    # Dump app settings into save file
    # Triggered when the window is closed
    def _on_window_close(self) -> ():
        with open("settings.pkl", 'wb') as f:
            pickle.dump([self.temp_scr.get(),
                        self.include.get(),
                        self.template.get(),
                        self.year_path.get(),
                        self.years.get(),
                        self.classes.get(),
                        self.year_names.get()], f)

        self.context.destroy()

    # Restore the app's settings from save file
    def _restore(self) -> ():
        if os.path.isfile("settings.pkl"):
            with open("settings.pkl", 'rb') as f:
                data = pickle.load(f)
                self.temp_scr.set(data[0])
                self.include.set(data[1])
                self.template.set(data[2])
                self.year_path.set(data[3])
                self.years.set(data[4])
                self.classes.set(data[5])
                self.year_names.set(data[6])

    def __init__(self):
        set_tkinter_global()

        # Create the main window
        self.context = tk.CTk()
        self.context.title("Noter")
        self.context.geometry("800x480")
        self.context.protocol("WM_DELETE_WINDOW", self._on_window_close)

        # Initialize settings
        self.temp_scr = tk.StringVar()
        self.include = tk.StringVar()
        self.template = tk.StringVar()
        self.year_path = tk.StringVar()
        self.years = tk.StringVar()
        self.classes = tk.StringVar()
        self.year_names = tk.StringVar()
        self.rename_check = False

        # Loads saved settings if a save file exists
        self._restore()

        # Generated by PAGE(tool that allows you to visually create tkinter guis and then export them to python code)
        # Modified by me
        # Create the gui of the main window
        self.left_frame = tk.CTkFrame()
        self.left_frame.place(relx=0.0, rely=0.0, relheight=1.006, relwidth=0.707)
        self.left_frame.configure(relief='groove')
        self.left_frame.configure(borderwidth="2")

        self.temp_scr_entry = tk.CTkEntry(self.left_frame, textvariable=self.temp_scr)
        self.temp_scr_entry.place(relx=0.037, rely=0.075, height=20, relwidth=0.594)
        self.temp_scr_entry.configure(font="TkFixedFont")

        self.temp_src_label = tk.CTkLabel(self.left_frame)
        self.temp_src_label.place(relx=0.037, rely=0.019, height=21, width=104)
        self.temp_src_label.configure(anchor='w')
        self.temp_src_label.configure(compound='left')
        self.temp_src_label.configure(text='''Template Source''')

        self.include_entry = tk.CTkEntry(self.left_frame, textvariable=self.include)
        self.include_entry.place(relx=0.037, rely=0.187, height=20, relwidth=0.594)
        self.include_entry.configure(font="TkFixedFont")

        self.include_label = tk.CTkLabel(self.left_frame)
        self.include_label.place(relx=0.037, rely=0.131, height=21, width=74)
        self.include_label.configure(anchor='w')
        self.include_label.configure(compound='left')
        self.include_label.configure(text='''Include Files''')

        self.template_entry = tk.CTkEntry(self.left_frame, textvariable=self.template)
        self.template_entry.place(relx=0.037, rely=0.299, height=20, relwidth=0.594)
        self.template_entry.configure(font="TkFixedFont")

        self.template_label = tk.CTkLabel(self.left_frame)
        self.template_label.place(relx=0.037, rely=0.243, height=21, width=94)
        self.template_label.configure(anchor='w')
        self.template_label.configure(compound='left')
        self.template_label.configure(text='''Template File''')

        self.rename_check_button = tk.CTkCheckBox(self.left_frame, command=self.rename_button_callback)
        self.rename_check_button.place(relx=0.037, rely=0.897, relheight=0.047, relwidth=0.24)
        self.rename_check_button.configure(text='''Rename Template''')

        self.year_path_entry = tk.CTkEntry(self.left_frame, textvariable=self.year_path)
        self.year_path_entry.place(relx=0.037, rely=0.411, height=20, relwidth=0.594)
        self.year_path_entry.configure(font="TkFixedFont")

        self.year_path_label = tk.CTkLabel(self.left_frame)
        self.year_path_label.place(relx=0.037, rely=0.355, height=21, width=64)
        self.year_path_label.configure(anchor='w')
        self.year_path_label.configure(compound='left')
        self.year_path_label.configure(text='''Year Path''')

        self.years_entry = tk.CTkEntry(self.left_frame, textvariable=self.years)
        self.years_entry.place(relx=0.037, rely=0.523, height=20, relwidth=0.594)
        self.years_entry.configure(font="TkFixedFont")

        self.years_label = tk.CTkLabel(self.left_frame)
        self.years_label.place(relx=0.037, rely=0.467, height=21, width=34)
        self.years_label.configure(anchor='w')
        self.years_label.configure(compound='left')
        self.years_label.configure(text='''Years''')

        self.right_frame = tk.CTkFrame()
        self.right_frame.place(relx=0.713, rely=0.0, relheight=1.006, relwidth=0.292)
        self.right_frame.configure(relief='groove')
        self.right_frame.configure(borderwidth="2")

        self.update_button = tk.CTkButton(self.right_frame, command=self.update_button_callback)
        self.update_button.place(relx=0.222, rely=0.15, height=24, width=107)
        self.update_button.configure(compound='left')
        self.update_button.configure(pady="0")
        self.update_button.configure(text='''Update Includes''')

        self.class_label = tk.CTkLabel(self.right_frame)
        self.class_label.place(relx=0.089, rely=0.262, height=21, width=84)
        self.class_label.configure(anchor='w')
        self.class_label.configure(compound='left')
        self.class_label.configure(text='''Class Name''')

        self.class_entry = tk.CTkEntry(self.right_frame, textvariable=self.classes)
        self.class_entry.place(relx=0.089, rely=0.318, height=20, relwidth=0.773)
        self.class_entry.configure(font="TkFixedFont")

        self.add_button = tk.CTkButton(self.right_frame, command=self.add_button_callback)
        self.add_button.place(relx=0.222, rely=0.075, height=24, width=107)
        self.add_button.configure(compound='left')
        self.add_button.configure(pady="0")
        self.add_button.configure(text='''Add Class''')

        self.year_name_entry = tk.CTkEntry(self.right_frame, textvariable=self.year_names)
        self.year_name_entry.place(relx=0.089, rely=0.449, height=20, relwidth=0.773)
        self.year_name_entry.configure(font="TkFixedFont")

        self.year_name_label = tk.CTkLabel(self.right_frame)
        self.year_name_label.place(relx=0.089, rely=0.393, height=21, width=74)
        self.year_name_label.configure(anchor='w')
        self.year_name_label.configure(compound='left')
        self.year_name_label.configure(text='''Year Name''')

    def app_loop(self):
        self.context.mainloop()
