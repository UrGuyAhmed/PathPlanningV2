import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def clean_up():
    """Clear the main window."""
    for widget in tk._default_root.winfo_children():
        widget.destroy()

def ShowMap2D(map_holder=None, back_callback=None):
    clean_up()
    root = tk._default_root

    label = tk.Label(root, text="Map", bg="black", fg="white", font=("Bahnschrift", 24))
    label.pack(pady=50)

    img_label = tk.Label(root, bg="black")
    img_label.pack(pady=20)

    def upload_action():
        file_path = filedialog.askopenfilename(
            title="Select your map",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            if map_holder:
                map_holder.load_map(file_path)  # Use MapHolder to load the map
            img = Image.open(file_path)
            display_width, display_height = 500, 500
            img = img.resize((display_width, display_height), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            img_label.config(image=tk_img)
            img_label.image = tk_img

    upload_map = tk.Button(
        root,
        text="Upload Map",
        bg="#222222",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        font=("Bahnschrift", 14),
        width=10,
        height=1,
        borderwidth=0,
        highlightthickness=0,
        command=upload_action
    )
    upload_map.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)

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
        command=back_callback if back_callback else root.destroy
    )
    back_btn.place(relx=0.0, rely=1.0, anchor="sw", x=30, y=-30)