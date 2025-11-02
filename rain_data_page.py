import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from fetch_json_data import fetch_data_from_json
from search_query import search_rain_data
import csv


def rain_data_page(root, frame, go_back):
    tk.Label(frame, text="Rainfall Data", font=("Arial", 18)).pack(pady=15)

    start_var = tk.StringVar()
    end_var = tk.StringVar()

    # Filter section
    filt = tk.Frame(frame)
    filt.pack()
    tk.Label(filt, text="Start Date:").grid(row=0, column=0)
    start_date = DateEntry(filt, textvariable=start_var)
    start_var.set('')
    start_date.grid(row=0, column=1)
    tk.Label(filt, text="End Date:").grid(row=0, column=2)
    end_date = DateEntry(filt, textvariable=end_var)
    end_var.set('')
    end_date.grid(row=0, column=3)    
    tk.Label(filt, text="Season:").grid(row=0, column=4)
    season_entry = tk.Entry(filt)
    season_entry.grid(row=0, column=5)
    tk.Label(filt, text="Region:").grid(row=0, column=6)
    region_entry = tk.Entry(filt)
    region_entry.grid(row=0, column=7)

    # Table section (Treeview)
    columns = ("record_id", "date", "season", "region", "rainfall")
    tree = ttk.Treeview(filt, columns=columns, show='headings')
    
    # Define column headings and widths
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120)

    data = fetch_data_from_json("./server/rainfall_data.json")
    for record in data:
        tree.insert("", tk.END, values=(
            record.get("record_id"),
            record.get("date"),
            record.get("season"),
            record.get("region"),
            record.get("rainfall")
        ))

    def update_table():
        # Clear previous rows
        for row in tree.get_children():
            tree.delete(row)
        # Fetch filtered data
        start_val = start_var.get().strip()
        end_val = end_var.get().strip()
        start_iso = start_date.get_date().isoformat() if start_val else None
        end_iso = end_date.get_date().isoformat() if end_val else None
        data = search_rain_data(
            "./server/rainfall_data.json",
            region=region_entry.get(),
            start_date=start_iso,
            end_date=end_iso,
            season=season_entry.get()
        )
        for record in data:
            tree.insert("", "end", values=(
                record.get("record_id"),
                record.get("date"),
                record.get("season"),
                record.get("region"),
                record.get("rainfall")
            ))
    
    def save_table():
        try:
            # Collect rows currently in the treeview
            rows = [tree.item(item)['values'] for item in tree.get_children()]
            if not rows:
                messagebox.showinfo("Save", "No data to save.")
                return
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
                initialfile='rainfall_data.csv'
            )
            if not file_path:
                return
            # Use column headings from the Treeview
            headers = [tree.heading(c)['text'] for c in tree['columns']]
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            messagebox.showinfo("Save", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    tree.grid(row=1, column=0, columnspan=9)
    
    tk.Button(filt, text="Search", command=update_table).grid(row=0, column=8)
    # Bottom buttons: Save and Back
    bottom_frame = tk.Frame(frame)
    bottom_frame.pack(pady=10)
    tk.Button(bottom_frame, text="Save", command=save_table).pack(side="left", padx=6)
    tk.Button(bottom_frame, text="Back", command=go_back).pack(side="left")
