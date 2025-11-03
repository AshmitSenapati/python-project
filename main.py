import tkinter as tk
from tkinter import messagebox
import json
import subprocess
import sys
from admin_page import admin_dashboard

try:
    # Try to open and load the JSON file
    with open("./server/users.json", 'r', encoding='utf-8') as f:
        USER_DATABASE = json.load(f)
except FileNotFoundError:
    # Mark as not found, will be handled in main()
    USER_DATABASE = "NOT_FOUND" 
except json.JSONDecodeError:
    # Mark as corrupted, will be handled in main()
    USER_DATABASE = "CORRUPTED"

def open_admin_portal(parent):
    """
    Called when the 'Administrator' button is clicked.
    Opens a new Toplevel window for admin login.
    """
    WIN_BG = "#e0e0e0"
    LABEL_FONT = ("Helvetica", 11)
    BUTTON_FONT = ("Helvetica", 12, "bold")
    
    admin_window = tk.Toplevel(parent)
    admin_window.title("Admin Login")
    admin_window.geometry("600x400") 
    admin_window.configure(bg=WIN_BG)
    
    login_frame = tk.Frame(admin_window, bg=WIN_BG, pady=20, padx=20)
    login_frame.pack(expand=True, fill="both")

    btn_back = tk.Button(
        login_frame,
        text="Back",
        font=("Helvetica", 10),
        relief="solid",
        borderwidth=1,
        cursor="hand2",
        command=admin_window.destroy
    )
    btn_back.pack(anchor="w", pady=(0, 10)) 

    lbl_heading = tk.Label(
        login_frame,
        text="Admin Page",
        font=("Helvetica", 16, "bold"),
        bg=WIN_BG
    )
    lbl_heading.pack(pady=(0, 20)) 

    form_frame = tk.Frame(login_frame, bg=WIN_BG)
    form_frame.pack(pady=5, padx=20)
    
    # --- Center the grid columns ---
    form_frame.grid_columnconfigure(0, weight=1) # Left spacer
    form_frame.grid_columnconfigure(1, weight=0) # Label column
    form_frame.grid_columnconfigure(2, weight=0) # Entry column
    form_frame.grid_columnconfigure(3, weight=0) # Checkbutton column
    form_frame.grid_columnconfigure(4, weight=1) # Right spacer

    # User ID
    lbl_user = tk.Label(form_frame, text="User ID:", font=LABEL_FONT, bg=WIN_BG)
    lbl_user.grid(row=0, column=1, sticky="e", padx=5, pady=5)
    entry_user = tk.Entry(
        form_frame, 
        font=LABEL_FONT, 
        width=25, 
        justify='center', 
        relief="solid",  
        borderwidth=1    
    )
    entry_user.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    # Password
    lbl_pass = tk.Label(form_frame, text="Password:", font=LABEL_FONT, bg=WIN_BG)
    lbl_pass.grid(row=1, column=1, sticky="e", padx=5, pady=5)
    entry_pass = tk.Entry(
        form_frame, 
        font=LABEL_FONT, 
        show="*", # Initially hidden
        width=25, 
        justify='center', 
        relief="solid", 
        borderwidth=1    
    )
    entry_pass.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    
    # --- NEW: Checkbutton for Password Visibility (without text) ---
    show_pass_var = tk.IntVar(value=0) # 0 for hidden, 1 for shown
    
    def toggle_password_visibility():
        """Toggles the password field's visibility."""
        if show_pass_var.get() == 1: # 1 means checked (show password)
            entry_pass.config(show="")
        else: # 0 means unchecked (hide password)
            entry_pass.config(show="*")

    chk_show_pass = tk.Checkbutton( # Back to Checkbutton
        form_frame,
        # No 'text' attribute
        variable=show_pass_var,
        onvalue=1,
        offvalue=0,
        command=toggle_password_visibility,
        bg=WIN_BG # Match background
    )
    chk_show_pass.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w") # Adjusted padx
    # --- END NEW CODE ---

    # Login Button
    btn_login = tk.Button(
        login_frame,
        text="Login",
        font=BUTTON_FONT,
        relief="solid",
        borderwidth=1,
        cursor="hand2",
        command=lambda: perform_admin_login(parent, entry_user.get(), entry_pass.get(), admin_window)
    )
    btn_login.pack(pady=20, ipadx=30, ipady=5)

def open_client_portal(parent):
    """
    Called when the 'Client' button is clicked.
    Opens a new Toplevel window for client login.
    """
    WIN_BG = "#e0e0e0"
    LABEL_FONT = ("Helvetica", 11)
    BUTTON_FONT = ("Helvetica", 12, "bold")

    client_window = tk.Toplevel(parent)
    client_window.title("Client Login")
    client_window.geometry("600x400")
    client_window.configure(bg=WIN_BG)
    
    login_frame = tk.Frame(client_window, bg=WIN_BG, pady=20, padx=20)
    login_frame.pack(expand=True, fill="both")

    btn_back = tk.Button(
        login_frame,
        text="Back",
        font=("Helvetica", 10),
        relief="solid",
        borderwidth=1,
        cursor="hand2",
        command=client_window.destroy
    )
    btn_back.pack(anchor="w", pady=(0, 10)) 

    lbl_heading = tk.Label(
        login_frame,
        text="Client Page",
        font=("Helvetica", 16, "bold"),
        bg=WIN_BG
    )
    lbl_heading.pack(pady=(0, 20))

    form_frame = tk.Frame(login_frame, bg=WIN_BG)
    form_frame.pack(pady=5, padx=20)

    # --- Center the grid columns ---
    form_frame.grid_columnconfigure(0, weight=1) # Left spacer
    form_frame.grid_columnconfigure(1, weight=0) # Label column
    form_frame.grid_columnconfigure(2, weight=0) # Entry column
    form_frame.grid_columnconfigure(3, weight=0) # Checkbutton column
    form_frame.grid_columnconfigure(4, weight=1) # Right spacer

    # User ID
    lbl_user = tk.Label(form_frame, text="User ID:", font=LABEL_FONT, bg=WIN_BG)
    lbl_user.grid(row=0, column=1, sticky="e", padx=5, pady=5)
    entry_user = tk.Entry(
        form_frame, 
        font=LABEL_FONT, 
        width=25, 
        justify='center',
        relief="solid",
        borderwidth=1
    )
    entry_user.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    # Password
    lbl_pass = tk.Label(form_frame, text="Password:", font=LABEL_FONT, bg=WIN_BG)
    lbl_pass.grid(row=1, column=1, sticky="e", padx=5, pady=5)
    entry_pass = tk.Entry(
        form_frame, 
        font=LABEL_FONT, 
        show="*", # Initially hidden
        width=25, 
        justify='center',
        relief="solid",
        borderwidth=1
    )
    entry_pass.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    
    # --- NEW: Checkbutton for Password Visibility (without text) ---
    show_pass_var = tk.IntVar(value=0) # 0 for hidden, 1 for shown
    
    def toggle_password_visibility():
        """Toggles the password field's visibility."""
        if show_pass_var.get() == 1: # 1 means checked (show password)
            entry_pass.config(show="")
        else: # 0 means unchecked (hide password)
            entry_pass.config(show="*")

    chk_show_pass = tk.Checkbutton( # Back to Checkbutton
        form_frame,
        # No 'text' attribute
        variable=show_pass_var,
        onvalue=1,
        offvalue=0,
        command=toggle_password_visibility,
        bg=WIN_BG # Match background
    )
    chk_show_pass.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w") # Adjusted padx
    # --- END NEW CODE ---

    # Login Button
    btn_login = tk.Button(
        login_frame,
        text="Login",
        font=BUTTON_FONT,
        relief="solid",
        borderwidth=1,
        cursor="hand2",
        command=lambda: perform_client_login(entry_user.get(), entry_pass.get(), client_window)
    )
    btn_login.pack(pady=20, ipadx=30, ipady=5)

def perform_admin_login(parent, username, password, login_frame):
    for user in USER_DATABASE:
        if (user["user_type"] == "admin" and
            user["user_name"] == username and
            user["password"] == password):
            
            messagebox.showinfo(
                "Administrator Access",
                f"Login Successful!\nWelcome, {username}\n\nLoading Administrator Dashboard..."
            )
            admin_dashboard(parent)
            login_frame.destroy()
            break
    else:
        messagebox.showwarning("Login Failed", "Incorrect User ID or Password.")

def perform_client_login(username, password, login_frame):
    for user in USER_DATABASE:
        if (user["user_type"] == "client" and
            user["user_name"] == username and
            user["password"] == password):
            
            messagebox.showinfo(
                "Client Access",
                f"Login Successful!\nWelcome, {username}\n\nLoading Client Dashboard..."
            )
            subprocess.Popen([sys.executable, "client_page.py"])
            login_frame.destroy()
            break
    else:
        messagebox.showwarning("Login Failed", "Incorrect User ID or Password.")

def main():
    """
    Sets up and runs the main tkinter application window.
    """
    # 1. Create the main window
    root = tk.Tk()
    root.title("Rainfall & Water Resource Monitoring")

    # --- Database Load Check ---
    # Check the status of the USER_DATABASE loaded at the start
    if USER_DATABASE == "NOT_FOUND":
        messagebox.showerror("Fatal Error", 
            "User database file (users.json) not found.\nApplication will close.")
        root.destroy()
        return # Exit
    elif USER_DATABASE == "CORRUPTED":
        messagebox.showerror("Fatal Error", 
            "User database file (users.json) is corrupted.\nApplication will close.")
        root.destroy()
        return # Exit
    # --- End of Check ---
    
    root.geometry("800x500")
    
    # Matched background color
    WIN_BG = "#e0e0e0"
    root.configure(bg=WIN_BG)
    
    # Center the window on the screen
    root.eval('tk::PlaceWindow . center')

    # 2. Define Fonts
    TITLE_FONT = ("Helvetica", 18, "bold")
    SUBTITLE_FONT = ("Helvetica", 12)
    BUTTON_FONT = ("Helvetica", 12, "bold") # Matched login button font
    ICON_FONT = ("Helvetica", 48) # Re-added icon font
    FRAME_BG = "#e0e0e0" # White background for the card
    
    # 3. Create a main frame to hold all content (Restored)
    main_frame = tk.Frame(
        root,
        bg=FRAME_BG,
        padx=40,
        pady=40,
        relief="ridge",
        borderwidth=0
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # 4. Create Frames for Layout (Icons and Content) (Restored)
    
    # --- Icon Frame (Left Column) ---
    icon_frame = tk.Frame(main_frame, bg=FRAME_BG)
    icon_frame.pack(side="left", padx=(0, 40), fill="y", anchor="n")
    
    # --- Content Frame (Right Column) ---
    content_frame = tk.Frame(main_frame, bg=FRAME_BG)
    content_frame.pack(side="left", fill="y")

    # 5. Create the Widgets
    
    # --- Icon Widgets (in icon_frame) (Restored) ---
    lbl_icon1 = tk.Label(
        icon_frame,
        text="🌧️",  # Rain cloud emoji
        font=ICON_FONT,
        bg=FRAME_BG,
        fg="#000000"
    )
    lbl_icon2 = tk.Label(
        icon_frame,
        text="🌩️",  # Storm cloud emoji
        font=ICON_FONT,
        bg=FRAME_BG,
        fg="#000000"
    )
    lbl_icon3 = tk.Label(
        icon_frame,
        text="🌤️",  # Sun with cloud emoji
        font=ICON_FONT,
        bg=FRAME_BG,
        fg="#000000"
    )
    
    # --- Content Widgets (in content_frame) ---
    lbl_title = tk.Label(
        content_frame, # Moved back into content_frame
        text="Rainfall & Water Resource Monitoring System",
        font=TITLE_FONT,
        bg=FRAME_BG # Matched card background
    )
    
    lbl_subtitle = tk.Label(
        content_frame, # Moved back into content_frame
        text="Please select your role and proceed to login:",
        font=SUBTITLE_FONT,
        bg=FRAME_BG # Matched card background
    )

    btn_admin = tk.Button(
        content_frame, # Moved back into content_frame
        text="Administrator",
        font=BUTTON_FONT,
        command=lambda: open_admin_portal(root),
        width=20,
        pady=12,
        relief="solid", # Matched button style
        borderwidth=1,
        cursor="hand2"
    )
    
    btn_client = tk.Button(
        content_frame, # Moved back into content_frame
        text="Client",
        font=BUTTON_FONT,
        command=lambda: open_client_portal(root),
        width=20,
        pady=12,
        relief="solid", # Matched button style
        borderwidth=1,
        cursor="hand2"
    )

    # 6. Lay out the widgets
    
    # Pack icons vertically (Restored)
    lbl_icon1.pack(pady=(10, 15))
    lbl_icon2.pack(pady=15)
    lbl_icon3.pack(pady=15)
    
    # Pack content vertically (Restored)
    lbl_title.pack(pady=(25, 10))
    lbl_subtitle.pack(pady=(0, 30))
    btn_admin.pack(pady=10)
    btn_client.pack(pady=10)

    # 7. Start the application's main loop
    root.mainloop()

if __name__ == '__main__':
    main()
