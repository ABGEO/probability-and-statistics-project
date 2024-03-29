from statistics import variance
from ChartWindow import ChartWindow
from tkinter import filedialog, ttk, messagebox
from tkinter import *

import numpy as np
import variables
import pandas as pd


class MainWindow:
    def __init__(self, master):
        """
        Constructor for MainWindow.
        :param master: Master TkInter object.
        """
        
        self.master = master
        self.width = 500
        self.height = 500

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coords = int((screen_width / 2) - (self.width / 2))
        y_coords = int((screen_height / 2) - (self.height / 2))

        master.title("ალბათობა და სტატისტიკა | თემური თაკალანძე")

        master.geometry("{}x{}+{}+{}".format(self.width, self.height, x_coords, y_coords))
        master.resizable(0, 0)

    def draw(self):
        """
        Draw main window.
        :return: void
        """

        # TODO: Fix widget positions.
        master = self.master

        # Create Open Database Button.
        Button(master, text="ბაზის იმპორტი", command=self.__import_database)\
            .pack(pady=(0, 10))

        # Create Parameters Label Frame.

        master.lf_parameters = LabelFrame(
            master,
            text="პარამეტრები",
            width=self.width / 2,
        )

        # Create Region selector.
        Label(master.lf_parameters, text="რეგიონი:").pack(pady=(10, 5))
        master.combo_box_region = ttk.Combobox(master.lf_parameters)
        master.combo_box_region.pack()

        # Create Data selector.
        Label(master.lf_parameters, text="მონაცემები:").pack(pady=(10, 5))
        master.combo_box_data = ttk.Combobox(master.lf_parameters, values=list(variables.tasks.keys()))
        master.combo_box_data.bind('<<ComboboxSelected>>', self.__combo_box_data_on_select)
        master.combo_box_data.pack()

        # Create Action selector.
        Label(master.lf_parameters, text="მოქმედება:").pack(pady=(10, 5))
        master.combo_box_action = ttk.Combobox(master.lf_parameters)
        master.combo_box_action.bind('<<ComboboxSelected>>', self.__combo_box_action_on_select)
        master.combo_box_action.pack()

        master.calculate_btn = Button(master.lf_parameters, text="დათვლა", command=self.__run_calculation)
        master.calculate_btn.pack(pady=(20, 0))

        master.lf_parameters.pack(ipadx=10, ipady=10)

        # End Create Parameters Label Frame.

        # Disable all elements into frame.
        self.__change_children_state(master.lf_parameters)

        # Create Details Label Frame.

        lf_data_details = LabelFrame(
            master,
            text="არჩეული მონაცემების დეტალები",
            width=self.width
        )

        master.data_details_label = Label(lf_data_details, text='', wraplength=self.width-20, justify=LEFT)
        master.data_details_label.pack(padx=0, pady=0)

        lf_data_details.pack(side=BOTTOM, ipadx=10, ipady=10)

        # End Create Details Label Frame.

        master.mainloop()

    def __import_database(self):
        """
        Create File Dialog for selecting database file.
        :return: void
        """

        filename = filedialog.askopenfilename(
            initialdir="data",
            title="აირჩიეთ ბაზა"
        )
        
        self.__read_database(filename) 
        
    def __read_database(self, filename):
        """
        Read database file.
        :param filename: File path for reading.
        :return: void
        """

        master = self.master

        try:
            xl_workbook = pd.ExcelFile(filename)
        except Exception:
            messagebox.showerror('შეცდომა', 'აირჩიეთ სწორი მონაცემთა ბაზა.')
            return 

        # Read the first sheet.
        df = xl_workbook.parse(0)

        # Get regions from database and put to regions Combo Box.
        master.combo_box_region['values'] = list(dict.fromkeys(df['რეგიონი'].tolist()))

        # Enable all elements into frame.
        self.__change_children_state(master.lf_parameters, NORMAL)

        self.excel_data = df

    @staticmethod
    def __change_children_state(widget, state=DISABLED):
        """
        Change state to given widget children.
        :param widget: Widget for changing.
        :param state:  New state.
        :return: void
        """

        for child in widget.winfo_children():
            try:
                child.configure(state=state)
            except:
                pass

    def __combo_box_data_on_select(self, event):
        """
        Select event for combo_box_data.
        :param event: Current event.
        :return: void
        """

        master = self.master
        selected_data_code = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data_code)
        selected_data_description = selected_data_details.get('description')
        selected_data_codes = selected_data_details.get('codes')
        selected_data_actions = selected_data_details.get('actions')
        selected_data_additional_index = selected_data_details.get('additional_index', -1)

        # Set Available actions to actions Combo Box.
        available_actions = []
        master.combo_box_action.set('')
        for action in selected_data_actions:
            available_actions.append(
                list(variables.actions.keys())[list(variables.actions.values()).index(action)]
            )
        master.combo_box_action['values'] = available_actions

        # Set text to Data Details panel.
        selected_data_codes_text = ""
        for code, description in selected_data_codes.items():
            selected_data_codes_text += "%s: %s\n" % (code, description)

        details_template = "არჩეული მონაცემების ნომერი: %s\n\n" \
                           "მონაცემების აღწერა:\n%s\n\n"
        template_data = (selected_data_code, selected_data_description)

        if selected_data_codes_text != "":
            details_template += "კოდების მნიშვნელობები:\n%s"
            template_data = template_data + (selected_data_codes_text, )

        if selected_data_additional_index != -1:
            details_template += "დამატებითი ველი: %s"
            template_data = template_data + (selected_data_additional_index, )

        master.data_details_label['text'] = details_template % template_data

    def __combo_box_action_on_select(self, event):
        """
        Select event for combo_box_action.
        :param event: Current event.
        :return: void
        """

        master = self.master
        selected_action = master.combo_box_action.get()
        selected_action_code = variables.actions.get(selected_action)

        if selected_action_code in [2, 3, 4, 5]:
            master.calculate_btn['text'] = 'დიაგრამის ჩვენება'
        else:
            master.calculate_btn['text'] = 'დათვლა'

    def __run_calculation(self):
        master = self.master
        selected_region = master.combo_box_region.get()
        selected_data = master.combo_box_data.get()
        selected_action = master.combo_box_action.get()
        
        if selected_region == '':
            messagebox.showerror('შეცდომა', 'აირჩიეთ რეგიონი!')
            master.combo_box_region.focus_set()
        elif selected_data == '':
            messagebox.showerror('შეცდომა', 'აირჩიეთ მონაცემები!')
            master.combo_box_data.focus_set()
        elif selected_action == '':
            messagebox.showerror('შეცდომა', 'აირჩიეთ მოქმედება!')
            master.combo_box_action.focus_set()
        else:
            # Filter data by region.
            df = self.excel_data
            
            # Filter by given region and column.
            data = df[df["რეგიონი"] == selected_region]
            data = data[variables.tasks.get(selected_data).get('index')]
            
            calculators = {
                1: self.__calculate_action_1,
                2: self.__calculate_action_2,
                3: self.__calculate_action_3,
                4: self.__calculate_action_4,
                5: self.__calculate_action_5,
                6: self.__calculate_action_6,
                7: self.__calculate_action_7,
                8: self.__calculate_action_8,
                9: self.__calculate_action_9,
                10: self.__calculate_action_10,
            }

            selected_action_code = variables.actions.get(selected_action)
            calculators.get(selected_action_code)(data)

    def __calculate_action_1(self, data):
        """
        Draw Distribution chart.
        :param data: Data.
        :return: void
        """

        master = self.master
        selected_data = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data)
        selected_data_description = selected_data_details.get('description')

        chart = ChartWindow('სიხშირული განაწილება', width=600, height=600)
        chart.distribution_chart(selected_data_description, data)

    def __calculate_action_2(self, data):
        """
        Draw bar chart.
        :param data: Data.
        :return: void
        """

        master = self.master
        selected_data = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data)
        selected_data_description = selected_data_details.get('description')
        selected_data_codes = selected_data_details.get('codes')

        new_data = {}
        for code, description in selected_data_codes.items():
            new_data[code] = {
                'description': description,
                'count': 0,
            }

        for i in list(data):
            new_data[i]['count'] += 1

        chart = ChartWindow('სვეტოვანი დიაგრამა', width=600, height=600)
        chart.bar_chart(selected_data_description, new_data)

    def __calculate_action_3(self, data):
        """
        Draw Linear chart.
        :param data: Data.
        :return: void
        """

        master = self.master
        df = self.excel_data
        selected_data = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data)
        selected_data_index = selected_data_details.get('index')
        selected_data_description = selected_data_details.get('description')

        selected_region = master.combo_box_region.get()

        data = df[df["რეგიონი"] == selected_region]
        quarter_data = {}
        for quart in range(1, 5):
            current_quarter_data = data[data["კვარტ"] == quart]
            current_quarter_data = current_quarter_data[selected_data_index]
            quarter_data[str(quart) + " კვარტილი"] = current_quarter_data.sum()

        chart = ChartWindow('ხაზოვანი დიაგრამა', width=600, height=600)
        chart.linear_chart(selected_data_description, quarter_data)

    def __calculate_action_4(self, data):
        """
        Draw pie chart.
        :param data: Data.
        :return: void
        """

        master = self.master
        selected_data = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data)
        selected_data_description = selected_data_details.get('description')
        selected_data_codes = selected_data_details.get('codes')

        new_data = {}
        for code, description in selected_data_codes.items():
            new_data[code] = {
                'description': description,
                'count': 0,
            }

        for i in list(data):
            new_data[i]['count'] += 1

        chart = ChartWindow('წრიული დიაგრამა', width=600, height=600)
        chart.pie_chart(selected_data_description, new_data)

    def __calculate_action_5(self, data):
        """
        Draw Scatter chart.
        :param data: Data.
        :return: void
        """

        master = self.master
        df = self.excel_data
        selected_data = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data)
        selected_data_description = selected_data_details.get('description')
        selected_data_additional_index = selected_data_details.get('additional_index')

        selected_region = master.combo_box_region.get()

        data2 = df[df["რეგიონი"] == selected_region]
        data2 = data2[selected_data_additional_index]

        chart = ChartWindow('გაბნევის დიაგრამა', width=600, height=600)
        chart.scatter_chart(selected_data_description, list(data), list(data2))

    @staticmethod
    def __calculate_action_6(data):
        """
        Calculate Average of given data.
        :param data: Data.
        :return: void
        """

        avg = float(data.mean())
        messagebox.showinfo('ინფორმაცია', 'მოცემული მონაცემების საშუალოა: %f' % avg)

    @staticmethod
    def __calculate_action_7(data):
        """
        Calculate Median of given data.
        :param data: Data.
        :return: void
        """

        median = float(data.median())
        messagebox.showinfo('ინფორმაცია', 'მოცემული მონაცემების მედიანაა: %f' % median)
        
    @staticmethod
    def __calculate_action_8(data):
        """
        Calculate Mode of given data.
        :param data: Data.
        :return: void
        """

        mode = float(data.mode())
        messagebox.showinfo('ინფორმაცია', 'მოცემული მონაცემების მოდაა: %f' % mode)

    @staticmethod
    def __calculate_action_9(data):
        """
        Calculate variance of given data.
        :param data: Data.
        :return: void
        """

        var = variance(data)
        messagebox.showinfo('ინფორმაცია', 'მოცემული მონაცემების დისპერსიაა: %f' % var)

    def __calculate_action_10(self, data):
        """
        Calculate Correlation.
        :param data: Data.
        :return: void
        """

        master = self.master
        df = self.excel_data
        selected_data = master.combo_box_data.get()
        selected_data_details = variables.tasks.get(selected_data)
        selected_data_additional_index = selected_data_details.get('additional_index')

        selected_region = master.combo_box_region.get()

        data2 = df[df["რეგიონი"] == selected_region]
        data2 = data2[selected_data_additional_index]

        correlation = np.corrcoef(data, data2)
        messagebox.showinfo('ინფორმაცია', 'მოცემული მონაცემების კორელაციის კოეფიციენტია: %f' % correlation.item(1))
