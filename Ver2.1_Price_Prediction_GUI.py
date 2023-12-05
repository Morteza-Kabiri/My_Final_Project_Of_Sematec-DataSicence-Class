import sklearn
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import messagebox
from joblib import load
import numpy as np
import pandas as pd
import re

########################################################################################
DataSet_Path="H:\DataSets\HouseNew.csv"
# Load the CSV file into a DataFrame
df = pd.read_csv(DataSet_Path)

df = df.dropna(subset=['Address'])
df['Address'].fillna('Unknown', inplace=True)

df['Address'] = df['Address'].str.replace('\u200c', '')  # Remove '\u200c'
df['Address'] = df['Address'].str.strip() # Strip any remaining leading/trailing spaces

address_ends_with_ABAD = df[df['Address'].str.endswith('آباد')]

def add_space_if_needed(x):
    return x if x[-1] == ' ' else x[:-4] + ' ' + x[-4:]

# Apply the function and update the original DataFrame using .loc to avoid the warning
# address_ends_with_ABAD['Address'] = address_ends_with_ABAD['Address'].apply(lambda x: x if x[-1] == ' ' else x[:-4] + ' ' + x[-4:])
df.loc[address_ends_with_ABAD.index, 'Address'] = address_ends_with_ABAD['Address'].apply(add_space_if_needed)

Address_list = set(sorted(df['Address'].tolist()))

ddf = df.dropna(subset=['YearOfConstruction'])
df['YearOfConstruction'].fillna('Unknown', inplace=True)
YearOfConstruction_list = set(df['YearOfConstruction'].tolist())

########################################################################################
myForm = Tk()
myForm.title('Linear Regression GUI For Price House Perdiction')
myForm.geometry('480x420')
myForm.resizable(0, 0)
text_variables = {}
newdata_from_entry=[]

items = ['Elevator', 'Floor', 'Area', 'Parking', 'Room', 'Warehouse', 'YearOfConstruction', 'Address']
items_Farsi=['آسانسور', 'طبقه', 'مساحت', 'پارکینگ', 'تعداد اتاق', 'انباری','سال ساخت', 'آدرس']


# Elevator  Floor  Area  Parking  Room  Warehouse  YearOfConstruction Address
# 0         3.0    49        1     1          1                1392     10
# Price
# 1750000000
# newdata = [[1,3.0,60,1,1,1,1393,10]]
def validate_entries():
    for item, var in text_variables.items():
        if var.get().strip() == "":
            messagebox.showerror("خطا", "لطفا تمامی فیلدها را پر کنید.")
            return False
    return True
def predictPrice():
    if validate_entries():
        loaded_model = load('H:\MyProjects\Price_new_model.joblib')
        newdata_from_entry = []

        for item in items:
            input_value = text_variables[item].get()

            if item == 'Address'and input_value != '' :
                sorted_address_list = sorted(list(Address_list))
                index_item = sorted_address_list.index(input_value)
                numeric_value = float(index_item)
                newdata_from_entry.append(numeric_value)
            else:
                if (isinstance(input_value,str) or isinstance(input_value,bool)) and input_value.strip() == "":
                    input_value=0
                else:
                    numeric_value = float(input_value)
                    newdata_from_entry.append(numeric_value)

        newdata_from_entry_checked = []
        for i, item_data in enumerate(newdata_from_entry):
            if item_data is None:
                newdata_from_entry_checked.append(0)
            elif isinstance(item_data, str) and item_data.strip() == "":
                newdata_from_entry_checked.append(0)
            else:
                newdata_from_entry_checked.append(float(item_data))
        newdata = [newdata_from_entry_checked]
        predicted_price = loaded_model.predict(newdata)
        msg.showinfo(' پیش بینی قیمت براساس الگوریتم رگرسیون خطی ', f'قیمت پیش بینی شده برابر است با: {"{:,.0f}".format(predicted_price[0])}')
    


# Create labels and input widgets for each item in the list
for i, itemx in enumerate(items_Farsi):
    # Create a label
    label = Label(myForm, text=f'{itemx}: ')
    label.grid(row=i, column=0, padx=10, pady=10, sticky='w')


footer_label = Label(myForm, text='Ver2.0 - تهیه شده : توسط مرتضی کبیری پاییز 1402 - کلاس پایتون برای دیتاسایس')
footer_label.grid(row=15, column=0, columnspan=4, padx=10, pady=10, sticky='w')


def is_valid_integer(P):
    try:
        int(P)
        return True
    except ValueError:
        return False

def is_valid_float(P):
    try:
        float(P)
        return True
    except ValueError:
        return False
def validate_integer_input(P):
    if len(P)==0 or P == "\x08":
        return True  # Allow Backspace key
    if P == "":
        messagebox.showerror("خطا", "لطفا عدد معتبر وارد نمایید:")
        return False
    if P == "-":
        messagebox.showerror("خطا", "لطفا عدد معتبر وارد نمایید:")
        return False

    if is_valid_integer(P) :
        return True
    else:
        messagebox.showerror("خطا", "لطفا عدد معتبر وارد نمایید:")
        return False


def validate_numeric_input(P):
    if len(P)==0 or P == "\x08":
        return True  # Allow Backspace key
    if P == "":
        messagebox.showerror("خطا", "لطفا عدد معتبر وارد نمایید:")
        return False
    if P == "-":
        messagebox.showerror("خطا", "لطفا عدد معتبر وارد نمایید:")
        return False
    if is_valid_float(P) :
        return True
    else:
        messagebox.showerror("خطا", "لطفا عدد معتبر وارد نمایید:")
        return False




for i, item in enumerate(items):
    # Create input widgets based on the item
    if item in ['Elevator', 'Parking', 'Warehouse']:
        # Create radio buttons for 'Elevator', 'Parking', and 'Warehouse'
        var = StringVar()
        # var.set('True')  # Default selection
        radio_true = ttk.Radiobutton(myForm, text='دارد', variable=var, value=1)
        radio_false = ttk.Radiobutton(myForm, text='ندارد', variable=var, value=0)
        radio_true.grid(row=i, column=1, padx=10, pady=10, sticky='w')
        radio_false.grid(row=i, column=1, padx=10, pady=10, sticky='n')
        text_variables[item] = var

    elif item == 'YearOfConstruction':
        # Create a combo box for 'YearOfConstruction' with YearOfConstruction_list values
        var = StringVar()
        combo = ttk.Combobox(myForm, textvariable=var, values=list(YearOfConstruction_list),state='readonly')
        combo.grid(row=i, column=1, padx=10, pady=10, sticky='w')
        text_variables[item] = var

    elif item == 'Address':
        # Create a combo box for 'Address' with Address_list values
        var = StringVar()
        combo = ttk.Combobox(myForm, textvariable=var, values=sorted(list(Address_list)),state='readonly')
        combo.grid(row=i, column=1, padx=10, pady=10, sticky='w')
        text_variables[item] = var
    elif item == 'Area':
        var = StringVar()
        validate_num = myForm.register(validate_numeric_input)
        entry = ttk.Entry(myForm, width=20, textvariable=var, validate="key", validatecommand=(validate_num, "%P"))
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='w')
        text_variables[item] = var
    else:
        var = StringVar()
        validate_int = myForm.register(validate_integer_input)
        entry = ttk.Entry(myForm, width=20, textvariable=var, validate="key", validatecommand=(validate_int, "%P"))
        entry.grid(row=i, column=1, padx=10, pady=10, sticky='w')
        text_variables[item] = var


custom_style1 = ttk.Style()
custom_style1.configure('Red.TButton', foreground='red', background='blue')
custom_style2 = ttk.Style()
custom_style2.configure('Green.TButton', foreground='green', background='blue')

btnClose = ttk.Button(myForm, text='بستن', width=20, command=myForm.quit ,style='Red.TButton')
btnClose.grid(row=8, column=2, padx=10, pady=10, sticky='w')

btnPredict = ttk.Button(myForm, text='تخمین قیمت', width=20, command=predictPrice ,style='Green.TButton')
btnPredict.grid(row=8, column=1, padx=10, pady=10, sticky='w')

myForm.mainloop()

