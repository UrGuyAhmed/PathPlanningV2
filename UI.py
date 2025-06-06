import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import copy
import threading
from Start import add_start_buttons  
from twoD import ShowMap2D

root = tk.Tk()

def ShowMainPage():
    """Return to the main page."""
    for widget in root.winfo_children():
        widget.destroy()
    MainPage()

def MainPage():
    """Initialize the main page UI."""
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    root.title("Path Planning")
    root.geometry("800x800")
    title_label = tk.Label(root, text="Path Planning", bg="black", fg="white", font=("Bahnschrift", 36))
    title_label.pack(pady=50)
    description_label = tk.Label(root, text="Visualize path planning algorithms on a map.", bg="black", fg="white", font=("Bahnschrift", 16))
    description_label.pack(pady=20)
    add_start_buttons(root, on_2d=ShowMap2D)  
    credit_label = tk.Label(root, text="Created by Ahmed Yacine Ahriche", bg="black", fg="white", font=("Bahnschrift", 10))
    credit_label.pack(side="bottom", pady=5)
    close_button = tk.Button(
        root,
        text="Close",
        command=root.destroy,
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 12),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0
    )
    close_button.pack(side="bottom", pady=10)



if __name__ == "__main__":
    MainPage()
    root.mainloop()