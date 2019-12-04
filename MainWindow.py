from tkinter import filedialog, ttk
from tkinter import *
import pandas as pd


class MainWindow:
    def __init__(self, master):
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

        self.tasks = {
            'D6': ('საპენსიო ასაკის (65+) მამაკაცების რაოდენობა ოჯახში', {}),
            'E2': (
                'ვის ეკუთვნის საცხოვრისი, რომელშიც ოჯახი ცხოვრობს',
                {
                    1: 'ეკუთვნის შინამეურნეობას',
                    2: 'დაქირავებულია',
                    3: 'დაგირავებულია',
                    4: 'უფასო სარგებლობაშია'
                }
            ),
            'F22': ('გაზქურების/ელექტროქურების რაოდენობა ოჯახში', {}),
            'S3': ('რამდენი ლარი სჭირდება თვეში, თქვენს ოჯახს სურსათისა და სხვა აუცილებელი ხარჯებისათვის', {}),
            'I4': ('ოჯახის შემოსავლები ქონების გაქირავებიდან(საშუალოდ თვეში)', {}),
            'C5': ('ოჯახის დანახარჯები საწვავზე და ელექტროენერგიაზე (ლარი, საშუალოდ თვეში)', {}),
        }

    def draw(self):
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
        master.combo_box_data = ttk.Combobox(master.lf_parameters, values=list(self.tasks.keys()))
        master.combo_box_data.bind('<<ComboboxSelected>>', self.__update_data_details)
        master.combo_box_data.pack()

        # Create Action selector.
        Label(master.lf_parameters, text="მოქმედება:").pack(pady=(10, 5))
        master.combo_box_action = ttk.Combobox(master.lf_parameters)
        master.combo_box_action.pack()

        Button(master.lf_parameters, text="დათვლა", command=print('დათვლა'))\
            .pack(pady=(20, 0))

        master.lf_parameters.pack(ipadx=10, ipady=10)

        # End Create Parameters Label Frame.

        # Disable all elements into frame.
        self.__change_children_state(master.lf_parameters)

        # Create Details Label Frame.

        lf_data_details = LabelFrame(
            master,
            text="არჩეული მონაცემების დეტალები",
            width=self.width,
            height=100
        )

        master.data_details_label = Label(lf_data_details, text='')
        master.data_details_label.pack(padx=0, pady=0)

        lf_data_details.pack(side=BOTTOM, ipadx=10, ipady=10)

        # End Create Details Label Frame.

        master.mainloop()

    def __import_database(self):
        master = self.master

        master.filename = filedialog.askopenfilename(
            initialdir="data",
            title="აირჩიეთ ბაზა"
        )

        xl_workbook = pd.ExcelFile(master.filename)
        df = xl_workbook.parse(0)

        master.combo_box_region['values'] = list(dict.fromkeys(df['რეგიონი'].tolist()))

        self.__change_children_state(master.lf_parameters, NORMAL)

    @staticmethod
    def __change_children_state(widget, state=DISABLED):
        for child in widget.winfo_children():
            try:
                child.configure(state=state)
            except:
                pass

    def __update_data_details(self, event):
        master = self.master
        selected_data = master.combo_box_data.get()
        selected_data_description = self.tasks.get(selected_data)[0]
        selected_data_codes = self.tasks.get(selected_data)[1]

        selected_data_codes_text = ""
        for code, description in selected_data_codes.items():
            selected_data_codes_text += "%s: %s\n" % (code, description)

        details_template = "არჩეული მონაცემების ნომერი: %s\n\n" \
                           "მონაცემების აღწერა: %s\n\n" \
                           "კოდების მნიშვნელობები:\n %s"

        master.data_details_label['text'] \
            = details_template % (selected_data, selected_data_description, selected_data_codes_text)
