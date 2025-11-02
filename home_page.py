import tkinter as tk

def home_page(root, frame, goto_rain, goto_water):
    tk.Label(frame, text="Weather Report", font=("Arial", 28)).pack(pady=40)
    tk.Button(frame, text="Rainfall Data Page", command=goto_rain, width=20).pack(pady=10)
    tk.Button(frame, text="Groundwater Data Page", command=goto_water, width=20).pack(pady=10)
