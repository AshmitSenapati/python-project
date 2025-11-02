import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry # Import the DateEntry widget
from tkinter import ttk # Import themed tkinter widgets
from tkinter import filedialog # Import the file dialog module
import json # Import the json module

def admin_dashboard(parent):
    """
    Opens the main 'Weather Report' dashboard window, 
    now with a tabbed interface for Rainfall and Ground Water.
    """
    # Define colors and fonts
    WIN_BG = "#e0e0e0" # A light grey background
    FRAME_BG = "#e0e0e0"
    LABEL_FONT = ("Helvetica", 10)
    TITLE_FONT = ("Helvetica", 16, "bold")
    
    dashboard_window = tk.Toplevel(parent)
    dashboard_window.title("Weather Report")
    dashboard_window.geometry("1000x850") # Increased height for tabs
    dashboard_window.configure(bg=WIN_BG)
    
    # --- Load Rainfall Data File ---
    try:
        with open("./server/rainfall_data.json", 'r', encoding='utf-8') as f:
            rainfall_data_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", 
            f"Failed to load rainfall_data.json.\nError: {e}",
            parent=dashboard_window) # Show on top
        dashboard_window.destroy()
        return
    # --- End Rainfall Data Load ---
    
    # --- Load Groundwater Data File ---
    try:
        with open("./server/water_data.json", 'r', encoding='utf-8') as f:
            groundwater_data_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", 
            f"Failed to load water_data.json.\nError: {e}",
            parent=dashboard_window) # Show on top
        dashboard_window.destroy()
        return
    # --- End Groundwater Data Load ---
    
    # --- Style for Tabs ---
    # This makes the tab text larger and more readable
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=LABEL_FONT, padding=[10, 5])
    
    # --- Notebook (Tab) Widget ---
    notebook = ttk.Notebook(dashboard_window)
    
    # --- Create Tabs ---
    rainfall_tab = ttk.Frame(notebook, padding=10)
    groundwater_tab = ttk.Frame(notebook, padding=10)
    
    notebook.add(rainfall_tab, text="   Rainfall Data   ")
    notebook.add(groundwater_tab, text="   Ground Water Data   ")
    
    notebook.pack(pady=10, padx=10, expand=True, fill="both")
    
    
    # --- ###################### ---
    # --- BEGIN: RAINFALL TAB  ---
    # --- ###################### ---
    
    # --- Treeview (Rainfall Data Table) ---
    table_frame_rf = tk.Frame(rainfall_tab) # Parent is rainfall_tab
    table_frame_rf.pack(pady=20, padx=20, fill="both", expand=True)
    
    columns_rf = ("record_id", "date", "season", "region", "rainfall")
    # --- MODIFIED: Added selectmode="extended" to allow multi-select ---
    tree_rf = ttk.Treeview(table_frame_rf, columns=columns_rf, show="headings", selectmode="extended")
    
    # --- Filter Function (Rainfall) ---
    def filter_data_rf():
        """
        Filters data for the RAINFALL table.
        """
        # Get values from rainfall filters
        start_val = start_var.get().strip()
        end_val = end_var.get().strip()
        start_iso = entry_start_date_rf.get_date().isoformat() if start_val else None
        end_iso = entry_end_date_rf.get_date().isoformat() if end_val else None
        season = season_combobox_rf.get().strip().lower()
        region = entry_region_rf.get().strip().lower()
        
        # Clear the existing rainfall table data
        tree_rf.delete(*tree_rf.get_children())
        
        # Loop through the loaded rainfall data (list of dictionaries)
        for record in rainfall_data_list: # <--- USE LOADED DATA
            
            date = record.get('date', '')
            rec_season = record.get('season', '')
            rec_region = record.get('region', '')
            match_start = (not start_iso) or (date >= start_iso)
            match_end = (not end_iso) or (date <= end_iso)
            match_season = (not season) or (rec_season.lower() == season)
            match_region = (not region) or (rec_region.lower() == region)
            
            if match_start and match_end and match_season and match_region:
                values_tuple = (
                    record.get('record_id'),
                    record.get('date'),
                    record.get('season'),
                    record.get('region'),
                    record.get('rainfall')
                )
                # Use record_id as the item ID (iid)
                tree_rf.insert("", "end", iid=record.get('record_id'), values=values_tuple)

    # --- Filter Frame (Rainfall) ---
    filter_frame_rf = tk.Frame(rainfall_tab, bg=FRAME_BG) # Parent is rainfall_tab
    filter_frame_rf.pack(pady=10, padx=20, fill="x") # Packed after table
    
    # ... (Filter widgets for rainfall tab) ...
    # Start Date
    start_var = tk.StringVar()
    lbl_start_date_rf = tk.Label(filter_frame_rf, text="Start Date:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_start_date_rf.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_start_date_rf = DateEntry(filter_frame_rf, textvariable=start_var)
    start_var.set('')
    entry_start_date_rf.grid(row=0, column=1, padx=5, pady=5)
    
    # End Date
    end_var = tk.StringVar()
    lbl_end_date_rf = tk.Label(filter_frame_rf, text="End Date:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_end_date_rf.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_end_date_rf = DateEntry(filter_frame_rf, textvariable=end_var)
    end_var.set('')
    entry_end_date_rf.grid(row=0, column=3, padx=5, pady=5)

    # Season
    lbl_season_rf = tk.Label(filter_frame_rf, text="Season:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_season_rf.grid(row=0, column=4, padx=5, pady=5, sticky="w")
    season_combobox_rf = ttk.Combobox(
        filter_frame_rf, 
        font=LABEL_FONT, 
        width=15, 
        values=["", "Winter", "Spring", "Summer", "Monsoon", "Autumn"]
    )
    season_combobox_rf.grid(row=0, column=5, padx=5, pady=5)
    
    # Region
    lbl_region_rf = tk.Label(filter_frame_rf, text="Region:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_region_rf.grid(row=0, column=6, padx=5, pady=5, sticky="w")
    entry_region_rf = tk.Entry(filter_frame_rf, font=LABEL_FONT, width=15)
    entry_region_rf.grid(row=0, column=7, padx=5, pady=5)


    # --- Reset Function (Rainfall) ---
    def reset_filters_rf():
        """Resets rainfall filters to default and re-runs filter."""
        start_var.set('')
        end_var.set('')
        season_combobox_rf.set("")
        entry_region_rf.delete(0, tk.END)
        # Re-run the filter to repopulate the table
        filter_data_rf()

    # Search Button (Rainfall)
    btn_search_rf = tk.Button(
        filter_frame_rf,
        text="🔎", 
        font=("Helvetica", 12), 
        relief="solid",
        borderwidth=1,
        command=filter_data_rf # Connected to rainfall filter
    )
    btn_search_rf.grid(row=0, column=8, padx=5, pady=5) # Reduced padding
    
    # Reset Button (Rainfall)
    btn_reset_rf = tk.Button(
        filter_frame_rf,
        text="Reset",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        command=reset_filters_rf # Connected to reset function
    )
    btn_reset_rf.grid(row=0, column=9, padx=5, pady=5)

    # --- Setup Treeview (Rainfall) ---
    tree_rf.heading("record_id", text="RECORD_ID")
    tree_rf.heading("date", text="DATE")
    tree_rf.heading("season", text="SEASON")
    tree_rf.heading("region", text="REGION")
    tree_rf.heading("rainfall", text="RAINFALL (mm)")
    
    tree_rf.column("record_id", width=80, anchor="center")
    tree_rf.column("date", width=120, anchor="center")
    tree_rf.column("season", width=120, anchor="center")
    tree_rf.column("region", width=120, anchor="center")
    tree_rf.column("rainfall", width=100, anchor="center") 
    
    for record in rainfall_data_list: # <--- USE LOADED DATA
        values_tuple = (
            record.get('record_id'),
            record.get('date'),
            record.get('season'),
            record.get('region'),
            record.get('rainfall')
        )
        # Use record_id as the item ID (iid)
        tree_rf.insert("", "end", iid=record.get('record_id'), values=values_tuple)

    scrollbar_rf = ttk.Scrollbar(table_frame_rf, orient="vertical", command=tree_rf.yview)
    tree_rf.configure(yscrollcommand=scrollbar_rf.set)
    scrollbar_rf.pack(side="right", fill="y")
    tree_rf.pack(side="left", fill="both", expand=True)
    
    # --- ###################### ---
    # ---  END: RAINFALL TAB   ---
    # --- ###################### ---


    # --- ########################### ---
    # --- BEGIN: GROUND WATER TAB   ---
    # --- ########################### ---

    # --- Treeview (Ground Water Table) ---
    table_frame_gw = tk.Frame(groundwater_tab) # Parent is groundwater_tab
    table_frame_gw.pack(pady=20, padx=20, fill="both", expand=True)
    
    columns_gw = ("res_id", "name", "type", "region", "capacity", "current_level", "status")
    # --- MODIFIED: Added selectmode="extended" to allow multi-select ---
    tree_gw = ttk.Treeview(table_frame_gw, columns=columns_gw, show="headings", selectmode="extended")
    
    # --- Filter Function (Ground Water) ---
    def filter_data_gw():
        """
        Filters data for the GROUND WATER table based on new data.
        """
        # Get values from new ground water filters
        region = entry_region_gw.get().strip().lower()
        res_type = type_combobox_gw.get().strip().lower()
        status = status_combobox_gw.get().strip().lower()
        
        # Clear the existing ground water table
        tree_gw.delete(*tree_gw.get_children())
        
        # Loop through the loaded ground water data
        for record in groundwater_data_list:
            
            # Access data by new dictionary keys
            rec_region = record.get('region', '').lower()
            rec_type = record.get('type', '').lower()
            rec_status = record.get('status', '').lower()
            
            # Match against new filter values
            match_region = (not region) or (rec_region == region)
            match_type = (not res_type) or (rec_type == res_type)
            match_status = (not status) or (rec_status == status)
            
            if match_region and match_type and match_status:
                # Create ordered tuple for insertion
                values_tuple = (
                    record.get('res_id'),
                    record.get('name'),
                    record.get('type'),
                    record.get('region'),
                    record.get('capacity'),
                    record.get('current_level'),
                    record.get('status')
                )
                # Use res_id as the item ID (iid)
                tree_gw.insert("", "end", iid=record.get('res_id'), values=values_tuple)

    # --- Filter Frame (Ground Water) ---
    filter_frame_gw = tk.Frame(groundwater_tab, bg=FRAME_BG) # Parent is groundwater_tab
    filter_frame_gw.pack(pady=10, padx=20, fill="x") # Packed after table
    
    # ... (Filter widgets for groundwater tab) ...
    # Region
    lbl_region_gw = tk.Label(filter_frame_gw, text="Region:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_region_gw.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_region_gw = tk.Entry(filter_frame_gw, font=LABEL_FONT, width=15)
    entry_region_gw.grid(row=0, column=1, padx=5, pady=5)
    
    # Type (was Season)
    lbl_type_gw = tk.Label(filter_frame_gw, text="Type:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_type_gw.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    type_combobox_gw = ttk.Combobox(
        filter_frame_gw, 
        font=LABEL_FONT, 
        width=15, 
        values=["", "Reservoir", "Lake", "Dam"] # New values
    )
    type_combobox_gw.grid(row=0, column=3, padx=5, pady=5)
    
    # Status (New Filter)
    lbl_status_gw = tk.Label(filter_frame_gw, text="Status:", font=LABEL_FONT, bg=FRAME_BG)
    lbl_status_gw.grid(row=0, column=4, padx=5, pady=5, sticky="w")
    status_combobox_gw = ttk.Combobox(
        filter_frame_gw, 
        font=LABEL_FONT, 
        width=15, 
        values=["", "Normal", "Low"] # New values
    )
    status_combobox_gw.grid(row=0, column=5, padx=5, pady=5)


    # --- Reset Function (Ground Water) ---
    def reset_filters_gw():
        """Resets ground water filters to default and re-runs filter."""
        # Reset new filters
        entry_region_gw.delete(0, tk.END)
        type_combobox_gw.set("")
        status_combobox_gw.set("")
        # Re-run the filter to repopulate the table
        filter_data_gw()

    # Search Button (Ground Water)
    btn_search_gw = tk.Button(
        filter_frame_gw,
        text="🔎", 
        font=("Helvetica", 12), 
        relief="solid",
        borderwidth=1,
        command=filter_data_gw # Connected to ground water filter
    )
    btn_search_gw.grid(row=0, column=6, padx=5, pady=5) # Adjusted column
    
    # Reset Button (Ground Water)
    btn_reset_gw = tk.Button(
        filter_frame_gw,
        text="Reset",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        command=reset_filters_gw # Connected to reset function
    )
    btn_reset_gw.grid(row=0, column=7, padx=5, pady=5) # Adjusted column
    
    # --- Setup Treeview (Ground Water) ---
    tree_gw.heading("res_id", text="RES_ID")
    tree_gw.heading("name", text="Name")
    tree_gw.heading("type", text="Type")
    tree_gw.heading("region", text="Region")
    tree_gw.heading("capacity", text="Capacity (ML)")
    tree_gw.heading("current_level", text="Current Level (ML)")
    tree_gw.heading("status", text="Status")
    
    tree_gw.column("res_id", width=60, anchor="center")
    tree_gw.column("name", width=150, anchor="center")
    tree_gw.column("type", width=100, anchor="center")
    tree_gw.column("region", width=110, anchor="center")
    tree_gw.column("capacity", width=120, anchor="center")
    tree_gw.column("current_level", width=130, anchor="center")
    tree_gw.column("status", width=100, anchor="center")
    
    for record in groundwater_data_list:
        values_tuple = (
            record.get('res_id'),
            record.get('name'),
            record.get('type'),
            record.get('region'),
            record.get('capacity'),
            record.get('current_level'),
            record.get('status')
        )
        # Use res_id as the item ID (iid)
        tree_gw.insert("", "end", iid=record.get('res_id'), values=values_tuple)

    scrollbar_gw = ttk.Scrollbar(table_frame_gw, orient="vertical", command=tree_gw.yview)
    tree_gw.configure(yscrollcommand=scrollbar_gw.set)
    scrollbar_gw.pack(side="right", fill="y")
    tree_gw.pack(side="left", fill="both", expand=True)

    # --- ########################### ---
    # ---  END: GROUND WATER TAB    ---
    # --- ########################### ---

    # --- ########################### ---
    # ---   EDIT AND SAVE LOGIC       ---
    # --- ########################### ---

    def on_tree_double_click(event, tree):
        """
        Handles the double-click event on either treeview to make a cell editable.
        """
        region_clicked = tree.identify_region(event.x, event.y)
        
        # Ensure the user clicked on a cell
        if region_clicked != "cell":
            return

        item_id = tree.identify_row(event.y) # This is the iid (record_id or res_id)
        column_id = tree.identify_column(event.x)
        column_index = int(column_id.replace('#', '')) - 1

        # Do not allow editing the first column (ID)
        if column_index == 0:
            return

        # Get cell bounds
        x, y, width, height = tree.bbox(item_id, column_id)

        # Create a temporary Entry widget
        entry = tk.Entry(tree, font=LABEL_FONT, relief="solid")
        entry.place(x=x, y=y, width=width, height=height)

        # Get current value and place it in the entry
        try:
            value = tree.item(item_id, 'values')[column_index]
        except IndexError:
            value = ""
            
        entry.insert(0, value)
        entry.select_range(0, 'end')
        entry.focus_set()

        def save_tree_edit(event):
            """
            Saves the value from the temporary Entry widget back to the tree
            AND updates the in-memory list.
            """
            try:
                new_value_str = entry.get() # Get value as string
                current_values = list(tree.item(item_id, 'values'))
                
                # --- Update the in-memory list with correct type ---
                record_id_to_find = int(item_id)
                new_value = new_value_str # Default to string

                if tree == tree_rf:
                    # Find the record in rainfall_data_list
                    column_key = columns_rf[column_index]
                    for record in rainfall_data_list:
                        if record.get('record_id') == record_id_to_find:
                            # Try to convert to original type
                            if column_key == 'rainfall':
                                new_value = float(new_value_str)
                            elif column_key == 'record_id':
                                new_value = int(new_value_str) # (This is disabled, but good practice)
                            
                            record[column_key] = new_value # Save converted value
                            break
                elif tree == tree_gw:
                    # Find the record in groundwater_data_list
                    column_key = columns_gw[column_index]
                    for record in groundwater_data_list:
                        if record.get('res_id') == record_id_to_find:
                            # Try to convert to original type
                            if column_key in ('capacity', 'current_level'):
                                new_value = float(new_value_str)
                            elif column_key == 'res_id':
                                new_value = int(new_value_str) # (This is disabled)

                            record[column_key] = new_value # Save converted value
                            break
                
                # Update the treeview visually
                current_values[column_index] = new_value # *** Use the converted value ***
                tree.item(item_id, values=tuple(current_values))
                
                entry.destroy()
            except (tk.TclError, IndexError, ValueError):
                # Handle error if widget is destroyed or item is gone
                # Or if conversion failed (e.g., "abc" to float)
                messagebox.showwarning("Input Error", 
                    f"Invalid data type for this column: {new_value_str}",
                    parent=dashboard_window)
                if entry:
                    entry.destroy()

        # Bind events to save and close the entry
        entry.bind('<Return>', save_tree_edit)
        entry.bind('<FocusOut>', save_tree_edit)
        entry.bind('<Escape>', lambda e: entry.destroy())

    # Bind the double-click event to both trees
    tree_rf.bind('<Double-1>', lambda e: on_tree_double_click(e, tree_rf))
    tree_gw.bind('<Double-1>', lambda e: on_tree_double_click(e, tree_gw))


    def save_rainfall_data():
        """Saves the in-memory rainfall_data_list to ./server/rainfall_data.json"""
        try:
            with open("./server/rainfall_data.json", 'w', encoding='utf-8') as f:
                json.dump(rainfall_data_list, f, indent=2)
            messagebox.showinfo("Save Successful", 
                "Rainfall data saved to ./server/rainfall_data.json.", parent=dashboard_window)
        except IOError as e:
            messagebox.showerror("Save Error", 
                f"Could not save ./server/rainfall_data.json.\nError: {e}", parent=dashboard_window)
        except TypeError as e:
             messagebox.showerror("Data Error", 
                f"Could not save rainfall data. Check data types.\nError: {e}", parent=dashboard_window)


    def save_groundwater_data():
        """Saves the in-memory groundwater_data_list to ground./server/water_data.json"""
        try:
            with open("./server/water_data.json", 'w', encoding='utf-8') as f:
                json.dump(groundwater_data_list, f, indent=2)
            messagebox.showinfo("Save Successful", 
                "Groundwater data saved to ./server/water_data.json.", parent=dashboard_window)
        except IOError as e:
            messagebox.showerror("Save Error", 
                f"Could not save ground./server/water_data.json.\nError: {e}", parent=dashboard_window)
        except TypeError as e:
             messagebox.showerror("Data Error", 
                f"Could not save groundwater data. Check data types.\nError: {e}", parent=dashboard_window)


    def save_current_tab_data():
        """Checks the active tab and calls the corresponding save function."""
        try:
            # --- FIX: Force focus away from any Entry widget ---
            # This triggers any pending <FocusOut> event *before* saving.
            dashboard_window.focus_set()
            
            current_tab_index = notebook.index(notebook.select())
            if current_tab_index == 0:
                save_rainfall_data()
            elif current_tab_index == 1:
                save_groundwater_data()
        except tk.TclError:
            # Handle case where no tab is selected (shouldn't happen)
            pass

    # --- ########################### ---
    # ---   ADD NEW DATA LOGIC        ---
    # --- ########################### ---

    def open_add_rainfall_window():
        """Opens a modal window to add a new rainfall record."""
        add_window_rf = tk.Toplevel(dashboard_window)
        add_window_rf.title("Add New Rainfall Record")
        add_window_rf.geometry("400x300")
        add_window_rf.configure(bg=WIN_BG)
        add_window_rf.transient(dashboard_window)
        add_window_rf.grab_set()

        form_frame = tk.Frame(add_window_rf, bg=WIN_BG, pady=10, padx=10)
        form_frame.pack(expand=True, fill="both")
        
        entries = {}
        
        # Create labels and entries for each column
        for i, col in enumerate(columns_rf):
            lbl = tk.Label(form_frame, text=f"{col.replace('_', ' ').title()}:", font=LABEL_FONT, bg=WIN_BG)
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            entry = tk.Entry(form_frame, font=LABEL_FONT, relief="solid", borderwidth=1, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[col] = entry

        def submit_new_rainfall():
            new_record = {}
            try:
                # Get and validate data
                new_record["record_id"] = int(entries["record_id"].get())
                new_record["date"] = entries["date"].get()
                new_record["season"] = entries["season"].get()
                new_record["region"] = entries["region"].get()
                new_record["rainfall"] = float(entries["rainfall"].get())
                
                # Check for duplicate ID
                for rec in rainfall_data_list:
                    if rec.get('record_id') == new_record["record_id"]:
                        messagebox.showerror("Error", "Record ID already exists.", parent=add_window_rf)
                        return

                # Add to in-memory list
                rainfall_data_list.append(new_record)
                
                # Add to treeview
                values_tuple = tuple(new_record.values())
                tree_rf.insert("", "end", iid=new_record["record_id"], values=values_tuple)
                
                # Save the entire list to JSON
                save_rainfall_data()
                
                add_window_rf.destroy()
                
            except ValueError:
                messagebox.showerror("Input Error", "Record ID must be an integer and Rainfall must be a number.", parent=add_window_rf)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}", parent=add_window_rf)

        submit_btn = tk.Button(
            form_frame, 
            text="Submit", 
            font=LABEL_FONT, 
            relief="solid", 
            borderwidth=1, 
            command=submit_new_rainfall
        )
        submit_btn.grid(row=len(columns_rf), column=0, columnspan=2, pady=10)


    def open_add_groundwater_window():
        """Opens a modal window to add a new groundwater record."""
        add_window_gw = tk.Toplevel(dashboard_window)
        add_window_gw.title("Add New Ground Water Record")
        add_window_gw.geometry("400x350")
        add_window_gw.configure(bg=WIN_BG)
        add_window_gw.transient(dashboard_window)
        add_window_gw.grab_set()

        form_frame = tk.Frame(add_window_gw, bg=WIN_BG, pady=10, padx=10)
        form_frame.pack(expand=True, fill="both")
        
        entries = {}
        
        # Create labels and entries for each column
        for i, col in enumerate(columns_gw):
            lbl = tk.Label(form_frame, text=f"{col.replace('_', ' ').title()}:", font=LABEL_FONT, bg=WIN_BG)
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            entry = tk.Entry(form_frame, font=LABEL_FONT, relief="solid", borderwidth=1, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[col] = entry

        def submit_new_groundwater():
            new_record = {}
            try:
                # Get and validate data
                new_record["res_id"] = int(entries["res_id"].get())
                new_record["name"] = entries["name"].get()
                new_record["type"] = entries["type"].get()
                new_record["region"] = entries["region"].get()
                new_record["capacity"] = float(entries["capacity"].get())
                new_record["current_level"] = float(entries["current_level"].get())
                new_record["status"] = entries["status"].get()
                
                # Check for duplicate ID
                for rec in groundwater_data_list:
                    if rec.get('res_id') == new_record["res_id"]:
                        messagebox.showerror("Error", "Reservoir ID already exists.", parent=add_window_gw)
                        return

                # Add to in-memory list
                groundwater_data_list.append(new_record)
                
                # Add to treeview
                values_tuple = tuple(new_record.values())
                tree_gw.insert("", "end", iid=new_record["res_id"], values=values_tuple)
                
                # Save the entire list to JSON
                save_groundwater_data()
                
                add_window_gw.destroy()
                
            except ValueError:
                messagebox.showerror("Input Error", "ID, Capacity, and Current Level must be numbers.", parent=add_window_gw)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}", parent=add_window_gw)

        submit_btn = tk.Button(
            form_frame, 
            text="Submit", 
            font=LABEL_FONT, 
            relief="solid", 
            borderwidth=1, 
            command=submit_new_groundwater
        )
        submit_btn.grid(row=len(columns_gw), column=0, columnspan=2, pady=10)

    def open_add_data_window():
        """Checks the active tab and calls the corresponding 'add' function."""
        try:
            current_tab_index = notebook.index(notebook.select())
            if current_tab_index == 0:
                open_add_rainfall_window()
            elif current_tab_index == 1:
                open_add_groundwater_window()
        except tk.TclError:
            pass # No tab selected

    # --- ########################### ---
    # ---   UPLOAD DATA LOGIC         ---
    # --- ########################### ---

    def upload_rainfall_data():
        """Opens a file dialog to upload and append rainfall data from a JSON file."""
        filepath = filedialog.askopenfilename(
            title="Select Rainfall JSON File",
            filetypes=[("JSON files", "*.json")],
            parent=dashboard_window
        )
        if not filepath:
            return # User cancelled

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                new_data = json.load(f)
            
            # --- Validation ---
            if not isinstance(new_data, list):
                messagebox.showerror("Error", "Invalid JSON format. The file must contain a list of records.", parent=dashboard_window)
                return

            required_keys = set(columns_rf)
            existing_ids = {rec['record_id'] for rec in rainfall_data_list}
            
            for i, record in enumerate(new_data):
                if not isinstance(record, dict) or not required_keys.issubset(record.keys()):
                    messagebox.showerror("Error", f"Record {i+1} in the uploaded file has a wrong data structure or missing keys.", parent=dashboard_window)
                    return
                
                # Check for duplicate IDs
                if record.get('record_id') in existing_ids:
                    messagebox.showerror("Error", f"Duplicate Record ID {record.get('record_id')} found in uploaded file. Aborting.", parent=dashboard_window)
                    return
            
            # --- Append and Update ---
            for record in new_data:
                rainfall_data_list.append(record)
                values_tuple = tuple(record.get(k) for k in columns_rf)
                tree_rf.insert("", "end", iid=record.get('record_id'), values=values_tuple)
            
            save_rainfall_data() # Save the newly appended data
            messagebox.showinfo("Success", f"Successfully uploaded and updated {len(new_data)} records.", parent=dashboard_window)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "The selected file is not a valid JSON file.", parent=dashboard_window)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=dashboard_window)
    

    def upload_groundwater_data():
        """Opens a file dialog to upload and append groundwater data from a JSON file."""
        filepath = filedialog.askopenfilename(
            title="Select Ground Water JSON File",
            filetypes=[("JSON files", "*.json")],
            parent=dashboard_window
        )
        if not filepath:
            return # User cancelled

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                new_data = json.load(f)
            
            # --- Validation ---
            if not isinstance(new_data, list):
                messagebox.showerror("Error", "Invalid JSON format. The file must contain a list of records.", parent=dashboard_window)
                return

            required_keys = set(columns_gw)
            existing_ids = {rec['res_id'] for rec in groundwater_data_list}
            
            for i, record in enumerate(new_data):
                if not isinstance(record, dict) or not required_keys.issubset(record.keys()):
                    messagebox.showerror("Error", f"Record {i+1} in the uploaded file has a wrong data structure or missing keys.", parent=dashboard_window)
                    return
                
                # Check for duplicate IDs
                if record.get('res_id') in existing_ids:
                    messagebox.showerror("Error", f"Duplicate Reservoir ID {record.get('res_id')} found in uploaded file. Aborting.", parent=dashboard_window)
                    return
            
            # --- Append and Update ---
            for record in new_data:
                groundwater_data_list.append(record)
                values_tuple = tuple(record.get(k) for k in columns_gw)
                tree_gw.insert("", "end", iid=record.get('res_id'), values=values_tuple)
            
            save_groundwater_data() # Save the newly appended data
            messagebox.showinfo("Success", f"Successfully uploaded and updated {len(new_data)} records.", parent=dashboard_window)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "The selected file is not a valid JSON file.", parent=dashboard_window)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=dashboard_window)


    def upload_data_for_current_tab():
        """Checks the active tab and calls the corresponding 'upload' function."""
        try:
            current_tab_index = notebook.index(notebook.select())
            if current_tab_index == 0:
                upload_rainfall_data()
            elif current_tab_index == 1:
                upload_groundwater_data()
        except tk.TclError:
            pass # No tab selected

    # --- ########################### ---
    # ---   NEW: DELETE DATA LOGIC    ---
    # --- ########################### ---

    def delete_rainfall_data():
        """Deletes all selected rows from the rainfall treeview and data file."""
        selected_items = tree_rf.selection() # Returns a tuple of iids
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select one or more rows to delete.", parent=dashboard_window)
            return
        
        # Ask for confirmation
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_items)} selected record(s)?", parent=dashboard_window):
            return
        
        try:
            # 1. Get a set of all integer IDs to be deleted
            ids_to_delete = {int(item_id) for item_id in selected_items}
            
            # 2. Create a new list excluding the records to be deleted
            new_rainfall_list = [record for record in rainfall_data_list if record.get('record_id') not in ids_to_delete]
            
            # 3. Update the main in-memory list
            rainfall_data_list.clear()
            rainfall_data_list.extend(new_rainfall_list)
            
            # 4. Remove items from the Treeview
            for item_id in selected_items:
                tree_rf.delete(item_id)
                
            # 5. Save the updated list to the JSON file
            save_rainfall_data() # This function will show its own success/error message
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deletion: {e}", parent=dashboard_window)
            
    def delete_groundwater_data():
        """Deletes all selected rows from the groundwater treeview and data file."""
        selected_items = tree_gw.selection() # Returns a tuple of iids
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select one or more rows to delete.", parent=dashboard_window)
            return
        
        # Ask for confirmation
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_items)} selected record(s)?", parent=dashboard_window):
            return
        
        try:
            # 1. Get a set of all integer IDs to be deleted
            ids_to_delete = {int(item_id) for item_id in selected_items}
            
            # 2. Create a new list excluding the records to be deleted
            new_groundwater_list = [record for record in groundwater_data_list if record.get('res_id') not in ids_to_delete]
            
            # 3. Update the main in-memory list
            groundwater_data_list.clear()
            groundwater_data_list.extend(new_groundwater_list)
            
            # 4. Remove items from the Treeview
            for item_id in selected_items:
                tree_gw.delete(item_id)
                
            # 5. Save the updated list to the JSON file
            save_groundwater_data() # This function will show its own success/error message
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deletion: {e}", parent=dashboard_window)

    def delete_data_for_current_tab():
        """Checks the active tab and calls the corresponding 'delete' function."""
        try:
            current_tab_index = notebook.index(notebook.select())
            if current_tab_index == 0:
                delete_rainfall_data()
            elif current_tab_index == 1:
                delete_groundwater_data()
        except tk.TclError:
            pass # No tab selected
            
    # --- ########################### ---
    # --- END NEW DELETE DATA LOGIC ---
    # --- ########################### ---


    # --- Bottom Button Frame (Add, Upload, Delete, Save & Back) ---
    bottom_button_frame = tk.Frame(dashboard_window, bg=WIN_BG)
    bottom_button_frame.pack(pady=10)

    btn_add_data = tk.Button(
        bottom_button_frame,
        text="Add Data",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        width=15,
        command=open_add_data_window # Connect to new function
    )
    btn_add_data.pack(side="left", padx=10)

    btn_upload_data = tk.Button(
        bottom_button_frame,
        text="Upload Data",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        width=15,
        command=upload_data_for_current_tab # Connect to upload dispatcher
    )
    btn_upload_data.pack(side="left", padx=10)

    # --- NEW: Delete Data Button ---
    btn_delete_data = tk.Button(
        bottom_button_frame,
        text="Delete Data",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        width=15,
        command=delete_data_for_current_tab # Connect to delete dispatcher
    )
    btn_delete_data.pack(side="left", padx=10)
    # --- END NEW BUTTON ---

    btn_save = tk.Button(
        bottom_button_frame,
        text="Save Changes",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        width=15,
        command=save_current_tab_data # Connect to save function
    )
    btn_save.pack(side="left", padx=10)

    btn_back = tk.Button(
        bottom_button_frame,
        text="Back",
        font=LABEL_FONT,
        relief="solid",
        borderwidth=1,
        width=15,
        command=dashboard_window.destroy 
    )
    btn_back.pack(side="left", padx=10)

# --- You would still need your main() and login functions ---
# --- to call admin_dashboard(root) ---

# Example of how to run this (if you don't have your main file)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main App (Hidden)")
    root.geometry("100x100")
    
    # --- Create dummy JSON files if they don't exist ---
    import os
    if not os.path.exists("./server"):
        os.makedirs("./server")
        
    if not os.path.exists("./server/rainfall_data.json"):
        with open("./server/rainfall_data.json", 'w') as f:
            json.dump([
                {"record_id": 1, "date": "2025-01-01", "season": "Winter", "region": "North", "rainfall": 10.5},
                {"record_id": 2, "date": "2025-01-02", "season": "Winter", "region": "South", "rainfall": 5.2}
            ], f, indent=2)
            
    if not os.path.exists("./server/water_data.json"):
        with open("./server/water_data.json", 'w') as f:
            json.dump([
                {"res_id": 101, "name": "Main Lake", "type": "Lake", "region": "North", "capacity": 5000, "current_level": 4500, "status": "Normal"},
                {"res_id": 102, "name": "South Dam", "type": "Dam", "region": "South", "capacity": 10000, "current_level": 3000, "status": "Low"}
            ], f, indent=2)
    # --- End of dummy file creation ---
    
    
    # Button to open the dashboard
    btn = tk.Button(root, text="Open Admin Dashboard", command=lambda: admin_dashboard(root))
    btn.pack(pady=20, padx=20)
    
    root.withdraw() # Hide the main root window
    admin_dashboard(root) # Open the dashboard immediately
    
    root.mainloop()