# import modules
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='expense.db')

# global variables
count = 0
selected_rowid = 0

# functions


def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')


def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')


def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for record in f:
        tv.insert(parent='', index='end', iid=count,
                  values=(record[0], record[1], record[2], record[3]))
        count += 1
    tv.after(400, refreshData)


def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as e:
        pass


def update_record():
    global selected_rowid

    selected = tv.focus()
    # Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(),
                          dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(
            namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as e:
        messagebox.showerror('Error',  e)

        # Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)


def totalSpent():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo(
                'Total Spent: ', f"Total Expense: {round(j,2)} \n")


def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()


def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()


# create tkinter object
root = Tk()
root.title('Expense Tracker')

root.minsize(700, 400)  # set the minimum size of the window (width , height)

# variables
f = ('Trebuchet MS', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widget
f2 = Frame(root)
f2.pack(pady=5)

f1 = Frame(
    root,
    padx=10,
    pady=10,
)
f1.place(relx=0.5, rely=0.72, anchor=CENTER)
# f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


# Action buttons
cur_date = Button(
    f1,
    text='Current Date',
    font=f,
    bg='#04C4D9',
    command=setDate,
    width=15
)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    command=saveRecord,
    bg='green',
    fg='white'
)

clr_btn = Button(
    f1,
    text='Clear Entry',
    font=f,
    command=clearEntries,
    bg='purple',
    fg='white'
)

quit_btn = Button(
    f1,
    text='Exit',
    font=f,
    command=root.destroy,
    bg='darkblue',
    fg='white'
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    bg="deeppink",
    command=totalSpent,
)

update_btn = Button(
    f1,
    text='Update',
    bg='yellow',
    command=update_record,
    font=f
)

del_btn = Button(
    f1,
    text='Delete',
    bg='red',
    command=deleteRow,
    font=f
)

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_spent.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Item no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function
fetch_records()

# infinite loop
root.mainloop()
