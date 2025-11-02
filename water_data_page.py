import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from fetch_json_data import fetch_data_from_json
from search_query import search_water_data
import csv

def water_data_page(root, frame, go_back):
    tk.Label(frame, text="Groundwater Data", font=("Arial", 18)).pack(pady=15)

    filt = tk.Frame(frame)
    filt.pack()
    tk.Label(filt, text="Region:").grid(row=0, column=1)
    region_entry = tk.Entry(filt)
    region_entry.grid(row=0, column=2)
    tk.Label(filt, text="Reservoir Type:").grid(row=0, column=3)
    res_entry = tk.Entry(filt)
    res_entry.grid(row=0, column=4)
    tk.Label(filt, text="Status:").grid(row=0, column=5)
    status_entry = tk.Entry(filt)
    status_entry.grid(row=0, column=6)

    # Table section (Treeview)
    columns = ("record_id", "name", "type", "region", "capacity", "current_level", "status")
    tree = ttk.Treeview(filt, columns=columns, show='headings')
    
    # Define column headings and widths
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120)

    data = fetch_data_from_json("./server/water_data.json")
    for record in data:
        tree.insert("", tk.END, values=(
            record.get("res_id"),
            record.get("name"),
            record.get("type"),
            record.get("region"),
            record.get("capacity"),
            record.get("current_level"),
            record.get("status")
        ))

    def update_table():
        # Clear previous rows
        for row in tree.get_children():
            tree.delete(row)
        # Fetch filtered data
        data = search_water_data(
            "./server/water_data.json",
            region=region_entry.get(),
            res_type=res_entry.get(),
            status=status_entry.get()
        )
        for record in data:
            tree.insert("", "end", values=(
                record.get("res_id"),
                record.get("name"),
                record.get("type"),
                record.get("region"),
                record.get("capacity"),
                record.get("current_level"),
                record.get("status")
            ))
    
    def save_table():
        try:
            rows = [tree.item(item)['values'] for item in tree.get_children()]
            if not rows:
                messagebox.showinfo("Save", "No data to save.")
                return
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
                initialfile='water_data.csv'
            )
            if not file_path:
                return
            headers = [tree.heading(c)['text'] for c in tree['columns']]
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            messagebox.showinfo("Save", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    tree.grid(row=1, column=0, columnspan=8)
    
    tk.Button(filt, text="Search", command=update_table).grid(row=0, column=7)
    # Bottom buttons: Save and Back
    bottom_frame = tk.Frame(frame)
    bottom_frame.pack(pady=10)
    tk.Button(bottom_frame, text="Save", command=save_table).pack(side="left", padx=6)
    tk.Button(bottom_frame, text="Back", command=go_back).pack(side="left")