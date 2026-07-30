import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv

# ==============================
# DATABASE
# ==============================

db = sqlite3.connect("Crane_CMMS.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
equipment TEXT,
component TEXT,
fault_type TEXT,
fault_code TEXT,
description TEXT,
technician TEXT,
shift TEXT,
start_time TEXT,
end_time TEXT,
duration TEXT
)
""")

db.commit()

# ==============================
# LISTS
# ==============================

equipment_list = [f"Crane-{i}" for i in range(1,13)] + [f"RTG-{i}" for i in range(1,41)]

component_list = [
    "Hoist","Trolley","Gantry","Boom","Spreader",
    "PLC","Drives","Other","Operation Fault"
]

fault_type_list = ["Electrical","Mechanical","Operation"]

shift_list = ["A","B","C"]

# ==============================
# FUNCTIONS
# ==============================

def start_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_entry.delete(0, tk.END)
    start_entry.insert(0, now)

def stop_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_entry.delete(0, tk.END)
    end_entry.insert(0, now)
    calculate_duration()

def calculate_duration():
    try:
        s = datetime.strptime(start_entry.get(), "%Y-%m-%d %H:%M:%S")
        e = datetime.strptime(end_entry.get(), "%Y-%m-%d %H:%M:%S")
        duration_label.config(text=str(e - s))
    except:
        messagebox.showerror("Error","Invalid Time Format")

def clear_fields():
    equipment_box.set("")
    component_box.set("")
    fault_type_box.set("")
    fault_code_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    technician_entry.delete(0, tk.END)
    shift_box.set("")
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    duration_label.config(text="00:00:00")

def save_record():

    data = (
        equipment_box.get(),
        component_box.get(),
        fault_type_box.get(),
        fault_code_entry.get(),
        description_entry.get(),
        technician_entry.get(),
        shift_box.get(),
        start_entry.get(),
        end_entry.get(),
        duration_label.cget("text")
    )

    if "" in data:
        messagebox.showwarning("Missing","Fill all fields")
        return

    cursor.execute("""
    INSERT INTO maintenance
    (equipment,component,fault_type,fault_code,description,technician,shift,start_time,end_time,duration)
    VALUES(?,?,?,?,?,?,?,?,?,?)
    """, data)

    db.commit()
    messagebox.showinfo("Saved","Record Saved Successfully")

    clear_fields()

def show_history():

    win = tk.Toplevel()
    win.title("History")
    win.geometry("1100x400")

    tree = ttk.Treeview(win)
    tree["columns"] = ("ID","Equip","Comp","Type","Code","Desc","Tech","Shift","Start","End","Dur")

    for col in tree["columns"]:
        tree.heading(col,text=col)
        tree.column(col,width=100)

    cursor.execute("SELECT * FROM maintenance")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)

def export_csv():
    file = filedialog.asksaveasfilename(defaultextension=".csv")
    if not file:
        return

    cursor.execute("SELECT * FROM maintenance")
    rows = cursor.fetchall()

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID","Equip","Comp","Type","Code","Desc","Tech","Shift","Start","End","Dur"])
        writer.writerows(rows)

    messagebox.showinfo("Exported","Saved to CSV")

# ==============================
# GUI
# ==============================

win = tk.Tk()
win.title("CRANE CMMS SYSTEM")
win.geometry("750x750")

tk.Label(win,text="CRANE MAINTENANCE SYSTEM",font=("Arial",18,"bold")).pack(pady=10)

def add_field(label, widget):
    tk.Label(win,text=label).pack()
    widget.pack()

equipment_box = ttk.Combobox(win, values=equipment_list, width=40)
component_box = ttk.Combobox(win, values=component_list, width=40)
fault_type_box = ttk.Combobox(win, values=fault_type_list, width=40)
fault_code_entry = tk.Entry(win, width=40)
description_entry = tk.Entry(win, width=60)
technician_entry = tk.Entry(win, width=40)
shift_box = ttk.Combobox(win, values=shift_list, width=40)
start_entry = tk.Entry(win, width=40)
end_entry = tk.Entry(win, width=40)

add_field("Equipment", equipment_box)
add_field("Component", component_box)
add_field("Fault Type", fault_type_box)
add_field("Fault Code", fault_code_entry)
add_field("Description", description_entry)
add_field("Technician", technician_entry)
add_field("Shift", shift_box)
add_field("Start Time", start_entry)

tk.Button(win,text="Start Now",command=start_now).pack()

add_field("End Time", end_entry)

tk.Button(win,text="Stop Now",command=stop_now).pack()

tk.Label(win,text="Downtime").pack()
duration_label = tk.Label(win,text="00:00:00",font=("Arial",12,"bold"))
duration_label.pack()

tk.Button(win,text="Calculate",command=calculate_duration).pack(pady=5)
tk.Button(win,text="Save",command=save_record,width=20).pack(pady=10)
tk.Button(win,text="View History",command=show_history,width=20).pack()
tk.Button(win,text="Export CSV",command=export_csv,width=20).pack(pady=5)

# ==============================
# SIGNATURE (اسمك تحت)
# ==============================

tk.Label(
    win,
    text="AHMED ZEZO",
    font=("Segoe Script",16,"bold"),
    fg="blue"
).pack(side="bottom", pady=10)

win.mainloop()
