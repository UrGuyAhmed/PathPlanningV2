import tkinter as tk
from twoDNormal import ShowMap2D

class MapHolder:
    def __init__(self):
        self.map_data = None

    def load_map(self, path):
        # Load map logic here
        self.map_data = path  # Example

def show_map_holder(back_callback=None):
    """Display the map holder interface."""
    root = tk.Tk()
    root.title("Map Holder")
    root.geometry("800x600")
    root.configure(bg="black")

    label = tk.Label(root, text="Map Holder", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=50)

    def open_map():
        ShowMap2D(back_callback=back_callback)

    open_map_button = tk.Button(
        root,
        text="Open Map",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=open_map
    )
    open_map_button.place(relx=0.5, rely=0.5, anchor="center")

    if back_callback:
        back_btn = tk.Button(
            root,
            text="Back",
            bg="#222222",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            font=("Bahnschrift", 14),
            width=10,
            height=1,
            borderwidth=0,
            highlightthickness=0,
            command=back_callback
        )
        back_btn.place(relx=0.0, rely=1.0, anchor="sw", x=30, y=-30)

    root.mainloop()