import tkinter as tk
from home_page import home_page
from rain_data_page import rain_data_page
from water_data_page import water_data_page

def show_home():
    clear_content()
    home_page(root, content_frame, switch_to_rain, switch_to_water)

def switch_to_rain():
    clear_content()
    rain_data_page(root, content_frame, show_home)

def switch_to_water():
    clear_content()
    water_data_page(root, content_frame, show_home)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Weather Report")
root.geometry("1000x500")

content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)

show_home()
root.mainloop()
