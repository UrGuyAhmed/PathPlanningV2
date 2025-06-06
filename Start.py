import tkinter as tk

def add_start_buttons(parent, on_2d=None, on_3d=None):
    button_frame = tk.Frame(parent, bg="black")
    button_frame.pack(pady=30)

    start_button_2d = tk.Button(
        button_frame,
        text="2D",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 24),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0,
        command=on_2d 
    )
    start_button_2d.pack(side=tk.LEFT, padx=10)

    start_button_3d = tk.Button(
        button_frame,
        text="3D",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 24),
        width=10,
        height=2,
        borderwidth=0,
        highlightthickness=0,
        command=on_3d 
    )
    start_button_3d.pack(side=tk.LEFT, padx=10)
